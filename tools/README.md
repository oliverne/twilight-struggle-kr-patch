# tools/

폰트 주입·에셋 탐색 보조 도구 모음. `asset-tool/`·`unity-font-replacer/`의 일부 파일만 git 관리되고,
`font-inject-work/`는 로컬 전용(gitignore, 게임 에셋 파생물 다수 포함).

## 현재 구성 (2026-08-12 기준)

| 경로 | 용도 | 크기 | 상태 |
|---|---|---|---|
| `font-inject-work/` | **폰트 주입 작업 폴더** (로컬 전용, gitignore) | 322MB | 🟢 활성 |
| `unity-font-replacer/` | Unity_Font_Replacer v1.2.8 + 한글화 매핑 | 329MB | 🟢 활성 |
| `asset-tool/` | 에셋 탐색·덤프 (.NET, AssetsTools.NET) | 1.2MB | 🟡 보조 (UnityPy가 주도구) |

## font-inject-work/ (폰트 주입 워크스페이스)

| 항목 | 용도 | 비고 |
|---|---|---|
| `Twilight Struggle/` | 가상 게임 폴더 (Steam 게임의 사본) | 주입 대상. resources.assets는 최신 patched/로 교체 후 사용 |
| `ufr-src/` | Unity_Font_Replacer 파이썬 소스 (`make_sdf.py`, `unity_font_replacer_core.py` 등) | 스킬 `twilight-struggle-font-swap`이 참조 |
| `font-output-new2/` | **최신 폰트 주입 산출물** (resources/sharedassets0/globalgamemanagers) | ⚠️ KO 열 추가 **이전** 버전 — **현재 최종본은 `patched/`** |
| `probe_fonts.py`·`probe_names.py`·`probe_monoscripts.py` | TMP FontAsset 구조/클래스 조사 도구 | 재사용 가능 |
| `diff_assets.py` | original vs patched 객체 손상 비교 | verify_assets.py의 원형 |
| `test_fork_save.py`·`test_full_inject.py` | 포크 UnityPy 저장 무손상 검증 실험 | 참고용 |

> ⚠️ `font-output/`·`font-output-new/`(이전 산출물), `test-full.assets`·`test-save.assets`·`patched-DAMAGED-old.assets`(테스트/손상 파일), `Managed/Managed.off`·`Managed.bak`(이름변경 잔재)는 **2026-08-12 정리로 삭제** (재주입으로 재생성 가능).

## unity-font-replacer/ (폰트 교체 도구)

| 항목 | 용도 |
|---|---|
| `unity_font_replacer_ko.exe` | 폰트 주입 실행 파일 (--parse/--list/--output-only) |
| `export_fonts_ko.exe` | 폰트 내보내기 보조 exe |
| `Twilight Struggle.json` | 매핑 JSON — Replace_to 47개 (⚠️ parse가 초기화 → `scripts/apply_font_mapping.py` 재실행 필수) |
| `KR_ASSETS/` | 한글 SDF 자산 (NotoSerifKR·BlackHanSans SDF json/png/material + 원본 폰트) |
| `Il2CppDumper/` | IL2CPP 메타데이터 덤퍼 (폰트 스캔 보조) |
| `Unity_Font_Replacer_v1.2.8.zip` | 도구 원본 아카이브 (143MB, 백업용) |
| `CharList_3911.txt` | 기본 문자 목록 (chars.txt가 실제 사용) |
| `README.md`·`README_EN.md` | 원본 도구 설명 |

> ⚠️ `src/`는 gitignore (원본 소스). `verbose.txt`는 스캔 로그 (gitignore).

## asset-tool/ (에셋 탐색)

- Phase 1 실험 B용 읽기 전용 탐색 도구. `probe`\|`types`\|`list`\|`dump` 명령.
- `AssetsTools.NET.dll`을 `../uabea/`에서 HintPath 참조 → **`tools/uabea/` 없이는 빌드 불가** (현재 uabea 미설치, 필요 시 `scripts/setup-uabea-mac.sh`)
- 현재 텍스트 주입은 UnityPy 기반 `scripts/inject_translations.py`가 주도구 — 이 도구는 조사/대안용

## 필요 시 설치 (현재 없음)

| 경로 | 용도 | 설치 |
|---|---|---|
| `uabea/` | 에셋 추출/수정 GUI — UnityPy 포크 파싱 실패 시 대안 | `scripts/setup-uabea-mac.sh` |
| `legacy-patches/` | 기존 한글 패치 (블루칩 v1.0.1·v2.0.1 등) — 번역 추출 완료, 보존용 | [블루칩](https://bluechip2022.tistory.com/2) |
| `asset-ripper/` | UABEA 파싱 실패 시 대안 | [AssetRipper Releases](https://github.com/AssetRipper/AssetRipper/releases) |
| `dump/` | UnityPy/asset-tool 추출 텍스트 덤프 (git 제외) | 스크립트로 재생성 |

## 관련 문서

- 폰트 주입 절차: `.pi/skills/twilight-struggle-font-swap/SKILL.md`, `docs/runbooks/phase-3-windows-font-injection.md`
- 게임 업데이트 대응: `.pi/skills/twilight-struggle-update/SKILL.md`
- 파이프라인 스크립트: `scripts/README.md`
