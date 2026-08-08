# Phase 4 — 텍스트 주입 & 레이아웃 조정

## 상태

- 상태: 🚧 진행 중 (Common_Strings + TS_Cards + AvailableCultures 주입 완료)
- 선행 Phase: Phase 2·3 완료

## 목표

번역 소스를 게임 에셋에 반복 적용할 수 있는 파이프라인을 만들고, 한글 길이·개행·TMP 태그 차이로 발생하는 UI 레이아웃 문제를 조정한다.

## 주입 방식 결정 (Phase 2에서 확정)

- **EN 열(열 2)은 보존하고, 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않는다.
- 이유: 영문 폴백·원문 대조·번역 검수 유지, EN열 치환 시 짧은 토큰 측면 치환 위험 회피.
- 현재 `Common_Strings` 열 구조: `Key(1) EN(2) FR(3) DE(4) ES(5) PL(6) PT(7) JP(8) IT(9) RU(10) NL(11) CH(12) null(13~)`
- 현재 `AvailableCultures` 등록 언어: `de, en, es, fr, ru` (SmartLocalization)
- Phase 2 번역 소스는 **EN 원문**(열 2)과 **번역값**(한글)을 분리 저장했으므로, 교체 열 선택과 무관하게 재사용 가능.

## 체크리스트

- [x] 번역 JSON → TextAsset 주입 스크립트 작성 (`scripts/inject_translations.py`)
- [x] **Common_Strings 주입** — RU(10열) → KO, 322행 한글 주입, EN(2열) 보존
- [x] **TS_Cards 주입** — 344행 EN→한글 교체
- [x] **AvailableCultures 수정** — ru → ko (한국어 선택 가능)
- [x] EN 열 보존 검증 (Common_Strings: col 2 EN 무결함)
- [ ] 게임에서 한국어로 전환되는지 실게임 테스트
- [ ] `TS_Ingame`, `TS_Strings`, `TS_RulesTutorial`, `Common_Ingame` 추가 주입
- [ ] 설치 스크립트 `scripts/install-*.sh` 작성
- [ ] 주입 전후 무결성 검증 추가

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 재현성 | 번역 JSON과 원본 에셋만으로 패치 파일을 재생성할 수 있음 |
| 보존성 | TMP 태그와 필요한 개행이 유지됨 |
| 레이아웃 | 주요 화면에서 텍스트 잘림·겹침·빈 박스가 없음 |
| 안전성 | 스크립트가 원본 해시를 확인하고 멱등적으로 실행됨 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| Common_Strings 주입 | `inject_translations.py` — 셀 단위 키 매칭, RU(10)→KO, EN 무결성 검증 | ✅ 성공 — 322행 한글 주입, EN 보존 |
| TS_Cards 주입 | `inject_translations.py` — row-key 기반 EN→KO | ✅ 성공 — 344행 교체, 카드명/설명 한글 확인 |
| AvailableCultures | XML 텍스트 치환 ru→ko | ✅ 성공 — "ko" 문화 등록 |
| 게임 테스트 | — | ⬜ 대기 (Phase 3 폰트 주입 선행 필요) |

## 다음 Phase로 핸드오프

Phase 완료 시 수정 파일 목록, 레이아웃 이슈, 제외한 텍스트 영역, 플랫폼별 주의사항을 기록한다.
