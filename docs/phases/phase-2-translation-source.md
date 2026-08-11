# Phase 2 — 문자열 추출 & 번역 소스 구축

## 상태

- 상태: ✅ 완료
- 선행 Phase: Phase 1 완료
- 착수일: 2026-08-05
- 완료일: 2026-08-08

## 목표

실제 사용되는 TextAsset에서 영문 문자열을 추출하고, 기존 블루칩 패치 및 신규 런타임 패치의 한글 번역을 현재 게임 버전에 맞춰 `translation/`의 소스 파일로 정리한다.

## 번역 소스 구조 원칙 (Phase 4 주입을 위한 선결 조건)

Phase 4 검증 기준(재현성·안전성)을 만족하려면 번역 소스는 **raw 부분문자열 치환**에 의존하지 않고 **키/셀 단위**로 설계해야 한다. `patch_textasset.py`의 raw `str.replace`는 짧은 토큰(`US`, `The`, `in`) 측면 치환 위험이 있으므로, Phase 2 산출 구조가 이를 회피하는 것이다.

- `Common_Strings`는 스프레드시트형 (행=키, 열=언어) → 추출 단위는 **(행 키, EN 열 값)**이며 번역은 같은 행의 **한글 교체 대상 열** 값으로 대응.
- `TS_Cards` 동일하게 행 기반 구조면 (행 키, 필드) 단위로 추출.
- 번역 JSON의 키는 에셋 내 **고유 식별자**(행 키/Path ID/셀 주소)로 지정하여, 주입 시 셀 단위 교체가 가능하도록 한다.
- 임의 부분문자열 매칭은 번역 소스 구축 단계(매칭)에서만 허용하고, 주입 단계에서는 키 매칭을 사용한다.

### 번역 주입 방식 결정 (2026-08-05)

- **EN 열(열 2)은 보존하고, 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않는다.
- 이유: 영문 폴백·원문 대조·번역 검수 유지, EN열 치환 시 발생 가능한 짧은 토큰 측면 치환 위험 회피.
- 게임이 한국어를 언어 선택기에서 인식하려면 교체 대상 열에 해당하는 언어로 게임 언어를 전환하거나, 새 한국어 컬처를 `AvailableCultures`에 등록해야 한다.
- 현재 `Common_Strings` 열 구조: `Key(1) EN(2) FR(3) DE(4) ES(5) PL(6) PT(7) JP(8) IT(9) RU(10) NL(11) CH(12) null(13~)`
- 현재 `AvailableCultures` 등록 언어: `de, en, es, fr, ru` (SmartLocalization)
- **구체적 교체 열과 컬처 등록 방식은 Phase 4에서 검증 결정** — SmartLocalization이 언어 코드 → 열 인덱스를 어떻게 매핑하는지 확인 후 확정.
- Phase 2 번역 소스는 **EN 원문**(열 2)과 **번역값**(한글)을 분리해 저장하므로, 교체 열 선택과 무관하게 재사용 가능.

## 체크리스트

- [x] `Common_Strings` 영문 문자열 추출 → `translation/strings.json` (키/행 단위)
- [x] `TS_Cards` 영문 문자열 추출 → `translation/cards.json` (키/행 단위)
- [x] **블루칩 v1.0.1 MonoBehaviour에서 한글 432개 추출** (raw 바이트 수동 파싱, UnityPy `read()`는 IL2CPP로 실패)
- [x] 신규 런타임 패치 `runtime_exact.tsv`에서 원문-한글 2,253개 추출 (비교·검증용, BepInEx 포팅 대상 아님)
- [x] 현재 `Common_Strings`·`TS_Cards`와 신규 런타임 번역의 원문 전체 일치 매칭
- [x] 전체 일치한 신규 런타임 번역을 `Common_Strings`·`TS_Cards` 행 키에 연결
- [x] 현재 문자열과 기존 번역 자동 매칭 (매칭은 원문 전체 비교, 부분 토큰 비교 금지)
- [x] 버전 차이 문장 수동 분류·번역
- [ ] 용어 통일표 `translation/glossary.md` 작성 → Phase 3과 병행
- [ ] TMP 리치텍스트 태그 보존 규칙 수립
- [x] 기타 TextAsset 사용 여부 확인 (`TS_Ingame`·`TS_Strings`·`TS_RulesTutorial`·`Common_Ingame`) → Phase 4에서 검증
- [x] 번역 JSON 스키마 확정: 행 키/Path ID → 번역 값 매핑 (Phase 4 주입기 입력 규격)
- [x] (선택) `Common_Strings`의 타 언어 열을 참조용으로 활용해 매칭 교차 검증
- [x] (선택) 우드킹 패치 입수 시 보조/검증용으로 매칭 교차 검증 → 불필요 (신규 런타임 TSV로 충분)

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 문자열 추출 | 대상 TextAsset의 키·영문·식별자(Path ID/행 키)가 재현 가능하게 추출됨 |
| 번역 매칭 | 매칭 수와 미매칭 수를 산출할 수 있고, 매칭은 원문 전체 비교로 수행 |
| 주입 호환성 | 번역 JSON 키가 에셋의 고유 식별자와 1:1로 대응하여 Phase 4에서 셀 단위 교체 가능 |
| 태그 보존 | `<color>`, `<font>`, `<br>`, `<indent>` 등이 원문과 번역에서 보존됨 |
| 재현성 | 원본 에셋에서 같은 명령으로 JSON을 재생성할 수 있음 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| 신규 런타임 번역 추출 | `extract_runtime_tsv.py`로 TSV 행 순서·중복을 보존해 JSON 생성 | ✅ 성공 — 2,253개 원문-한글 쌍 추출 |
| 신규 런타임 번역 매칭 | `match_runtime_translations.py`로 현재 `Common_Strings`·`TS_Cards` 666행과 전체 문자열 비교 | ✅ 성공 — 337행 정확 일치, 4행 이스케이프 해석 후 일치 |
| 카드 타이틀 추가 매칭 | `match_remaining.py`로 TS_Cards 타이틀 조각 런타임 TSV 카드명 인덱스 매칭 | ✅ 성공 — 64행 추가 매칭 |
| 확장 매칭 (prefix/quotes/format 보정) | `apply_all_translations.py`로 `+1 ` prefix, `<font>` 태그, 따옴표 차이 보정 | ✅ 성공 — 10행 추가 매칭 |
| 수동 번역 (Common_Strings 235행) | `apply_manual_translations.py`로 235행 한글 번역 적용 | ✅ 성공 — 235행 전체 번역 |
| 최종 커버리지 | 666행 전체 `ko` 필드 존재 확인 | ✅ 성공 — **666/666 (100%)** |

