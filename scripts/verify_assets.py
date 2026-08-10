#!/usr/bin/env python3
"""패치 후 에셋 무결성 검증 스크립트

원본 vs 패치본을 비교해 MonoBehaviour m_Script 참조와
수정 의도 밖의 raw 데이터가 보존됐는지 확인한다.

사용법:
  python scripts/verify_assets.py --orig <원본 resources.assets> --patched <패치본>

의도된 변경(허용):
  - TextAsset 내용 (번역 주입)
  - TMP 폰트 MonoBehaviour + 아틀라스 Texture2D + Material (폰트 주입)
  - 그 외 모든 객체는 raw 바이트가 동일해야 함
"""

import argparse
import struct
import sys
from pathlib import Path

import UnityPy

# Windows 콘솔(cp949)에서 UTF-8 출력 보장
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FONT_PATH_RANGE = (30683, 30707)  # resources.assets의 TMP 폰트/Sprite PathID 범위


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]


def u64(b: bytes, o: int) -> int:
    return struct.unpack_from("<Q", b, o)[0]


def load(path: str) -> dict:
    env = UnityPy.load(path)
    return {obj.path_id: obj for obj in env.objects}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig", required=True)
    ap.add_argument("--patched", required=True)
    args = ap.parse_args()

    orig = load(args.orig)
    patched = load(args.patched)
    print(f"original: {len(orig)} 객체 | patched: {len(patched)} 객체")

    script_mismatch = 0
    unexpected_raw = 0
    expected_font = 0
    expected_text = 0

    for pid, obj in orig.items():
        po = patched.get(pid)
        if po is None:
            print(f"  ❌ patched에 객체 없음: PathID={pid}")
            continue

        # m_Script 참조 무손상 확인
        if obj.type.name == "MonoBehaviour":
            r1, r2 = obj.get_raw_data(), po.get_raw_data()
            if len(r1) >= 28 and len(r2) >= 28:
                s1 = (u32(r1, 16), u64(r1, 20))
                s2 = (u32(r2, 16), u64(r2, 20))
                if s1 != s2:
                    script_mismatch += 1
                    if script_mismatch <= 5:
                        print(f"  ❌ m_Script 변경: PathID={pid} {s1} → {s2}")

        # raw 바이트 비교 (의도된 변경 분류)
        if obj.get_raw_data() == po.get_raw_data():
            continue
        if obj.type.name == "TextAsset":
            expected_text += 1
        elif obj.type.name == "MonoBehaviour" and FONT_PATH_RANGE[0] <= pid <= FONT_PATH_RANGE[1]:
            expected_font += 1
        elif obj.type.name in ("Texture2D", "Material"):
            expected_font += 1
        else:
            unexpected_raw += 1
            if unexpected_raw <= 10:
                print(f"  ❌ 예상외 raw 변경: PathID={pid} type={obj.type.name}")

    ok = True
    if script_mismatch:
        print(f"\n❌ m_Script 불일치: {script_mismatch}건 — 패치본이 손상됨!")
        ok = False
    else:
        print("\n✅ MonoBehaviour m_Script 전부 보존됨")

    if unexpected_raw:
        print(f"❌ 예상외 raw 변경: {unexpected_raw}건")
        ok = False
    else:
        print(f"✅ 의도된 변경만 존재 (TextAsset {expected_text}, 폰트/텍스처 {expected_font})")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
