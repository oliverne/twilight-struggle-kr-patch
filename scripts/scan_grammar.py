#!/usr/bin/env python3
"""grammar-checker 기반 번역 맞춤법/문법 스캐너.

translation/*.json 의 한국어 번역에서 아래를 정규식으로 1차 필터링한다:
- 우선순위 1: 맞춤법 (되/돼, -ㄴ지/-는지, -ㄹ게/-를게, 던/든, 안/않, 웬/왠, -로써/-로서)
- 우선순위 2: 띄어쓰기 (의존명사 붙여쓰기)
- 우선순위 3: 조사 오류 (받침 불일치 -을/를, -이/가, -은/는, -와/과), 어미 (-읍니다)
- 우선순위 4: 구두점 (가운뎃점 오남용 후보, 따옴표 혼용)

사용: python3 scripts/scan_grammar.py
산출물: dist/grammar-scan.txt
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
TAG_RE = re.compile(r"<[^>]+>")

# 한글 음절의 받침 유무 판별 (종성 코드)
def has_jongseong(ch):
    if not ('\uac00' <= ch <= '\ud7a3'):
        return False
    return (ord(ch) - 0xAC00) % 28 != 0

# --- 패턴 정의: (이름, 정규식, 설명, 확신도) ---
PATTERNS = [
    # 우선순위 1: 맞춤법
    ("되/돼 — '안되' 붙여쓰기", re.compile(r"안되[어요]?|안되면|안되서|됬"), "'안 돼'로 띄어 씀 (안+돼). '안되다'는 형용사(안타깝다)일 때만", "확실한 오류"),
    ("되/돼 — '되요'", re.compile(r"되요"), "'되어요'의 준말은 '돼요'", "확실한 오류"),
    ("-ㄴ지/-는지 — 형용사+는지", re.compile(r"(좋는지|많는지|싫는지|적는지|높는지|낮는지|어렵는지|쉽는지|크는지|작는지|비싸는지|싸는지|빠르는지|느리는지|길는지|짧는지)"), "형용사는 '-ㄴ지'(좋은지), 동사만 '-는지'", "확실한 오류"),
    ("-ㄹ게/-를게", re.compile(r"(하를게|보를게|먹를게|가를게|하를게요)"), "'-ㄹ게'가 항상 맞음 (하를게요→할게요)", "확실한 오류"),
    ("던/든 — 과거 회상에 '든'", re.compile(r"(했든|갔든|먹든|보든|했든|있든|없든)( |<[^>]+>)*(곳|때|음식|사람|날|적)"), "과거 회상은 '-던'(했던 곳)", "확실한 오류"),
    ("안/않 — '지 않' 오류", re.compile(r"(하지 안[고아]|않 해|않 하|않 가|않 오|안 지 않)"), "'-지 않-'이 맞음 (하지 않고)", "확실한 오류"),
    ("안/않 — '않' 단독", re.compile(r"않 (가|오|하|되|먹|보|주|놓|두)"), "'않'은 '-지 않다'로만, 단독 부정은 '안'", "확실한 오류"),
    ("웬/왠", re.compile(r"왠일|웬지|왠만"), "'왠'은 '왠지'에만, 나머지는 '웬'", "확실한 오류"),
    ("-로써/-로서 혼동 (자격에 로써)", re.compile(r"([가-힣]+)로써 (대표|사장|회장|회원|학생|시민|국민|지도자)"), "자격/지위는 '-로서'", "권장 사항"),
    # 우선순위 2: 띄어쓰기 (의존명사)
    ("의존명사 붙여쓰기 '수'", re.compile(r"할수 ?(있|없)"), "'할 수 있다' — '수'는 의존명사로 띄어 씀", "확실한 오류"),
    ("의존명사 붙여쓰기 '것'", re.compile(r"[가-힣](는|은|ㄴ)것(이|은|을|도|만|들)"), "'것'은 의존명사로 띄어 씀", "확실한 오류"),
    ("의존명사 붙여쓰기 '뿐'", re.compile(r"[가-힣](ㄹ|을|ㄴ)뿐"), "'뿐'은 의존명사로 띄어 씀", "확실한 오류"),
    ("의존명사 붙여쓰기 '만큼'", re.compile(r"[가-힣](ㄹ|을|ㄴ)만큼"), "'만큼'은 의존명사로 띄어 씀", "확실한 오류"),
    # 우선순위 3: 조사 오류 (받침 불일치)
    ("조사 -을/를 불일치", None, "받침 없으면 '-를', 받침 있으면 '-을'", "확실한 오류"),  # 커스텀
    ("조사 -이/가 불일치", None, "받침 없으면 '-가', 받침 있으면 '-이'", "확실한 오류"),  # 커스텀
    ("조사 -은/는 불일치", None, "받침 없으면 '-는', 받침 있으면 '-은'", "확실한 오류"),  # 커스텀
    ("조사 -와/과 불일치", None, "받침 없으면 '-와', 받침 있으면 '-과'", "확실한 오류"),  # 커스텀
    ("어미 '-읍니다'", re.compile(r"[가-힣]읍니다"), "받침 있는 용언은 '-습니다' (먹읍니다→먹습니다)", "확실한 오류"),
    # 우선순위 4: 구두점
    ("가운뎃점 단순 나열 후보", re.compile(r"[가-힣]·[가-힣]·[가-힣]"), "짝/공통성분이 아닌 단순 나열이면 쉼표 권장 (문맥 판단)", "권장 사항"),
]

# 조사 쌍: (조사, 받침 없을 때, 받침 있을 때)
# "이/가/은/는"은 단어 내부 음절 오탐이 폭주(국가→국이)하므로 제외.
# "을/를"·"와/과"만 검사 (오탐 상대적으로 적음)
JOSA_RULES = [
    ("을", "를", "을"),
    ("를", "를", "을"),
    ("와", "와", "과"),
    ("과", "와", "과"),
]

# 단어 내부에서 조사로 오인되는 흔한 단어 (오탐 블랙리스트)
JOSA_BLACKLIST = {
    "가을", "마을", "서울", "너을", "하늘", "바다", "고을", "나을",
    "효과", "사과", "니카라과", "바나과", "코스타리카과", "도화과", "포과",
    "초과", "부과", "여과", "통과", "합격과", "누과", "고과",
    "파라과이", "우루과이", "마나과", "안와르",
}


def check_josa(text):
    """받침 불일치 조사 검출. (위치, 틀린 표현, 올바른 표현)"""
    hits = []
    for m in re.finditer(r"([가-힣])(을|를|와|과)", text):
        prev, josa = m.group(1), m.group(2)
        start = max(0, m.start() - 3)
        end = min(len(text), m.end() + 1)
        context = text[start:end]
        if any(w in context for w in JOSA_BLACKLIST):
            continue
        has_jong = has_jongseong(prev)
        correct = "를" if not has_jong and josa == "을" else \
                  "을" if has_jong and josa == "를" else \
                  "와" if not has_jong and josa == "과" else \
                  "과" if has_jong and josa == "와" else None
        if correct:
            hits.append((m.start(), prev + josa, prev + correct))
    return hits


def collect():
    out = []
    for f, label, fields in [
        ("strings.json", "Common_Strings", ["ko"]),
        ("cards.json", "TS_Cards", ["ko"]),
        ("runtime-20260315.json", "runtime", ["translation_ko"]),
        ("manual-extra.json", "manual-extra", ["__all__"]),
        ("manual-scenes.json", "manual-scenes", ["__manual__"]),
    ]:
        p = ROOT / "translation" / f
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        for field in fields:
            if field == "__all__":
                for k, v in d.items():
                    if isinstance(v, str) and k not in ("$schema", "description"):
                        out.append((f"{label}:{k}", v))
            elif field == "__manual__":
                for k, v in d.get("manual", {}).items():
                    out.append((f"{label}:{k}", v))
            elif field == "ko":
                for row in d.get("rows", []):
                    if row.get("ko"):
                        out.append((f"{label} row{row.get('row')} [{row.get('key','')}]", row["ko"]))
            else:
                for e in d.get("entries", []):
                    if e.get("translation_ko"):
                        out.append((f"runtime L{e.get('source_line')}", e["translation_ko"]))
    return out


def main():
    items = collect()
    print(f"총 번역 항목: {len(items)}")
    results = []  # (우선순위, 이름, 확신도, id, 컨텍스트)
    for pid, ko in items:
        ko_plain = TAG_RE.sub("", ko)
        for name, rx, desc, conf in PATTERNS:
            if rx is None:
                continue
            for m in rx.finditer(ko_plain):
                s = max(0, m.start() - 15)
                e = min(len(ko_plain), m.end() + 15)
                results.append((name, conf, pid, ko_plain[s:e].replace("\n", " "), m.group(0), desc))
        # 조사 오류 (커스텀)
        for pos, wrong, right in check_josa(ko_plain):
            s = max(0, pos - 15)
            e = min(len(ko_plain), pos + len(wrong) + 15)
            results.append(("조사 %s → %s" % (wrong, right), "확실한 오류", pid,
                            ko_plain[s:e].replace("\n", " "), wrong, "받침에 따라 조사 선택"))

    # 출력
    lines = []
    by_name = {}
    for name, conf, pid, ctx, matched, desc in results:
        by_name.setdefault((name, conf), []).append((pid, ctx, matched, desc))
    total = 0
    for (name, conf), hits in sorted(by_name.items(), key=lambda kv: -len(kv[1])):
        total += len(hits)
        lines.append(f"### [{conf}] {name} — {len(hits)}건")
        for pid, ctx, matched, desc in hits[:10]:
            lines.append(f"  - {pid}: …{ctx}…  (→ {matched})")
        if len(hits) > 10:
            lines.append(f"  - … 외 {len(hits)-10}건")
        lines.append("")
    lines.insert(0, f"총 의심 항목: {total}건 (항목 수 {len(set(r[2] for r in results))})")
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    (out / "grammar-scan.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:30]))
    print(f"\n전체 결과: dist/grammar-scan.txt ({len(lines)}줄)")


if __name__ == "__main__":
    main()
