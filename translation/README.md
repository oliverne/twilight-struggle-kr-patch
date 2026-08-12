# translation/ — 번역 소스

한글 패치의 **진짜 코드** (불변 원칙 #4: 텍스트 주입은 이 폴더의 소스를 반복 실행 가능한 스크립트로만 수행).
EN 원문은 절대 덮어쓰지 않고 `ko` 필드로만 관리한다. 스키마는 [schema.md](schema.md) 참조.

## 활성 소스 (파이프라인이 사용)

| 파일 | 대상 | 분량 | 사용 스크립트 | 갱신 방법 |
|---|---|---|---|---|
| `strings.json` | Common_Strings (UI 문자열) | 322행 | `inject_translations.py` | 원본 TextAsset에서 재생성 (`scripts/archive/extract_original_en.py`) |
| `cards.json` | TS_Cards (카드 344행) | 344행 | `inject_translations.py` | 위와 동일 |
| `runtime-20260315.json` | 신규 런타임 패치 원문↔번역 (영문 원문 기준) | 2,253쌍 | `inject_translations.py`·`patch_scenes.py`·`analyze_scene_texts.py` | `scripts/archive/extract_runtime_tsv.py` |
| `manual-extra.json` | 잔존 UI 키 수동 번역 (TS_Ingame 40 + TS_Strings 12) | 52개 | `inject_translations.py`·`patch_scenes.py` | **수동 추가** — 미번역 키 발견 시 여기에 EN→KO 추가 |
| `manual-scenes.json` | 씬(level1~3) 하드코딩 문자열 수동 번역 | 206개 | `patch_scenes.py` | **수동 추가** — 씬 영어 잔존 발견 시 `manual`에 추가 |
| `schema.md` | 소스 스키마 문서 | — | — | — |

## 참고/산출물 (Phase 2 구축 — 보관)

| 파일 | 내용 | 상태 |
|---|---|---|
| `legacy-bluechip.json` | 블루칩 v1.0.1 MonoBehaviour 추출 (고유 한글 432개) | ✅ 번역 매칭 완료 — 감사/참고용 |
| `legacy-bluechip-lua.json` | 블루칩 twilight_cards.lua 카드 정의 | 참고용 (한글 10줄뿐 — 사실상 무의미) |
| `runtime-20260315-matches.json` | 런타임 TSV↔TextAsset 매칭 결과 (matches/ambiguous/unmatched) | 산출물 — 재실행 시 재생성 |

## 파이프라인 연동 (번역 추가 시)

```
1. 키 발견   → manual-extra.json(TextAsset) 또는 manual-scenes.json(씬)에 추가
2. 주입      → scripts/inject_translations.py  (EN 열 한글화)
3. KO 동기화 → scripts/add_ko_columns.py        (KO 열 = EN 값 복사)
4. 씬        → scripts/patch_scenes.py          (씬 하드코딩)
5. 검증      → scripts/verify_assets.py
6. 문자셋    → 새 글자 발생 시 scripts/extract_charset.py → fonts/chars.txt → SDF 재생성
```

⚠️ **우선순위**: `key_to_ko(strings/cards) > runtime TSV(EN 값 매칭) > manual` — 기존 번역이 먼저 적용되고
수동 번역이 덮어쓴다. EN 열은 항상 보존된다.

⚠️ **용어 일관성**: 용어표 `translation/glossary.md` 기준으로 번역한다 (Phase 7에서 신설, 2026-08-13).
수동 번역 추가 시 기존 번역(러시아·쿠데타·격전지·영향력·데프콘 등)과 용어를 맞출 것 — [docs/phases/phase-7-help-translation.md](../docs/phases/phase-7-help-translation.md)

## 구성 규칙

- `ko` 필드: 확정 번역만. 미번역 행은 필드 자체가 없음 (검토 대기)
- `translation_source`: ko의 출처·매칭 근거 (runtime / legacy-bluechip / manual)
- TMP 리치텍스트 태그(`<color>`, `<font>`, `<br>`, `<indent>`)는 보존 — 번역문에도 유지
