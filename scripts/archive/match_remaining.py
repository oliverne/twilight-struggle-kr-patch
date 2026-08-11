#!/usr/bin/env python3
"""미일치 TextAsset 행을 런타임 TSV 및 블루칩 번역과 매칭한다.

전략:
  1. TS_Cards 카드 제목: 런타임 TSV에서 카드 제목(끝에 * 붙은 패턴)과 매칭
  2. TS_Cards 카드 설명: 런타임 TSV의 동일 설명과 매칭
  3. Common_Strings: 기본 UI 문자열 — 런타임 TSV에 없으므로 매뉴얼 번역 대상
  4. 블루칩 v1.0.1 한글도 보조 검증용으로 확인

사용법:
  match_remaining.py <runtime.json> <matches.json> <bluechip.json> <strings.json> <cards.json> <출력.json>
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def unescape_runtime(value):
    escapes = {
        "n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"',
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


def normalize_card_title(title: str) -> str:
    """카드 제목 정규화: *, 공백, 대소문자 무시"""
    t = title.strip().rstrip("*").strip()
    return t


def load_runtime_index(runtime_path: Path) -> dict:
    """런타임 TSV를 여러 인덱스로 변환"""
    entries = json.loads(runtime_path.read_text(encoding="utf-8"))["entries"]
    
    exact = {}
    unescaped = {}
    card_titles = {}  # 카드 제목만 (끝에 * 붙은 항목)
    
    for e in entries:
        orig = e["original"]
        exact[orig] = e
        
        unesc = unescape_runtime(orig)
        unescaped[unesc] = e
        
        # 카드 제목 패턴: "이름*" 또는 "이름\n이름*"
        if orig.endswith("*") or unesc.endswith("*"):
            title = normalize_card_title(unesc)
            if title and len(title) >= 3:
                card_titles[title.lower()] = e
                # 줄바꿈 변형도 저장
                title_one_line = title.replace("\n", " ")
                if title_one_line != title.lower():
                    card_titles[title_one_line] = e
    
    return {"exact": exact, "unescaped": unescaped, "card_titles": card_titles}


def load_bluechip_index(bluechip_path: Path) -> dict:
    """블루칩 한글 문자열을 키로 하는 인덱스"""
    bc = json.loads(bluechip_path.read_text(encoding="utf-8"))
    return bc.get("unique_texts", {})


def match_tscards(unmatched: list, rt_index: dict, bc_kr: dict) -> list:
    """TS_Cards 미일치 행 매칭"""
    results = []
    
    for row in unmatched:
        en = row["en"]
        key = row["key"]
        found = None
        method = "none"
        
        # 1. 직접 exact 매칭
        if en in rt_index["exact"]:
            found = rt_index["exact"][en]
            method = "exact"
        elif en in rt_index["unescaped"]:
            found = rt_index["unescaped"][en]
            method = "exact_unesc"
        
        # 2. 카드 제목 매칭 (Title, Title1, Title2 등)
        if not found and ("Title" in key):
            normalized = normalize_card_title(en).lower()
            if normalized in rt_index["card_titles"]:
                found = rt_index["card_titles"][normalized]
                method = "card_title"
            elif normalized.strip().replace("\n", " ") in rt_index["card_titles"]:
                found = rt_index["card_titles"][normalized.strip().replace("\n", " ")]
                method = "card_title"
        
        # 3. 부분 매칭 (카드 설명이 더 큰 런타임 항목에 포함된 경우 — 신중하게)
        if not found and len(en) > 30 and ("Text" in key or "Text" in key):
            # 긴 텍스트만 부분 매칭 시도
            for rt_orig, rt_entry in rt_index["exact"].items():
                if en in rt_orig and len(en) > len(rt_orig) * 0.60:
                    found = rt_entry
                    method = "substring_long"
                    break
        
        result = {
            "asset_name": row["asset_name"],
            "row": row["row"],
            "key": key,
            "en": en,
            "method": method,
        }
        
        if found:
            result["translation_ko"] = (
                found.get("translation_ko_raw") or found["translation_ko"]
            )
            result["matched_original"] = found["original"]
            result["source_line"] = found.get("source_line")
        else:
            result["translation_ko"] = None
            result["matched_original"] = None
            result["source_line"] = None
        
        results.append(result)
    
    return results


def main():
    if len(sys.argv) != 7:
        print(__doc__)
        return 1
    
    runtime_path, matches_path, bluechip_path, strings_path, cards_path, output_path = map(Path, sys.argv[1:])
    
    # 데이터 로드
    rt_index = load_runtime_index(runtime_path)
    bc_kr = load_bluechip_index(bluechip_path)
    
    with open(matches_path) as f:
        match_data = json.load(f)
    
    unmatched_cards = [u for u in match_data["unmatched"] if u["asset_name"] == "TS_Cards"]
    unmatched_strings = [u for u in match_data["unmatched"] if u["asset_name"] == "Common_Strings"]
    
    print(f"TS_Cards 미일치: {len(unmatched_cards)}")
    print(f"Common_Strings 미일치: {len(unmatched_strings)}")
    
    # TS_Cards 매칭
    card_results = match_tscards(unmatched_cards, rt_index, bc_kr)
    
    # 집계
    methods = defaultdict(int)
    found_count = 0
    for r in card_results:
        methods[r["method"]] += 1
        if r["translation_ko"]:
            found_count += 1
    
    print(f"\nTS_Cards 매칭 결과:")
    for method, count in sorted(methods.items()):
        print(f"  {method}: {count}")
    print(f"  번역 있음: {found_count}/{len(card_results)}")
    
    # Common_Strings는 런타임 TSV에 없으므로 수동 번역 대상으로 표시
    cs_results = []
    for row in unmatched_strings:
        cs_results.append({
            "asset_name": row["asset_name"],
            "row": row["row"],
            "key": row["key"],
            "en": row["en"],
            "method": "manual_needed",
            "translation_ko": None,
            "matched_original": None,
            "source_line": None,
        })
    
    # 결과 저장
    output = {
        "tscards_results": card_results,
        "common_strings_results": cs_results,
        "summary": {
            "tscards_total": len(card_results),
            "tscards_matched": found_count,
            "tscards_unmatched": len(card_results) - found_count,
            "common_strings_total": len(cs_results),
            "common_strings_manual_needed": len(cs_results),
        },
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    
    print(f"\nCommon_Strings: {len(cs_results)}행 모두 수동 번역 필요")
    print(f"→ {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
