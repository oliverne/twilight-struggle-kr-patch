#!/usr/bin/env python3
"""TextAsset 일괄 추출 도구 (읽기 전용)

용도: Unity 에셋 파일에서 모든 TextAsset의 본문을 추출해 파일로 저장.
원본/기존 패치 모두에서 사용. patch_textasset.py와 동일한 raw 레이아웃 사용.

사용법:
  extract_textassets.py <입력.assets> <출력디렉토리> [--names Name1,Name2,...]

옵션:
  --names  콤마로 구분된 TextAsset 이름 목록 (기본: 전체 추출)
  --list   TextAsset 이름/크기만 출력 후 종료

TextAsset raw 레이아웃:
  int32 name_len | name bytes | pad to 4 | int32 script_len | script bytes | pad to 4
"""
import os
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
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out_dir = sys.argv[2]
    names_filter = None
    list_only = False
    for arg in sys.argv[3:]:
        if arg == "--list":
            list_only = True
        elif arg.startswith("--names="):
            names_filter = set(arg[len("--names="):].split(","))

    env = UnityPy.load(src)
    found = 0
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw(obj.get_raw_data())
        if names_filter and name not in names_filter:
            continue
        size = len(script)
        if list_only:
            print(f"{obj.path_id}\t{size}\t{name}")
            found += 1
            continue
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{name}.txt")
        with open(path, "wb") as f:
            f.write(script)
        print(f"{size} 바이트 → {path}")
        found += 1

    if not found:
        print("추출된 TextAsset 없음")
        return 2
    print(f"총 {found}개 TextAsset")
    return 0


if __name__ == "__main__":
    sys.exit(main())