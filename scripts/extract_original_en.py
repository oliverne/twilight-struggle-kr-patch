#!/usr/bin/env python3
"""원본 resources.assets 내 TextAsset에서 문자열 추출.

용도: 원본 게임의 Common_Strings, TS_Cards 등 TextAsset에서
      (행 키, 영문 원문) 쌍을 추출해 번역 소스 JSON을 생성.

TextAsset 본문 구조: 첫 줄은 날짜 헤더("28 July, (22:46)"),
나머지는 {"0": {"행:열": "값", ...}} 형식의 JSON.
  - 열 1 = 키 (Key_XXX 또는 Card_XXXTitle/Text 등)
  - 열 2 = EN (영문 원문)
  - 나머지 열 = 타 언어 또는 "null"

사용법:
  extract_original_en.py <입력.resources> <TextAsset이름> <출력.json>

출력 JSON 스키마:
  {
    "asset_name": "Common_Strings",
    "header": "28 July, (22:46)",
    "row_count": N,
    "rows": [
      {"row": 행번호, "key": "Key_PlayOffline", "en": "Play Offline"},
      ...
    ]
  }
"""
import json
import struct
import sys

import UnityPy


def pad4(n: int) -> int:
    return (4 - n % 4) % 4


def parse_raw(raw: bytes):
    name_len = struct.unpack_from("<i", raw, 0)[0]
    name = raw[4 : 4 + name_len].decode("utf-8")
    off = 4 + name_len + pad4(4 + name_len)
    script_len = struct.unpack_from("<i", raw, off)[0]
    script = raw[off + 4 : off + 4 + script_len]
    return name, script


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    src = sys.argv[1]
    asset_name = sys.argv[2]
    out_path = sys.argv[3]

    env = UnityPy.load(src)
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw(obj.get_raw_data())
        if name != asset_name:
            continue

        text = script.decode("utf-8")
        # 첫 줄(날짜 헤더) 분리
        first_nl = text.find("\n")
        header = text[:first_nl] if first_nl != -1 else ""
        body = text[first_nl + 1 :] if first_nl != -1 else text

        data = json.loads(body)
        rows = []
        by_row: dict[int, dict[int, str]] = {}
        # 모든 최상위 키 처리 (TS_Cards는 "0" + 타임스탬프 키 2개)
        for top_key, inner in data.items():
            if not isinstance(inner, dict):
                continue
            for cell_key, val in inner.items():
                if ":" not in cell_key:
                    continue
                row_s, col_s = cell_key.split(":", 1)
                try:
                    row = int(row_s)
                    col = int(col_s)
                except ValueError:
                    continue
                by_row.setdefault(row, {})[col] = val

        for row in sorted(by_row.keys()):
            cols = by_row[row]
            key = cols.get(1, "")
            en = cols.get(2, "")
            if key and en and en != "null":
                rows.append({"row": row, "key": key, "en": en})

        result = {
            "asset_name": asset_name,
            "header": header,
            "row_count": len(by_row),
            "rows_with_en": len(rows),
            "rows": rows,
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"헤더: {header}")
        print(f"전체 행: {len(by_row)}, EN 포함 행: {len(rows)}")
        print(f"→ {out_path}")
        return 0

    print(f"TextAsset '{asset_name}' 없음", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())