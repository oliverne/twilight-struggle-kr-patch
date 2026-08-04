#!/usr/bin/env python3
"""TextAsset 문자열 치환 도구 (UnityPy raw 편집 기반)

용도: Unity 에셋 파일 내 TextAsset의 본문을 문자열 치환해 새 파일로 저장.
주의 1: 출력 파일명은 입력과 동일해야 함 (UnityPy가 원본 파일명으로 저장).
주의 2: UnityPy가 자신이 저장한 파일을 다시 읽어 저장하면 데이터가 유실됨
        (확인됨). 반드시 원본 파일에서 한 번에 모든 치환을 적용할 것.

사용법:
  patch_textasset.py <입력.assets> <출력.assets> <TextAsset이름> <찾을문자열> <바꿀문자열> [<TextAsset이름> <찾을문자열> <바꿀문자열> ...]

TextAsset raw 레이아웃:
  int32 name_len | name bytes | pad to 4 | int32 script_len | script bytes | pad to 4

검증: 치환 횟수를 출력하고, 하나라도 0회면 실패 종료(코드 2).
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


def build_raw(name: str, script: bytes) -> bytes:
    name_b = name.encode("utf-8")
    out = struct.pack("<i", len(name_b)) + name_b
    out += b"\x00" * pad4(len(out))
    out += struct.pack("<i", len(script)) + script
    out += b"\x00" * pad4(len(script))
    return out


def main() -> int:
    if len(sys.argv) < 6 or (len(sys.argv) - 2) % 3 != 0:
        print(__doc__)
        return 1
    src, dst = sys.argv[1:3]
    jobs = []
    for i in range(3, len(sys.argv), 3):
        jobs.append(sys.argv[i : i + 3])  # (asset_name, old, new)

    dst_dir = os.path.dirname(os.path.abspath(dst)) or "."
    if os.path.basename(dst) != os.path.basename(src):
        print("출력 파일명은 입력과 동일해야 합니다 (UnityPy 제약)")
        return 1
    os.makedirs(dst_dir, exist_ok=True)

    env = UnityPy.load(src)
    pending = {i: list(job) for i, job in enumerate(jobs)}  # 남은 치환
    edited = {}  # asset_name -> 변경된 text

    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw(obj.get_raw_data())
        text = script.decode("utf-8")
        changed = False
        for i in list(pending):
            asset_name, old, new = pending[i]
            if asset_name != name:
                continue
            count = text.count(old)
            if count == 0:
                print(f"'{old}' 발견되지 않음 (TextAsset: {asset_name})")
                return 2
            text = text.replace(old, new)
            print(f"치환 {count}회: {asset_name} / {old[:40]}")
            del pending[i]
            changed = True
        if changed:
            obj.set_raw_data(build_raw(name, text.encode("utf-8")))
            obj.mark_changed()

    if pending:
        print(f"미적용 치환 {len(pending)}개 — TextAsset 미존재 또는 문자열 없음")
        return 2

    env.save("none", dst_dir)
    print(f"저장 완료 → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
