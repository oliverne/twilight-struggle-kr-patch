#!/usr/bin/env python3
"""번역 소스에서 사용 글자 문자셋을 추출한다.

translation/strings.json, translation/cards.json의 모든 ko 필드에서
고유 문자를 추출해 fonts/chars.txt로 저장한다.
한글 음절, 영문, 숫자, TMP 태그용 특수문자(<, >, =, ", #, /)를 포함한다.
"""

import json
import sys
from pathlib import Path


def extract_chars(data: dict) -> set[str]:
    chars = set()
    for row in data.get("rows", []):
        ko = row.get("ko", "")
        if ko:
            for ch in ko:
                chars.add(ch)
    return chars


def main():
    base = Path(__file__).resolve().parent.parent

    strings_path = base / "translation/strings.json"
    cards_path = base / "translation/cards.json"
    output_path = base / "fonts/chars.txt"

    if not strings_path.exists():
        print(f"ERROR: {strings_path} not found", file=sys.stderr)
        return 1
    if not cards_path.exists():
        print(f"ERROR: {cards_path} not found", file=sys.stderr)
        return 1

    strings = json.loads(strings_path.read_text("utf-8"))
    cards = json.loads(cards_path.read_text("utf-8"))

    all_chars = extract_chars(strings) | extract_chars(cards)

    # TMP 리치텍스트 태그 보존에 필요한 필수 문자 추가
    extra = set('<>="/#\\{}[]:;.,!?\'\"()-+*&%$@^~`| \n\r\t\u00a0')
    all_chars |= extra

    # 정렬해서 저장
    sorted_chars = "".join(sorted(all_chars))

    # 한글, 비한글 분류 통계
    hangul = [c for c in sorted_chars if "\uac00" <= c <= "\ud7a3"]
    non_hangul = [c for c in sorted_chars if not ("\uac00" <= c <= "\ud7a3")]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(sorted_chars, encoding="utf-8")

    # Unity_Font_Replacer/make_sdf.py 호환 헤더 없는 chars.txt
    print(f"총 고유 문자: {len(sorted_chars)}")
    print(f"  한글 음절: {len(hangul)}")
    print(f"  기타 (영문/숫자/특수문자 등): {len(non_hangul)}")
    print(f"→ {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
