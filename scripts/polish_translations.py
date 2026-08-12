#!/usr/bin/env python3
"""humanizer 1차: 안전한 일괄 교정 스크립트.

원문(EN) 대조 후 안전하다고 판단된 번역투/AI 패턴만 규칙 기반 치환한다.
- EN 원문은 절대 수정하지 않는다 (ko/translation_ko 필드만)
- TMP 리치텍스트 태그 보존 (규칙은 태그 허용 정규식 사용 가능)
- 변경 전후 diff는 dist/polish-1.diff 로 저장

사용: python3 scripts/polish_translations.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRY_RUN = "--dry-run" in sys.argv

# (규칙명, 치환 전(str 또는 정규식 패턴), 치환 후, 근거)
RULES = [
    # --- A. 카드 규칙 피동 '~에 의해' → 조사/능동 (EN: cancelled/played by X) ---
    ("'악의 제국'에 의해 취소된다 → '으로'",
     "'악의 제국'에 의해 취소된다", "'악의 제국'으로 취소된다",
     "규칙서 피동 간결화: 받침 있는 명사는 '으로'"),
    ("#42 수렁에 의해 취소된다 → '으로'",
     "#42 수렁에 의해 취소된다", "#42 수렁으로 취소된다",
     "규칙서 피동 간결화"),
    ("'이 장벽을 허물어라'에 의해 사용할 수 없거나 → '로'",
     "'이 장벽을 허물어라'에 의해 사용할 수 없거나", "'이 장벽을 허물어라'로 사용할 수 없거나",
     "규칙서 피동 간결화: 받침 없는 명사는 '로'"),
    ('"이 장벽을 허물어라"에 의해 플레이 불가 → 로',
     '"이 장벽을 허물어라"에 의해 플레이 불가', '"이 장벽을 허물어라"로 플레이 불가',
     "규칙서 피동 간결화"),
    ("미국 플레이어에 의해 플레이되면 → 능동",
     "미국 플레이어에 의해 플레이되면", "미국 플레이어가 플레이하면",
     "EN 'played by the US player' — 능동태가 자연스러움"),
    ("이 카드가 미국 플레이어가 플레이하면 → 이 카드를",
     "이 카드가 미국 플레이어가 플레이하면", "이 카드를 미국 플레이어가 플레이하면",
     "이중 주격(카드가+플레이어가) 보정"),

    # --- B. 중국 카드 '가지고 있다' → '보유 중' (EN: has the China Card) ---
    ("중국 카드(태그 포함)를 가지고 있다면 → 보유 중이면",
     re.compile(r"(<i>)?중국 카드(</i>)?를 가지고 있다면"), r"\1중국 카드\2를 보유 중이면",
     "기존 번역 '보유 중인' 용어와 통일 (TMP <i> 태그 허용)"),
    ("이미 소련이 가지고 있다면 → 보유 중이면",
     "이미 소련이 가지고 있다면", "이미 소련이 보유 중이면",
     "위와 동일"),

    # --- C. 역사 서문 '~에 의해' 개별 치환 (능동태 전환) ---
    ("온건파에 의해 점점 소외된다고 느끼자 → 능동",
     "온건파에 의해 점점 소외된다고 느끼자", "온건파가 자신을 점점 소외시킨다고 느끼자",
     "EN 'marginalized by moderates' — 능동태 전환"),
    ("닉슨 대통령과 브레즈네프 서기장에 의해 완성된 → 능동",
     "닉슨 대통령과 브레즈네프 서기장에 의해 완성된", "닉슨 대통령과 브레즈네프 서기장이 완성한",
     "EN 'completed by Nixon and Brezhnev' — 능동태"),
    ("카터 대통령과 브레즈네프 서기장에 의해 완성되었다 → 능동",
     "카터 대통령과 브레즈네프 서기장에 의해 완성되었다", "카터 대통령과 브레즈네프 서기장이 완성했다",
     "EN 'completed by Carter and Brezhnev' — 능동태"),
    ("이슬람 과격파에 의해 암살되었다 → 에게",
     "이슬람 과격파에 의해 암살되었다", "이슬람 과격파에게 암살되었다",
     "인물 피동은 '에게'가 자연스러움"),
    ("민중 혁명에 의해 축출되었다 → 으로",
     "민중 혁명에 의해 축출되었다", "민중 혁명으로 축출되었다",
     "비인물 피동 '~으로'"),
    ("남성적 자아에 의해 추동되었다 → 능동",
     "남성적 자아에 의해 추동되었다", "남성적 자아가 추동했다",
     "EN 'driven by male ego' — 능동태"),
    ("한 플레이어에 의해 지배되거나 → 능동",
     "한 플레이어에 의해 <color=white>지배</color>되거나",
     "한 플레이어가 <color=white>지배</color>하거나",
     "EN 'controlled by one player' — 능동태"),
    ("주로 격전지에 의해 결정됩니다 → 능동",
     "주로 격전지에 의해 결정됩니다", "주로 격전지가 결정합니다",
     "EN 'driven by Battleground countries' — 능동태"),
    ("이벤트에 의해 배치가 요구되는 마커는 → 능동",
     "이벤트에 의해 배치가 요구되는 마커는", "이벤트가 배치를 요구하는 마커는",
     "EN 'placed when required by events' — 능동태"),

    # --- D. '~통해' 제거 (EN: through/via) — 태그 허용 정규식 ---
    ("지정학적 영향력을 통해 → 으로",
     re.compile(r"지정학적 영향력을 통해"), "지정학적 영향력으로",
     "EN 'through geographic influence' — '~으로' 간결화"),
    ("지리적 영향력을 통해 → 으로",
     re.compile(r"지리적 영향력을 통해"), "지리적 영향력으로",
     "동일"),
    ("이벤트 카드를 통해서도 → 으로도",
     "이벤트 카드를 통해서도", "이벤트 카드로도",
     "EN 'via Event Cards' — 간결화"),
    ("군사 쿠데타를 통해 권력을 장악했습니다 → 으로",
     "군사 쿠데타를 통해 권력을 장악했습니다", "군사 쿠데타로 권력을 장악했습니다",
     "EN 'via military coup' — 간결화"),
    ("임기라는 렌즈를 통해 평가됩니다 → 로",
     "임기라는 렌즈를 통해 평가됩니다", "임기라는 렌즈로 평가됩니다",
     "EN 'viewed through the lens' — '~로'가 자연스러움"),
    ("텔레비전 연설을 통해 미국 국민에게 → 로",
     "텔레비전 연설을 통해 미국 국민에게", "텔레비전 연설로 미국 국민에게",
     "EN 'in a live television address' — 간결화"),
    ("이를 통해 소련은 → 이로써",
     "이를 통해 소련은", "이로써 소련은",
     "'이를 통해' → '이로써' — 자연스러운 전환"),
    ("헌장 개정을 통해 → 으로",
     "헌장 개정을 통해", "헌장 개정으로",
     "EN 'through charter amendments' — 간결화"),
    ("공공 봉사 활동을 통해 → 으로",
     "공공 봉사 활동을 통해", "공공 봉사 활동으로",
     "EN 'through public service' — 간결화"),
    ("개인 설득을 통해 카터는 → 으로",
     "개인 설득을 통해 카터는", "개인 설득으로 카터는",
     "EN 'through direct personal appeal' — 간결화"),

    # --- E. '가지다' → '지니다/보유' ---
    ("온정주의적인 시각을 가지고 있었습니다 → 지니고",
     "온정주의적인 시각을 가지고 있었습니다", "온정주의적인 시각을 지니고 있었습니다",
     "문어체 '지니다'가 자연스러움"),
    ("얼마나 많은 영향력을 가지고 있는지에 따라 → 보유하고",
     "얼마나 많은 영향력을 가지고 있는지에 따라", "얼마나 많은 영향력을 보유하고 있는지에 따라",
     "EN 'how much influence each superpower has' — '보유'가 정확"),
    ("얼마나 영향력을 가지고 있는지에 따라 → 보유하고",
     "얼마나 영향력을 가지고 있는지에 따라", "얼마나 영향력을 보유하고 있는지에 따라",
     "동일"),

    # --- F. '~에 대해' 직역 (카드 규칙) ---
    ("각각에 대해 1씩 뺍니다 → 각각 1씩",
     "각각에 대해 1씩 뺍니다", "각각 1씩 뺍니다",
     "EN 'subtract 1 for each...' — 'for each' 직역 제거"),

    # --- G. 조사 받침 불일치 (grammar-checker 2026-08-12 검출, TMP 태그 허용) ---
    ("격전지을(태그 허용) → 격전지를",
     re.compile(r"격전지(</?[^>]+>)?을"), r"격전지\1를",
     "받침 없는 '지' + '을' → '를' (조사 불일치)"),
    ("비격전지과(태그 허용) → 비격전지와",
     re.compile(r"비격전지(</?[^>]+>)?과"), r"비격전지\1와",
     "받침 없는 '지' + '과' → '와' (조사 불일치)"),
    ("승점를(태그 허용) → 승점을",
     re.compile(r"승점(</?[^>]+>)?를"), r"승점\1을",
     "받침 있는 '점' + '를' → '을' (조사 불일치)"),
    ("작전치을(태그 허용) → 작전치를",
     re.compile(r"작전치(</?[^>]+>)?을"), r"작전치\1를",
     "받침 없는 '치' + '을' → '를' (조사 불일치)"),
]

# 대상 파일: (경로, [문자열 필드명들])
TARGETS = [
    (ROOT / "translation" / "cards.json", ["ko"]),
    (ROOT / "translation" / "strings.json", ["ko"]),
    (ROOT / "translation" / "runtime-20260315.json", ["translation_ko"]),
    (ROOT / "translation" / "manual-extra.json", ["__all__"]),    # dict 값 전체
    (ROOT / "translation" / "manual-scenes.json", ["__manual__"]),  # manual dict 값 전체
]


def walk_strings(obj, field, out):
    """JSON 트리에서 대상 문자열 필드를 수집."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if field == "__all__" and isinstance(v, str) and k not in ("$schema", "description"):
                out.append(v)
            elif field == "__manual__" and k == "manual" and isinstance(v, dict):
                out.extend(v.values())
            elif k == field and isinstance(v, str):
                out.append(v)
            elif isinstance(v, (dict, list)):
                walk_strings(v, field, out)
    elif isinstance(obj, list):
        for item in obj:
            walk_strings(item, field, out)


