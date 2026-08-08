#!/usr/bin/env python3
"""검증된 런타임 번역 매칭을 TextAsset별 키 기반 번역 소스에 반영한다.

사용법:
  apply_runtime_matches.py <매칭.json> <strings.json> <cards.json>

EN 원문은 변경하지 않는다. 전체 문자열 일치가 검증된 행에만 `ko`와
`translation_source`를 추가하며, 기존 수동 번역은 덮어쓰지 않는다.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


RUNTIME_SOURCE = "runtime-20260315"


def runtime_translation(match):
    translations = {
        candidate["translation_ko"] for candidate in match["candidates"]
    }
    if len(translations) != 1:
        raise ValueError(
            f"{match['asset_name']} 행 {match['row']}에 번역 충돌이 있습니다."
        )
    return translations.pop()


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 1

    match_path, strings_path, cards_path = map(Path, sys.argv[1:])
    report = json.loads(match_path.read_text(encoding="utf-8"))
    matches_by_asset = defaultdict(dict)
    for match in report["matches"]:
        identity = (match["row"], match["key"])
        if identity in matches_by_asset[match["asset_name"]]:
            raise ValueError(f"중복 매칭: {match['asset_name']} {identity}")
        matches_by_asset[match["asset_name"]][identity] = match

    applied = 0
    for asset_path in (strings_path, cards_path):
        asset = json.loads(asset_path.read_text(encoding="utf-8"))
        asset_matches = matches_by_asset.pop(asset["asset_name"], {})
        seen = set()
        for row in asset["rows"]:
            identity = (row["row"], row["key"])
            source = row.get("translation_source")
            if source and source.get("source") == RUNTIME_SOURCE:
                row.pop("ko", None)
                row.pop("translation_source", None)

            match = asset_matches.get(identity)
            if not match:
                continue
            translation_ko = runtime_translation(match)
            if "ko" in row and row["ko"] != translation_ko:
                raise ValueError(
                    f"{asset['asset_name']} 행 {row['row']}의 기존 번역을 덮어쓸 수 없습니다."
                )
            row["ko"] = translation_ko
            row["translation_source"] = {
                "source": RUNTIME_SOURCE,
                "match_mode": match["match_mode"],
                "runtime_source_lines": [
                    candidate["source_line"] for candidate in match["candidates"]
                ],
            }
            seen.add(identity)
            applied += 1

        missing = set(asset_matches) - seen
        if missing:
            raise ValueError(f"{asset['asset_name']}에 없는 매칭 행: {sorted(missing)!r}")
        asset_path.write_text(
            json.dumps(asset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if matches_by_asset:
        raise ValueError(f"입력 파일이 없는 에셋 매칭: {sorted(matches_by_asset)!r}")
    if applied != report["summary"]["matched_count"]:
        raise ValueError(f"반영 수 불일치: {applied}")

    print(f"키 기반 번역 반영: {applied}행")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
