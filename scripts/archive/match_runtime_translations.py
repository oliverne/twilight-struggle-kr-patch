#!/usr/bin/env python3
"""현재 TextAsset 영문 행과 런타임 패치 번역을 전체 문자열로 매칭한다.

사용법:
  match_runtime_translations.py <runtime.json> <strings.json> <cards.json> <출력.json>

원문 전체가 같은 경우만 매칭한다. 런타임 TSV가 보존한 \\n, \\r, \\t,
\\\\, \\" 이스케이프를 한 번 해석한 전체 문자열도 보조 비교한다. 부분 문자열
치환이나 유사도 비교는 하지 않는다.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def unescape_runtime(value):
    """런타임 플러그인이 해석하는 범위의 이스케이프만 변환한다."""
    escapes = {
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "\\": "\\",
        '"': '"',
    }
    result = []
    index = 0
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            escaped = escapes.get(value[index + 1])
            if escaped is not None:
                result.append(escaped)
                index += 2
                continue
        result.append(char)
        index += 1
    return "".join(result)


def index_entries(entries, transform):
    indexed = defaultdict(list)
    for entry in entries:
        indexed[transform(entry["original"])].append(entry)
    return indexed


def candidate_translations(entries):
    return list(dict.fromkeys(entry["translation_ko"] for entry in entries))


def serialize_candidate(entry):
    return {
        "source_line": entry["source_line"],
        "original_raw": entry["original"],
        "translation_ko_raw": entry["translation_ko"],
        "translation_ko": unescape_runtime(entry["translation_ko"]),
    }


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        return 1

    runtime_path, strings_path, cards_path, output_path = map(Path, sys.argv[1:])
    runtime_entries = json.loads(runtime_path.read_text(encoding="utf-8"))["entries"]
    current_assets = [
        json.loads(strings_path.read_text(encoding="utf-8")),
        json.loads(cards_path.read_text(encoding="utf-8")),
    ]
    raw_index = index_entries(runtime_entries, lambda value: value)
    unescaped_index = index_entries(runtime_entries, unescape_runtime)

    matches = []
    ambiguous = []
    unmatched = []
    for asset in current_assets:
        for row in asset["rows"]:
            if row["en"] == "EN":
                continue
            current = {
                "asset_name": asset["asset_name"],
                "row": row["row"],
                "key": row["key"],
                "en": row["en"],
            }
            candidates = raw_index.get(row["en"], [])
            match_mode = "exact"
            if not candidates:
                candidates = unescaped_index.get(row["en"], [])
                match_mode = "runtime_escape_decoded"

            translations = candidate_translations(candidates)
            if not candidates:
                unmatched.append(current)
            elif len(translations) > 1:
                ambiguous.append(
                    {
                        **current,
                        "match_mode": match_mode,
                        "candidates": [serialize_candidate(entry) for entry in candidates],
                    }
                )
            else:
                matches.append(
                    {
                        **current,
                        "match_mode": match_mode,
                        "candidates": [serialize_candidate(entry) for entry in candidates],
                    }
                )

    summary = {
        "current_row_count": len(matches) + len(ambiguous) + len(unmatched),
        "matched_count": len(matches),
        "exact_match_count": sum(
            match["match_mode"] == "exact" for match in matches
        ),
        "runtime_escape_decoded_match_count": sum(
            match["match_mode"] == "runtime_escape_decoded" for match in matches
        ),
        "ambiguous_count": len(ambiguous),
        "unmatched_count": len(unmatched),
    }
    result = {
        "sources": {
            "runtime": runtime_path.as_posix(),
            "current_assets": [strings_path.as_posix(), cards_path.as_posix()],
        },
        "matching_rule": "원문 전체 일치만 허용; 런타임 이스케이프 1회 해석은 별도 모드로 기록",
        "summary": summary,
        "matches": matches,
        "ambiguous": ambiguous,
        "unmatched": unmatched,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"현재 행: {summary['current_row_count']}")
    print(f"완전 일치: {summary['exact_match_count']}")
    print(f"이스케이프 해석 일치: {summary['runtime_escape_decoded_match_count']}")
    print(f"번역 충돌: {summary['ambiguous_count']}")
    print(f"미일치: {summary['unmatched_count']}")
    print(f"→ {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