## 산출물 예정

- `translation/strings.json` — `Common_Strings` 행 키 → 한글 매핑 (EN 원문은 보존용으로 함께 기록)
- `translation/cards.json` — `TS_Cards` 행 키/Path ID → 한글 매핑
- `translation/legacy-bluechip.json` — 블루칩 v1.0.1 MonoBehaviour에서 추출한 432개 고유 한글 문자열 (매칭 원본)
- `translation/runtime-20260315.json` — 신규 런타임 패치에서 추출한 원문-한글 2,253개 쌍 (비교·검증용)
- `translation/runtime-20260315-matches.json` — 현재 TextAsset 666행에 대한 신규 런타임 번역 전체 일치 매칭 결과
- `translation/schema.md` — Phase 4 주입기 입력 스키마와 EN 보존·키 기반 주입 규칙
- `translation/glossary.md` — 용어 통일표
- `translation/schema.md` — 번역 JSON 스키마 명세 (Phase 4 주입기 입력 규격)
- 문자열 추출·매칭 스크립트 (키/셀 단위 + MonoBehaviour raw 파싱 + 런타임 TSV 추출·전체 일치 매칭)

## 다음 Phase로 핸드오프

### 결정 사항

- **번역 소스 전략**: 런타임 TSV(신규 BepInEx 패치의 `runtime_exact.tsv`)를 1차 소스로 사용. 블루칩 v1.0.1의 MonoBehaviour 한글은 v1.0.1에 `Common_Strings`/`TS_Cards` TextAsset이 없어 매칭 불가. 신규 런타임 TSV로 충분히 커버되어 불필요.
- **EN 열 보존**: `Common_Strings` 모든 행은 EN(열 2) 원문을 유지하고 `ko` 필드를 별도로 추가. 교체 대상 열은 Phase 4에서 결정.
- **매칭 전략**: 원문 전체 비교를 원칙으로 하되, TS_Cards 카드 타이틀 조각은 런타임 TSV의 카드명 인덱스를 통해 매칭. prefix(`+1 ` 등), 따옴표, `<font>` 태그 차이는 보정 매핑으로 처리.

### 산출물 위치

- `translation/strings.json` — Common_Strings 322행, `ko` 및 `ko_source` 포함
- `translation/cards.json` — TS_Cards 344행, `ko` 및 `ko_source` 포함
- `translation/runtime-20260315.json` — 런타임 TSV 원본 2,253쌍
- `translation/runtime-20260315-matches.json` — 기존 매칭 결과
- `scripts/archive/apply_all_translations.py` — 모든 번역 적용 스크립트 (Phase 2 일회성, 2026-08-12 archive/로 이동)
- `scripts/archive/apply_manual_translations.py` — Common_Strings 수동 번역 맵
- `scripts/archive/match_remaining.py` — TS_Cards 추가 매칭 스크립트

### 사용 글자 수

`strings.json` + `cards.json`의 모든 `ko` 값에서 고유 한글 음절 추출:
- Phase 3에서 `scripts/` 아래 문자셋 추출 스크립트로 산출 예정

### 미해결 이슈

- `TS_Ingame`, `TS_Strings`, `TS_RulesTutorial`, `Common_Ingame` 사용 여부 미검증 → Phase 4에서 확인
- TMP 리치텍스트 태그 보존 규칙 수립 대기 → Phase 4에서 주입 시 검증

### Phase 3 즉시 실행 작업

1. `translation/strings.json` + `translation/cards.json`에서 모든 `ko` 값의 고유 한글 글자 추출
2. 폰트 (`fonts/`) 선정 완료됨 (Noto Serif KR 등) → TTF 준비 확인
3. `make_sdf.py` 실행을 위한 Unity_Font_Replacer 설정
4. 4096² SDF 아틀라스 생성 및 `resources.assets` 주입 테스트

---

Phase 완료 시 다음 항목을 기록한다.

- 추출된 문자열 수와 TextAsset별 분포
- 기존 번역 매칭률 및 미번역 목록
- 번역 JSON 스키마(행 키/Path ID → 번역 값 매핑) 확정 위치
- 용어표 위치와 주요 결정 사항
- 보존해야 하는 TMP 태그 목록
- 산출된 사용 글자 수와 Phase 3 문자셋 입력 위치
- 버전 차이로 보류한 문자열
- (중요) Phase 4 주입 스크립트는 키 매칭 기반 셀/행 단위 교체로 구현할 것 — raw 부분문자열 치환 사용 금지
