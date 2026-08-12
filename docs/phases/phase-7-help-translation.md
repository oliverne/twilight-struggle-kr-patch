# Phase 7 — 도움말/규칙 번역

## 상태

- 상태: 🚧 진행 중 (착수일: 2026-08-13)
- ⚠️ **순서 변경 (2026-08-13 사용자 결정)**: 기존 "배포 후 맨 마지막에 수행" → **배포 전에 수행**.
  최종 배포(Phase 6)는 Phase 7 완료 후 진행한다.
- 선행 Phase: Phase 5 완료

## 목표

게임 내 도움말(HELP)과 규칙북(RB) 텍스트를 한글화한다. 카드·UI·메뉴(Phase 4~5)와 달리 **번역 소스가 전무해 전량 수동 번역**이 필요한 영역.

## 대상 (2026-08-12 실측)

| 대상 | 위치 | 분량 | 비고 |
|---|---|---|---|
| TS_RulesTutorial | `resources.assets` TextAsset, 시트 1631793870 | **313행 / EN 본문 63,997자** | RB_ 규칙 97 + Help_ 도움말 214 + 기타 2. EN 열(3열), KO 열(10열) 이미 존재 |
| 씬 규칙 문단 | level1·level2 MonoBehaviour | 167개 | analyze_scene_texts에서 rules-text로 스킵된 항목 |
| **번역 소스** | — | **0개** | 런타임 TSV(2,253쌍)에 Help/RB 관련 0개 → 전량 수동 |

## 체크리스트

### 0. 선행 검증 (착수 전 필수 — AGENTS.md "살아있는 소스" 원칙)

- [x] TS_RulesTutorial 구조 실측 (2026-08-13) — 시트 1631793870: 313행 (RB_ 97 + Help_ 214 + Key_ 2), EN 63,997자, **KO 열(10열) 존재 확인**
- [ ] 게임에서 규칙북(RB)/도움말(HELP) 진입 경로 확인 (메뉴·게임 내 버튼) — 실게임 필요
- [ ] TS_RulesTutorial이 실제 화면 표시에 사용되는지 실게임 확인 — Phase 4의 "표시 텍스트 없음" 기록과 대조
- [ ] 표시 경로가 확인되면 표시되는 키(RB_/Help_)와 테이블 매핑 기록

### 1. 용어표(용어집) 신설

- [x] 기존 번역(cards.json·strings.json·runtime TSV·manual-*.json)에서 게임 용어 추출
      (진출/지배/격전지/데프콘/우주 경쟁/입찰/쿠데타/재편성/승점 등 — 2026-08-13 조사 완료)
- [x] `translation/glossary.md` 작성 — EN 용어 → 통일 한글 + 근거(기존 사용처) (2026-08-13)
- [ ] 번역 작업 전 용어표 확정 (검토 후 승인) — ⬜ 사용자 검토 필요

### 2. TS_RulesTutorial 번역

- [x] TS_RulesTutorial EN 313행 추출 → `translation/manual-rules.json` 생성 (key → original → translation_ko, 2026-08-13)
- [ ] 용어표 기준으로 번역 (AI 보조 → humanizer/grammar-checker 검수 — translation-polish 워크플로우)
- [ ] 번역 품질 검수 (용어 일관성, TMP 태그 보존, 문단 구조)

### 3. 주입

- [ ] `inject_translations.py`에 rules 테이블 처리 추가 (현재 건너뜀) → EN 열 교체
- [ ] `add_ko_columns.py` 재실행 (KO 열 동기화)
- [ ] 씬 규칙 문단 167개 — `translation/manual-scenes.json`에 추가 후 `patch_scenes.py` 재실행
- [ ] 번역 후 글리프 확인 — 새 글자 발생 시 `fonts/chars.txt` 확장 → SDF 재생성 → 폰트 재주입

### 4. 검증

- [ ] `verify_assets.py` 검증 (m_Script 0건, 의도 밖 변경 0건)
- [ ] 실게임 확인 (규칙북/도움말 팝업 — 스크롤·줄바꿈·레이아웃)
- [ ] 잔존 영문/`□` 0건 확인

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 규칙북 | RB_ 섹션 전부 한글 표시, 줄바꿈·리치텍스트 태그 정상 |
| 도움말 팝업 | Help_ 전 항목 한글 표시 (쿠데타/영향력/우주 경쟁/데프콘 등) |
| 레이아웃 | 긴 문단에서 텍스트 잘림 없음 (스크롤/폰트 크기 확인) |
| 문자셋 | `□` 누락 0건 |
| 용어 일관성 | 카드/UI 번역과 용어표가 일치 (번역 검수로 확인) |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| TS_RulesTutorial 구조 실측 | extract_textassets.py 추출 (2026-08-13) | ✅ 시트 1631793870, 313행 (RB_ 97 + Help_ 214 + Key_ 2), EN 63,997자, KO 열(10열) 존재 |
| 용어 조사 | 런타임 TSV 빈도 조사 (2026-08-13) | ✅ 핵심 용어 40여 개 통일안 도출 (승점/점수 카드/작전치/진출·지배·장악 등) |
| 용어표 | glossary.md 작성 (2026-08-13) | ✅ 초안 완료 — 사용자 검토 대기 |
| manual-rules.json | 313행 EN 추출 (2026-08-13) | ✅ 생성 완료 — translation_ko 미입력 (번역 대기) |
| 선행 검증 (실표시 경로) | 실게임 확인 | ⬜ 대기 |
| 규칙북/도움말 번역 | — | ⬜ 대기 |
| 주입·검증 | — | ⬜ 대기 |

## 산출물 (예정)

- ✅ `translation/glossary.md` — 용어 통일표 (2026-08-13 초안)
- ✅ `translation/manual-rules.json` — TS_RulesTutorial 313행 EN 추출 (2026-08-13, 번역 대기)
- ⬜ `scripts/inject_translations.py` 확장 (rules 테이블 처리)
- ⬜ 갱신된 `translation/manual-scenes.json` (씬 규칙 문단 167개)

## 다음 Phase로 핸드오프

(Phase 7 완료 시 작성 — 최종 배포(Phase 6)로 이관)

## 참고

- KO 열 구조: TS_RulesTutorial 시트 1631793870 — 1열=키(String), 2열=US, 3열=EN, 4~8=FR/IT/DE/ES/NL, 9=Notes, **10열=KO** (add_ko_columns.py가 배치, 원본 존재 열 범위 내)
- 용어표: 카드/UI 번역에서 사용한 용어(진출/지배/격전지 등)와 일관 유지 — `translation/manual-scenes.json` 참조
