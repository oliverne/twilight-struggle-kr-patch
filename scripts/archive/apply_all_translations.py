#!/usr/bin/env python3
"""Phase 2 최종: 모든 번역을 strings.json, cards.json에 반영한다.

1. 기존 런타임 TSV 매칭 결과 반영 (341행)
2. 추가 매칭 결과 반영 (card_title, substring 등)
3. 수동 확장 매칭 (prefix/quotes/format 차이 보정)
4. EN-KO 맵 기반 매칭

출력: strings.json, cards.json (ko 필드 추가)
"""

import json
import sys
from pathlib import Path


def unescape_runtime(value):
    escapes = {"n": "\n", "r": "\r", "t": "\t", "\\": "\\", '"': '"'}
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


def build_rt_index(entries):
    """런타임 TSV 엔트리를 exact, unescaped, lowered 인덱스로"""
    exact = {}
    unesc = {}
    for e in entries:
        orig = e["original"]
        exact[orig] = e
        u = unescape_runtime(orig)
        if u != orig:
            unesc[u] = e
    return exact, unesc


def get_translation(entry):
    return entry.get("translation_ko_raw") or entry["translation_ko"]


def main():
    base = Path(__file__).resolve().parent.parent.parent

    # ── 로드 ──
    rt_entries = json.loads(
        (base / "translation/runtime-20260315.json").read_text("utf-8")
    )["entries"]
    rt_exact, rt_unesc = build_rt_index(rt_entries)

    matches = json.loads(
        (base / "translation/runtime-20260315-matches.json").read_text("utf-8")
    )
    remaining = json.loads(
        Path("/tmp/remaining-matches.json").read_text("utf-8")
    )

    strings = json.loads(
        (base / "translation/strings.json").read_text("utf-8")
    )
    cards = json.loads(
        (base / "translation/cards.json").read_text("utf-8")
    )

    # ── EN → KO 매핑 (확장) ──
    # prefix/quotes/format 차이를 보정하는 추가 매핑
    en_to_ko_extra = {}

    for e in rt_entries:
        ko = get_translation(e)
        orig = e["original"]
        uorig = unescape_runtime(orig)

        # "+1 " prefix 없는 버전도 매핑
        for prefix in ["+1 ", "+2 ", "1 ", "- "]:
            if orig.startswith(prefix):
                en_to_ko_extra[orig[len(prefix):]] = ko
            if uorig.startswith(prefix):
                en_to_ko_extra[uorig[len(prefix):]] = ko

        # 따옴표 버전
        if orig.startswith('"') and orig.endswith('*'):
            stripped = orig.strip('"')
            en_to_ko_extra[stripped] = ko

        # <font="TIMESI SDF"> → <i> 변환
        if '<font="TIMESI SDF">' in orig:
            alt = orig.replace('<font="TIMESI SDF">', '<i>').replace('</font>', '</i>')
            en_to_ko_extra[alt] = ko

    # 수동 추가 매핑
    manual_en_ko = {
        "Special": "특수",
        "Optional": "선택 규칙",
        "VPs for Control of Thailand": "태국 지배 시 2VP",
        "VP each for Control of: Burma, Cambodia/Laos, Vietnam, Malaysia, Indonesia, the Philippines.":
            "버마·캄보디아/라오스·베트남·말레이시아·인도네시아·필리핀을 지배할 때마다 1 승점",
        "Shuttle": "셔틀",
    }
    en_to_ko_extra.update(manual_en_ko)

    # ── 매칭 함수 ──
    def find_ko(en_text):
        # 1. exact
        if en_text in rt_exact:
            return get_translation(rt_exact[en_text]), "exact"
        # 2. unescaped
        if en_text in rt_unesc:
            return get_translation(rt_unesc[en_text]), "exact_unesc"
        # 3. 확장 매핑
        if en_text in en_to_ko_extra:
            return en_to_ko_extra[en_text], "extra_map"
        return None, "none"

    # ── 적용 ──
    stats = {"applied": 0, "already_had": 0, "failed": 0}

    def apply_to_asset(asset_data, asset_name):
        rows = asset_data["rows"]
        for row in rows:
            key = row["key"]
            en = row["en"]
            if en == "EN":
                continue

            # 이미 ko가 있는지 확인
            if row.get("ko"):
                stats["already_had"] += 1
                continue

            ko, method = find_ko(en)
            if ko:
                row["ko"] = ko
                row["ko_source"] = method
                stats["applied"] += 1
            else:
                stats["failed"] += 1
                if stats["failed"] <= 10:
                    print(f"  [MISS] {asset_name} {key}: \"{en[:60]}\"")

    apply_to_asset(strings, "Common_Strings")
    apply_to_asset(cards, "TS_Cards")

    # ── 저장 ──
    (base / "translation/strings.json").write_text(
        json.dumps(strings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (base / "translation/cards.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\n=== 최종 결과 ===")
    print(f"이미 ko 있음: {stats['already_had']}")
    print(f"새로 적용: {stats['applied']}")
    print(f"실패 (수동 번역 필요): {stats['failed']}")
    print(f"커버리지: {(stats['already_had'] + stats['applied'])} / {(stats['already_had'] + stats['applied'] + stats['failed'])} ({(stats['already_had'] + stats['applied']) / (stats['already_had'] + stats['applied'] + stats['failed']) * 100:.1f}%)")
    print(f"\n→ translation/strings.json")
    print(f"→ translation/cards.json")


if __name__ == "__main__":
    main()
