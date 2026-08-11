#!/usr/bin/env python3
"""신규 런타임 한글 패치의 원문-번역 TSV를 비교용 JSON으로 추출한다.

용도:
  Windows 전용 BepInEx 배포본 자체를 포팅하지 않고, 함께 제공된
  runtime_exact.tsv의 영문 원문과 한글 번역을 Phase 2의 번역 재사용
  소스로 보존한다. 입력의 행 순서와 중복 원문을 유지한다.

사용법:
  extract_runtime_tsv.py <입력.tsv> <출력.json>

주의:
  TSV 안의 \\n+ 같은 이스케이프 표기는 런타임 패치가 해석하는 원문 그대로 보존한다.
  이 스크립트는 이를 실제 줄바꿈으로 변환하지 않는다.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple


HEADER = ("original_text", "translation_ko")


def parse_row(line: str, line_number: int) -> Tuple[str, str, Optional[str]]:
    """TSV 행을 읽고, 탭 누락 시 기존 배포본의 공백 구분 한 행을 복구한다."""
    cells = line.split("\t")
    if len(cells) == 2:
        return cells[0], cells[1], None

    if len(cells) == 1:
        fallback = re.split(r" {2,}", line, maxsplit=1)
        if len(fallback) == 2:
            return fallback[0], fallback[1], "space-delimited fallback"

    raise ValueError(f"{line_number}행을 원문/번역 두 셀로 해석할 수 없습니다.")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    source_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    lines = source_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise ValueError("입력 파일이 비어 있습니다.")

    header = tuple(lines[0].split("\t"))
    if header != HEADER:
        raise ValueError(f"예상 헤더 {HEADER!r}와 다릅니다: {header!r}")

    entries = []
    parsing_notes = []
    by_original: dict[str, list[dict[str, object]]] = defaultdict(list)
    for line_number, line in enumerate(lines[1:], start=2):
        original, translation_ko, note = parse_row(line, line_number)
        if not original or not translation_ko:
            raise ValueError(f"{line_number}행에 빈 원문 또는 번역이 있습니다.")

        entry = {
            "source_line": line_number,
            "original": original,
            "translation_ko": translation_ko,
        }
        entries.append(entry)
        by_original[original].append(entry)
        if note:
            parsing_notes.append({"source_line": line_number, "note": note})

    duplicate_originals = {
        original: [entry["source_line"] for entry in grouped]
        for original, grouped in by_original.items()
        if len(grouped) > 1
    }
    conflicting_duplicates = {
        original: {
            "source_lines": [entry["source_line"] for entry in grouped],
            "translations_ko": list(
                dict.fromkeys(entry["translation_ko"] for entry in grouped)
            ),
        }
        for original, grouped in by_original.items()
        if len({entry["translation_ko"] for entry in grouped}) > 1
    }

    result = {
        "source": source_path.as_posix(),
        "format": "runtime_exact.tsv",
        "entry_count": len(entries),
        "raw_escape_sequences_preserved": True,
        "entries": entries,
        "diagnostics": {
            "parsing_notes": parsing_notes,
            "duplicate_original_count": len(duplicate_originals),
            "duplicate_originals": duplicate_originals,
            "conflicting_duplicates": conflicting_duplicates,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"추출 행: {len(entries)}")
    print(f"중복 원문: {len(duplicate_originals)}")
    print(f"번역 충돌 원문: {len(conflicting_duplicates)}")
    print(f"파싱 보정 행: {len(parsing_notes)}")
    print(f"→ {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