def apply_rules(text):
    """규칙 적용. (새 텍스트, 적용된 규칙 카운트 dict)"""
    new_text = text
    applied = {}
    for name, old, new, why in RULES:
        if isinstance(old, re.Pattern):
            if old.search(new_text):
                new_text = old.sub(new, new_text)
                applied[name] = applied.get(name, 0) + 1
        else:
            if old in new_text:
                new_text = new_text.replace(old, new)
                applied[name] = applied.get(name, 0) + 1
    return new_text, applied


def replace_in_tree(obj, old_text, new_text):
    """JSON 트리의 모든 문자열에서 old_text → new_text 교체."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v == old_text:
                obj[k] = new_text
            elif isinstance(v, (dict, list)):
                replace_in_tree(v, old_text, new_text)
    elif isinstance(obj, list):
        for item in obj:
            replace_in_tree(item, old_text, new_text)


def main():
    total = 0
    applied_total = {}
    diff_lines = []
    for path, fields in TARGETS:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for field in fields:
            strings = []
            walk_strings(data, field, strings)
            for text in strings:
                new_text, applied = apply_rules(text)
                if new_text != text:
                    total += 1
                    for name, cnt in applied.items():
                        applied_total[name] = applied_total.get(name, 0) + cnt
                    diff_lines.append(f"--- {path.name} [{field}]")
                    diff_lines.append(f"- {text[:200]}")
                    diff_lines.append(f"+ {new_text[:200]}")
                    if not DRY_RUN:
                        replace_in_tree(data, text, new_text)
        if not DRY_RUN:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"변경된 문자열: {total}개")
    print("규칙별 적용 수:")
    for name, cnt in sorted(applied_total.items(), key=lambda kv: -kv[1]):
        print(f"  {cnt:3d}  {name}")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "polish-1.diff").write_text("\n".join(diff_lines), encoding="utf-8")
    print(f"\ndiff: dist/polish-1.diff ({len(diff_lines)}줄)")


if __name__ == "__main__":
    main()
