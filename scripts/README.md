# scripts/ — 스크립트 인벤토리

Twilight Struggle 한글 패치 파이프라인 스크립트 모음. 실행 시 반드시:

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/<스크립트>.py ...   # Windows
PYTHONIOENCODING=utf-8 .venv/bin/python scripts/<스크립트>.py ...           # macOS
```

> ⚠️ venv(pip 패키지: UnityPy **snowyegret23 포크** + TypeTreeGeneratorAPI) 필수.
> 공식 UnityPy `save()`는 금지 — 대신 `env.typetree_generator` 설정 후 `env.file.save(packer="original")`.

---

## 1️⃣ 핵심 파이프라인 (패치 적용에 필수)

| 스크립트 | 용도 | 비고 |
|---|---|---|
| `inject_translations.py` | `translation/` 소스를 resources.assets TextAsset에 주입 (Common_Strings KO 열 교체, TS_Cards/TS_Ingame 등 EN 열 한글화, AvailableCultures ko 등록) | --gamepath는 게임 **루트**(GameAssembly.dll 위치) |
| `add_ko_columns.py` | 5개 언어 테이블에 KO 열 추가 (TS_Cards 9열 / TS_Ingame·TS_Strings·Common_Ingame 8열 / TS_RulesTutorial 10열). **멱등** — 잘못된 KO 열 자동 제거 후 재배치, 키 열(1열) 보존 검증 | 3차 테스트 교훈: 원본 범위 밖 열은 파서가 무시 |
| `patch_scenes.py` | level1~3 씬 하드코딩 텍스트 패치 (m_text @ head+56 TMP / +112 Text) | 번역 소스: 런타임 TSV + manual-scenes.json |
| `verify_assets.py` | 원본 vs 패치본 무결성 검증 (m_Script 불일치 0건, 의도 밖 변경 감지) | 패치 후 반드시 실행 |
| `apply_font_mapping.py` | Unity_Font_Replacer의 `Twilight Struggle.json` Replace_to 47개 재설정 (parse가 JSON 초기화하므로 항상 재실행) | 폰트 주입 시 필수 |

**파이프라인 순서**: `inject_translations.py` → `add_ko_columns.py` → (`patch_scenes.py`) → 폰트 주입(apply_font_mapping.py 포함) → `verify_assets.py` → 설치

## 2️⃣ 보조 도구 (재실행 시 필요)

| 스크립트 | 용도 | 언제 |
|---|---|---|
| `analyze_scene_texts.py` | 씬 하드코딩 텍스트 추출 + 번역 매칭 분석 (미매칭 보고) | 게임 업데이트로 씬이 바뀌었을 때 |
| `extract_textassets.py` | 에셋에서 TextAsset 본문 추출 (읽기 전용) | 구조 조사, 번역 소스 갱신 시 |
| `extract_charset.py` | 번역 소스 ko 필드에서 사용 글자 문자셋 추출 → `fonts/chars.txt` | 새 번역 추가로 글리프 누락 시 |
| `backup-original.sh` | 게임 원본 → `original/` 백업 (멱등) | 업데이트/실험 전 |
| `restore-original.sh` | `original/` → 게임 폴더 복원 (멱등) | 복구 절차 검증 시 |
| `install.sh` | **macOS 설치**: patched/ → Steam + 코드사인 자동 (멱등) | macOS 적용 시 |
| `install-windows.ps1` | **Windows 설치**: patched/ → Steam (백업 → 복사 → SHA256 검증, 멱등) | Windows 적용 시 |

## 3️⃣ 일회성 도구 (Phase 2 번역 소스 구축 — 완료, `archive/`에 보관)

> 재사용 가능성: 게임 업데이트로 원본 EN이 바뀌면 일부 재사용 (경로: `scripts/archive/`).
> 파이프라인에는 영향 없음. 이동 시 상대 경로 참조(`parent.parent`)는 수정돼 있음.

| 스크립트 | 용도 | Phase |
|---|---|---|
| `archive/extract_original_en.py` | 원본 TextAsset에서 (행 키, EN 원문) 추출 | 2 |
| `archive/extract_bluechip_kr.py` | 블루칩 v1.0.1 MonoBehaviour에서 한글 432개 추출 | 2 |
| `archive/extract_bluechip_lua.py` | 블루칩 twilight_cards.lua 카드 정의 추출 | 2 |
| `archive/extract_runtime_tsv.py` | 신규 런타임 패치 TSV → 비교용 JSON | 2 |
| `archive/match_runtime_translations.py` | TextAsset EN 행 ↔ 런타임 번역 전체 문자열 매칭 | 2 |
| `archive/match_remaining.py` | 미일치 행을 런타임 TSV/블루칩과 매칭 (제목·설명) | 2 |
| `archive/apply_runtime_matches.py` | 검증된 매칭을 strings.json/cards.json에 반영 | 2 |
| `archive/apply_manual_translations.py` | Common_Strings 235행 수동 번역 적용 | 2 |
| `archive/apply_all_translations.py` | Phase 2 최종 — 모든 번역을 strings.json/cards.json에 반영 | 2 |

## 4️⃣ 삭제됨 (2026-08-12 정리)

| 스크립트 | 삭제 사유 |
|---|---|
| `patch_textasset.py` | raw `str.replace` 기반 구식 치환 도구 → `inject_translations.py`(키/셀 단위)가 완전 대체. 짧은 토큰 측면 치환 위험도 있음 |
| `install-lua-test.sh` | Lua 대상 실험. Phase 1에서 `StreamingAssets/Lua`가 죽은 잔재로 확인되어 작업 대상 제외 |
| `install-asset-test.sh` | Phase 1 단일 에셋 적용 실험. `install.sh`(전체 복사)가 표준 |
| `.gitkeep` | 스크립트가 전부 git 추적되므로 불필요 |

---

## 실행 주의사항

- **절대 Steam 설치 폴더를 직접 수정하지 않는다** — patched/ 또는 가상 폴더(`tools/font-inject-work/`)에서 작업 후 설치 스크립트로 적용
- venv python 필수: 시스템 python은 UnityPy 포크/typetree_generator 없음
- 셸 스크립트는 macOS 경로 기준 (`GAME_DIR` 환경변수로 재정의 가능)
- 최신 절차는 `.pi/skills/twilight-struggle-update/`·`twilight-struggle-font-swap/` 스킬 참조
