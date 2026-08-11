# Phase 7 — 도움말/규칙 번역 (후순위)

## 상태

- 상태: ⬜ 대기 (배포 이후 맨 마지막에 수행 — 사용자 결정 2026-08-12)
- 선행 Phase: Phase 6 (배포) 완료 후

## 목표

게임 내 도움말(HELP)과 규칙북(RB) 텍스트를 한글화한다. 카드·UI·메뉴(Phase 4~5)와 달리 **번역 소스가 전무해 전량 수동 번역**이 필요한 영역.

## 대상 (2026-08-12 실측)

| 대상 | 위치 | 분량 | 비고 |
|---|---|---|---|
| TS_RulesTutorial | `resources.assets` TextAsset, 시트 1631793870 | **313행 / EN 본문 63,997자** | RB_ 규칙 97 + Help_ 도움말 214 + 기타 2. EN 열(3열), KO 열(10열) 이미 존재 |
| 씬 규칙 문단 | level1·level2 MonoBehaviour | 167개 | analyze_scene_texts에서 rules-text로 스킵된 항목 |
| **번역 소스** | — | **0개** | 런타임 TSV(2,253쌍)에 Help/RB 관련 0개 → 전량 수동 |

## 체크리스트

- [ ] 용어표 확장 — 규칙 용어(작전점/쿠데타/데프콘/재편성/승점 등) 검토, `translation/` 용어표 갱신
- [ ] TS_RulesTutorial EN 313행 추출 → 번역 (수동 또는 AI 보조 후 검수)
- [ ] `translation/manual-rules.json` 작성 (key → KO)
- [ ] 주입: `inject_translations.py`에 rules 테이블 처리 추가 (또는 별도 스크립트) → EN 열 교체
- [ ] `add_ko_columns.py` 재실행 (KO 열 동기화)
- [ ] 씬 규칙 문단 167개 — `translation/manual-scenes.json`에 추가 후 `patch_scenes.py` 재실행
- [ ] 번역 후 글리프 확인 — 새 글자 발생 시 `fonts/chars.txt` 확장 → SDF 재생성 → 폰트 재주입
- [ ] 검증 (verify_assets.py) + 실게임 확인 (규칙북/도움말 팝업)

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 규칙북 | RB_ 섹션 전부 한글 표시, 줄바꿈·리치텍스트 태그 정상 |
| 도움말 팝업 | Help_ 전 항목 한글 표시 (쿠데타/영향력/우주 경쟁/데프콘 등) |
| 레이아웃 | 긴 문단에서 텍스트 잘림 없음 (스크롤/폰트 크기 확인) |
| 문자셋 | `□` 누락 0건 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

## 다음 Phase로 핸드오프

(Phase 7 완료 시 작성 — 배포 후 수행 예정)

## 참고

- KO 열 구조: TS_RulesTutorial 시트 1631793870 — 1열=키(String), 2열=US, 3열=EN, 4~8=FR/IT/DE/ES/NL, 9=Notes, **10열=KO** (add_ko_columns.py가 배치, 원본 존재 열 범위 내)
- 용어표: 카드/UI 번역에서 사용한 용어(진출/지배/격전지 등)와 일관 유지 — `translation/manual-scenes.json` 참조
