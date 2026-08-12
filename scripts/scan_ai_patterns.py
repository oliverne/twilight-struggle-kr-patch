#!/usr/bin/env python3
"""humanizer 기반 번역 AI 패턴 스캐너.

translation/*.json 의 한국어 번역에서 AI 작문 마커(humanizer 스킬 40패턴 중
기계 검출 가능한 것)를 정규식으로 1차 필터링한다.
용도: 심층 수동 검토(humanizer)가 필요한 의심 항목 우선순위화.

사용: python3 scripts/scan_ai_patterns.py
출력: dist/ai-pattern-scan.md (또는 stdout)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSLATION = ROOT / "translation"

# ---- TMP 리치텍스트 태그 제거 ----
TAG_RE = re.compile(r"<[^>]+>")

# ---- 패턴 정의: (이름, 심각도, 정규식, 설명) ----
PATTERNS = [
    # --- 번역투 (S1~S2) ---
    ("피동 남용 '~되어지다'", "S1", re.compile(r"되어지"), "이중 피동 — 무조건 의심"),
    ("피동 남용 '에 의해'", "S2", re.compile(r"(에 의해|으로 인해|로 인해)"), "영어 by/owing to 직역"),
    ("조사 번역투 '~에 대해'", "S2", re.compile(r"에 대해(서)?[는]? "), "영어 about/regarding 직역"),
    ("조사 번역투 '~에 있어'", "S2", re.compile(r"에 있어"), "in terms of 직역"),
    ("조사 번역투 '~통해'", "S2", re.compile(r"(을|를|을/를) 통해"), "through 직역"),
    ("조사 번역투 '~으로써/로서'", "S3", re.compile(r"으로써|로서"), "as/with 직역"),
    ("동사 잉여 '가지고 있다'", "S2", re.compile(r"가지고 있"), "have 직역 — '~을 지니다/보유하다'"),
    ("동사 잉여 '~해지고 있다'", "S2", re.compile(r"(되고 있|해지고 있|돼지고 있)"), "becoming 직역"),
    ("가능 표현 남발 '할 수 있'", "S3", re.compile(r"할 수 있"), "can 직역 — 빈도 기반 판정"),
    ("미래 단정 '~것이다'", "S3", re.compile(r"것입니다|것이야|것이다"), "will be 단정 — 빈도 기반"),
    ("의존명사 '것으로'", "S3", re.compile(r"것으로 (판단|생각|예상|간주|여겨|보이|나타)"), "~것으로 보인다 직역"),
    ("명사화 '-음/-기' 체인", "S3", re.compile(r"(함으로|됨으로|함에 따라|됨에 따라)"), "명사화 남용"),
    # --- AI 유행어 (S2) ---
    ("AI 유행어 '중요하'", "S2", re.compile(r"중요(하|한|합)"), "중요하다 남용"),
    ("AI 유행어 '핵심'", "S2", re.compile(r"핵심"), "핵심 남용"),
    ("AI 유행어 '효과적'", "S2", re.compile(r"효과적"), "효과적 남용"),
    ("AI 유행어 '최적'", "S2", re.compile(r"최적"), "최적 남용"),
    ("AI 유행어 '혁신'", "S3", re.compile(r"혁신"), "혁신 남용"),
    ("AI 유행어 '지속'", "S3", re.compile(r"지속적"), "지속적 남용"),
    ("hype 어휘 '완벽'", "S3", re.compile(r"완벽"), "완벽/완벽한 남용"),
    # --- 구조/문장부호 (S2~S3) ---
    ("쉼표 과다 (문장 내 3+개)", "S2", re.compile(r"^[^,。]*,[^,。]*,[^,。]*,[^,。]*$", re.M), "쉼표 3개 이상"),
    ("~적 N 추상 체인", "S3", re.compile(r"[가-힣]+적 [가-힣]{2,}"), "~적 + 명사 추상 체인"),
    ("복수형 '-들' 반복 (문장 내 2+개)", "S3", re.compile(r"^[^,。]*들[^,。]*들", re.M), "'들' 2회 이상"),
    # --- 영어 직역 어휘 (S3) ---
    ("영어 직역 '경우'", "S3", re.compile(r"의 경우(에)? "), "case 직역 — 문맥 판단 필요"),
    ("영어 직역 '수준'", "S3", re.compile(r"수준의"), "level 직역"),
]

# 번역 소스 수집: (파일명, 라벨, [(id, 원문, 번역)])
def collect():
    out = []
    # strings.json / cards.json
    for f, label in [("strings.json", "Common_Strings"), ("cards.json", "TS_Cards")]:
        p = TRANSLATION / f
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        for row in d.get("rows", []):
            en, ko = row.get("en", ""), row.get("ko", "")
            if ko:
                pid = f"{label} row{row.get('row')} [{row.get('key','')}]"
                out.append((pid, label, en, ko))
    # runtime TSV
    p = TRANSLATION / "runtime-20260315.json"
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        for e in d.get("entries", []):
            ko = e.get("translation_ko")
            if ko:
                out.append((f"runtime L{e.get('source_line')}", "runtime", e.get("original", ""), ko))
    # manual-extra / manual-scenes
    p = TRANSLATION / "manual-extra.json"
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        for grp in ("TS_Ingame", "TS_Strings"):
            for en, ko in d.get(grp, {}).items():
                if ko:
                    out.append((f"manual-extra {grp}", grp, en, ko))
    p = TRANSLATION / "manual-scenes.json"
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        for i, (en, ko) in enumerate(d.get("manual", {}).items()):
            if ko:
                out.append((f"manual-scenes #{i}", "manual-scenes", en, ko))
    return out


def main():
    items = collect()
    print(f"총 번역 항목: {len(items)}")
    hits = []
    for pid, label, en, ko in items:
        ko_plain = TAG_RE.sub("", ko)
        for name, sev, rx, desc in PATTERNS:
            for m in rx.finditer(ko_plain):
                start = max(0, m.start() - 18)
                end = min(len(ko_plain), m.end() + 18)
                ctx = ko_plain[start:end].replace("\n", " ")
                hits.append((sev, name, pid, ctx, en, ko))
    hits.sort(key=lambda h: (h[0], h[1]))
    # 요약
    from collections import Counter
    sev_cnt = Counter(h[0] for h in hits)
    print(f"검출: S1 {sev_cnt['S1']}건 / S2 {sev_cnt['S2']}건 / S3 {sev_cnt['S3']}건 / 총 {len(hits)}건")
    print(f"영향 항목 수: {len(set(h[2] for h in hits))}")
    print()
    # 패턴별 상위 15건만 상세 출력
    by_pat = {}
    for h in hits:
        by_pat.setdefault(h[1], []).append(h)
    for name, hs in sorted(by_pat.items(), key=lambda kv: -len(kv[1])):
        print(f"### [{hs[0][0]}] {name} — {len(hs)}건")
        for h in hs[:8]:
            print(f"  - {h[2]}: …{h[3]}…")
        if len(hs) > 8:
            print(f"  - … 외 {len(hs)-8}건")
        print()


if __name__ == "__main__":
    main()
