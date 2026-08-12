---
name: twilight-struggle-translation-polish
description: Twilight Struggle 한글 패치의 번역 소스(translation/*.json)를 humanizer(AI 패턴)와 grammar-checker(맞춤법/조사)로 검사·교정하는 전체 워크플로우. 스캔 → 일괄 교정 → 수동 교정 → 문법 검사 → 검증 → 문서화까지. 번역 다듬기 요청 시 사용.
---

# Twilight Struggle 한글 패치 — 번역 교정 워크플로우

## 배경 (핵심 지식)

- 번역 소스는 `translation/*.json` (진짜 코드). **EN 원문은 절대 수정하지 않는다.**
- 두 검사기 스킬을 결합:
  - **humanizer** (`.agents/skills/humanizer`) — AI 작문 마커 40패턴 (번역투·쉼표·유행어)
  - **grammar-checker** (`.agents/skills/grammar-checker`) — 맞춤법·띄어쓰기·조사·구두점
- 스크립트 5종 (모두 멱등, `PYTHONIOENCODING=utf-8` 필수):

| 스크립트 | 역할 |
|---|---|
| `scripts/scan_ai_patterns.py` | AI 패턴 1차 필터 (S1/S2/S3, dist/ai-scan.txt) |
| `scripts/dump_ai_hits.py` | 히트 상세 JSON (원문 포함, dist/ai-hits.json) |
| `scripts/polish_translations.py` | 규칙 기반 일괄 교정 (`--dry-run` 지원, dist/polish-1.diff) |
| `scripts/apply_polish.py` | 수동 교정안 적용 (dist/polish-2.diff) |
| `scripts/scan_grammar.py` | 맞춤법/조사 검사 (dist/grammar-scan.txt) |

- 교정 결과 기록: `docs/translation-polish-review.md` (검증 수치·규칙 근거·후속 작업)
- ⚠️ **게임 에셋 반영은 별도**: 소스 수정 후 `scripts/inject_translations.py` 재실행 필요
  (이 워크플로우는 소스 수정까지만)

## 워크플로우

### 1단계: AI 패턴 스캔 (humanizer)

```bash
cd <저장소 루트>
export PYTHONIOENCODING=utf-8
python3 scripts/scan_ai_patterns.py   # → dist/ai-scan.txt (패턴별 상세)
python3 scripts/dump_ai_hits.py       # → dist/ai-hits.json (원문 포함 전체 히트)
```

- S1(결정적)은 0건이 정상. S2/S3 위주로 우선순위 판단.
- **오탐 판정 기준** (교정 제외):
  - "것으로 간주/보이", "~로 인해" → 표준 한국어 (오탐)
  - 카드 규칙의 "~할 수 있다" → 규칙서 관용 표현 (오탐)
  - 게임 용어 "~적" (업적 제목, 지정학적 등) → 오탐 다수
- **진짜 개선 대상**: 런타임 장문 (역사 서문·도움말·시나리오) — 쉼표 과다·통해·핵심·중요하 집중

### 2단계: 규칙 기반 일괄 교정 (안전 치환만)

`scripts/polish_translations.py`의 `RULES`에 규칙 추가 후:

```bash
python3 scripts/polish_translations.py --dry-run   # 적용 전 검토
python3 scripts/polish_translations.py             # 적용 → dist/polish-1.diff
```

- **규칙 추가 원칙**: 원문(EN) 대조 후 안전한 것만. 예:
  - `'악의 제국'에 의해 취소된다` → `'악의 제국'으로 취소된다` (받침에 따라 로/으로)
  - `가지고 있다면` → `보유 중이면` (기존 용어 '보유'와 통일)
  - `~통해` → `~으로` / `이를 통해` → `이로써`
- ⚠️ **TMP 태그 함정**: 실제 텍스트는 `격전지</color>을`처럼 태그가 조사 앞에 끼어 있음.
  문자열 치환이 실패하므로 **태그 허용 정규식** 사용: `re.compile(r"격전지(</?[^>]+>)?을")`
- ⚠️ 조사 치환 시 이중 주격 확인: `이 카드가 미국 플레이어가` → `이 카드를 미국 플레이어가`

### 3단계: 런타임 장문 수동 교정 (humanizer 심층)

1. 대상 선정: 스캔 결과에서 **중첩 패턴(쉼표+유행어+것이다)이 많은 라인** 우선
2. 원문(EN) 대조 후 문단 단위 재작문:
   - "~한 것이다" 반복 → "~한 것으로 본다" (규칙 정의문)
   - "완벽한 파트너" → "이상적인" / "핵심축" → "초석" / "효과적인" → "성공적인"
   - 쉼표 과다 → 문장 분리, "추구하면서, 그는" → "추구한 그는"
3. 교정안은 `translation/polish-runtime.json`의 `entries`에 `"source_line": "교정본 전체"`로 저장
   (교정 이력 영구 보존 — 재적용 가능)
4. 적용: `python3 scripts/apply_polish.py` → dist/polish-2.diff
- ⚠️ **데모로만 보여주고 파일에 안 넣는 실수 금지** — polish-runtime.json에 실제 반영 확인
  (L582가 교정안만 제시되고 누락됐던 사례 있음)

### 4단계: 맞춤법/조사 검사 (grammar-checker)

```bash
python3 scripts/scan_grammar.py   # → dist/grammar-scan.txt
```

- **조사 검사는 "을/를·와/과"만 가능**: "이/가/은/는"은 단어 내부 음절과 구분 불가
  (국가→국이, 플레이어→레이 오탐 폭주 — 형태소 분석 없이는 불가)
- **오탐 블랙리스트** (`JOSA_BLACKLIST`) 유지보수: 효과·사과·초과·부과·파라과이·우루과이·마나과·안와르 등
  컨텍스트 검사는 앞 3글자+뒤 1글자 (4글자 단어 "파라과이"가 3글자 컨텍스트에 안 걸리는 실수 주의)
- 검출된 조사 오류는 2단계의 `polish_translations.py` G 규칙으로 일괄 교정 (태그 허용 정규식)
- 따옴표 혼용·가운뎃점·던/든·-ㄴ지/-는지 패턴은 게임 텍스트에서 검출 0건 또는 전부 정상 — 참고만

### 5단계: 검증 + 문서화

```bash
# 1) 교정 후 재스캔 — 건수 감소 확인 (S1 0 유지)
python3 scripts/scan_ai_patterns.py | head -3
python3 scripts/scan_grammar.py | head -3

# 2) JSON 유효성 + EN 불변 + 교정 반영 확인
python3 -c "
import json
d = json.load(open('translation/runtime-20260315.json', encoding='utf-8'))
e = next(x for x in d['entries'] if x['source_line'] == <교정 라인>)
print('EN 유지:', '<원문 일부>' in e['original'])   # EN 필드에 한글 없음 확인
"
```

- 문서: `docs/translation-polish-review.md`에 차수별 기록 (검출/교정 수치, 규칙 근거, 오탐 판정, 후속 작업)
- `docs/PROGRESS.md` 로그 1줄 갱신
- 커밋: Conventional Commits 한국어 메시지, 번역 소스+스크립트+문서를 한 커밋에

## CRLF 주의 (2026-08-12 실측)

- Windows Python의 `Path.write_text()` / `open('w')`는 `\n` → `\r\n`(os.linesep)으로 변환해 저장한다.
- translation JSON을 저장하는 모든 스크립트는 **LF 강제**:
  `path.write_text(text, encoding='utf-8', newline='\n')` 또는 `open(path, 'w', newline='\n')`
- CRLF로 저장돼도 git(autocrlf=input)이 정규화하므로 **내용 손실은 없음**.
  판정: `git diff --no-index --ignore-cr-at-eol <HEAD버전> <현재파일>`이 비어있으면 내용 동일.
- git status에 M 노이즈가 보여도 내용이 같다면 커밋 제외 (불변 원칙 10번 참조)

## 참고: 소스 파일 구조

| 파일 | 대상 | 번역 필드 |
|---|---|---|
| `strings.json` | Common_Strings (UI) | `rows[].ko` |
| `cards.json` | TS_Cards (카드) | `rows[].ko` |
| `runtime-20260315.json` | 런타임 TSV 2,253쌍 | `entries[].translation_ko` |
| `manual-extra.json` | 잔존 UI 키 52개 | dict 값 (`__all__`) |
| `manual-scenes.json` | 씬 문자열 206개 | `manual` dict 값 (`__manual__`) |
| `polish-runtime.json` | 수동 교정안 (source_line → 교정본) | `entries` |

## 주의사항

- ⚠️ **EN 원문 불변** — ko/translation_ko 필드만 수정. 검증 시 EN 필드에 한글이 섞이지 않았는지 확인
  (원본에 이미 EN=한글인 죽은 데이터 L659/L660 존재 — 교정하지 말 것, 중복 매칭 위험)
- ⚠️ 동일 문장이 여러 라인에 중복 (TS_Cards ↔ runtime) — 일괄 치환은 전부 적용되므로 규칙 신중히
- ⚠️ `replace_in_tree`는 동일 문자열 값을 모두 교체 — 중복 값 의도 확인
- ⚠️ 변경률 가드: 2~3단계에서 원문 대비 30% 이상 재작문 금지 (의미 보존 우선)
- 관련 스킬: humanizer / grammar-checker (패턴 상세), twilight-struggle-update (에셋 재주입 시)
