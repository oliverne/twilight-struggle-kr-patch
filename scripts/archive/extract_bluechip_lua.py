#!/usr/bin/env python3
"""블루칩 twilight_cards.lua에서 카드 정의 추출.

용도: Lua의 g_twilight_cards["이름"] 블록에서 card_name, card_number, event_text 등을
      추출해 영문 카드 식별자를 얻는다. 현재 원본 TS_Cards 영문과 카드별 매칭에 사용.

사용법:
  extract_bluechip_lua.py <입력.lua> <출력.json>

출력:
  { "cards": [ { "idx": int, "key": "Asia Scoring", "card_name": "...", "card_number": int, ... }, ... ] }
"""
import json
import re
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out_path = sys.argv[2]

    with open(src, encoding="utf-8") as f:
        text = f.read()

    cards = []
    # 패턴: g_twilight_cards["KEY"] = { ... }
    pattern = re.compile(
        r'g_twilight_cards\["([^"]+)"\]\s*=\s*\{(.*?)\n\}', re.DOTALL
    )
    for m in pattern.finditer(text):
        key = m.group(1)
        body = m.group(2)
        # card_name, card_number, card_type, stage, scoring_region 추출
        def field(name):
            mm = re.search(rf"{name}\s*=\s*\"(.*?)\"", body, re.DOTALL)
            return mm.group(1) if mm else None
        def numfield(name):
            mm = re.search(rf"{name}\s*=\s*(\d+)", body)
            return int(mm.group(1)) if mm else None
        # event_text는 .. 연결된 멀티라인 가능
        et = re.search(r'event_text\s*=\s*(.*?);\s*\n', body, re.DOTALL)
        event_text = None
        if et:
            raw = et.group(1)
            # "문자열" .. "문자열" 결합
            parts = re.findall(r'"((?:[^"\\]|\\.)*)"', raw)
            if parts:
                event_text = "".join(parts)

        cards.append({
            "idx": len(cards),
            "key": key,
            "card_name": field("card_name"),
            "card_number": numfield("card_number"),
            "card_type": field("card_type"),
            "stage": field("stage"),
            "scoring_region": field("scoring_region"),
            "event_text": event_text,
        })

    result = {"source": src, "card_count": len(cards), "cards": cards}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"카드 정의: {len(cards)}개 → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())