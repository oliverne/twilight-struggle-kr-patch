#!/usr/bin/env python3
"""블루칩 패치 resources.assets 내 MonoBehaviour에서 한글 문자열 추출.

용도: 기존 한글 패치의 번역을 재사용하기 위해 MonoBehaviour string 필드에서
      한글이 포함된 문자열을 추출해 JSON으로 저장.

배경:
  - 블루칩 v1.0.1(100% 한글화)은 번역을 resources.assets 내 MonoBehaviour의
    string 필드에 직접 주입했다.
  - UnityPy의 고수준 obj.read()는 IL2CPP 타입트리 불완전으로 실패.
  - 대신 get_raw_data()로 raw 바이트를 받아 Unity string 표준 레이아웃
    (int32 len + bytes + pad4)을 수동 파싱한다.

사용법:
  extract_bluechip_kr.py <입력.resources> <출력.json>

출력 JSON 스키마:
  {
    "source": "<입력경로>",
    "total_objects": N,
    "mono_behaviours": M,
    "mono_with_korean": K,
    "strings": [
      {
        "path_id": int,
        "m_name": "MonoBehaviour 이름 (빈 문자열 가능)",
        "offset": int,        # raw 내 string 필드 오프셋
        "length": int,         # 문자열 바이트 길이
        "text": "추출된 문자열"  # UTF-8 디코딩, 한글 포함
      },
      ...
    ],
    "unique_texts": { "고유 문자열": [path_id, ...] }
  }
"""
import json
import re
import struct
import sys

import UnityPy


def pad4(n: int) -> int:
    return (4 - n % 4) % 4


def extract_strings(raw: bytes):
    """raw 바이트에서 Unity string 필드(int32 len + bytes + pad4) 스캔.

    Returns: list of (offset, length, text)
    """
    out = []
    off = 0
    L = len(raw)
    while off + 4 <= L:
        ln = struct.unpack_from("<i", raw, off)[0]
        if 0 < ln <= 8000 and off + 4 + ln <= L:
            s = raw[off + 4 : off + 4 + ln]
            pad = pad4(ln)
            if raw[off + 4 + ln : off + 4 + ln + pad] == b"\x00" * pad:
                try:
                    txt = s.decode("utf-8")
                    # 유효한 텍스트만 (제어문자 제외, \n\r 허용)
                    if txt.strip() and all(
                        c in "\n\r\t" or 32 <= ord(c) < 0x10000 for c in txt
                    ):
                        out.append((off, ln, txt))
                except UnicodeDecodeError:
                    pass
        off += 1
    return out


def is_korean(text: str) -> bool:
    return any("\uac00" <= c <= "\ud7a3" for c in text)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out_path = sys.argv[2]

    env = UnityPy.load(src)
    total = 0
    mono_count = 0
    mono_with_ko = 0
    strings = []
    unique_texts: dict[str, list[int]] = {}

    for obj in env.objects:
        total += 1
        if obj.type.name != "MonoBehaviour":
            continue
        mono_count += 1
        raw = obj.get_raw_data()
        if not re.search(rb"[\xea-\xed][\x80-\xbf]{2}", raw):
            continue

        # m_Name 추출 (Unity MonoBehaviour 헤더):
        #   m_GameObject (PPtr: int fileID + int + i64 pathID = 12B? 실제론 int+int+long)
        #   m_Enabled (int8 + 3 pad)
        #   m_Script (PPtr 12B)
        #   m_Name (string)
        # UnityPy PPtr는 일반적으로 (int fileID, long pathID) = 12B
        m_name = ""
        try:
            # m_GameObject(12) + m_Enabled(4) + m_Script(12) = 28 offset
            nl = struct.unpack_from("<i", raw, 28)[0]
            if 0 < nl < 200:
                m_name = raw[32 : 32 + nl].decode("utf-8", "replace")
        except Exception:
            pass

        found_ko = False
        for off, ln, txt in extract_strings(raw):
            if is_korean(txt):
                found_ko = True
                strings.append(
                    {
                        "path_id": obj.path_id,
                        "m_name": m_name,
                        "offset": off,
                        "length": ln,
                        "text": txt,
                    }
                )
                unique_texts.setdefault(txt, []).append(obj.path_id)
        if found_ko:
            mono_with_ko += 1

    result = {
        "source": src,
        "total_objects": total,
        "mono_behaviours": mono_count,
        "mono_with_korean": mono_with_ko,
        "korean_string_count": len(strings),
        "unique_text_count": len(unique_texts),
        "strings": strings,
        "unique_texts": {k: v for k, v in unique_texts.items()},
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"총 오브젝트: {total}")
    print(f"MonoBehaviour: {mono_count}")
    print(f"한글 포함 MonoBehaviour: {mono_with_ko}")
    print(f"한글 문자열: {len(strings)}")
    print(f"고유 문자열: {len(unique_texts)}")
    print(f"→ {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())