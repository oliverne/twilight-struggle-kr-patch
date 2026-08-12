# Twilight Struggle 한글 패치 — 에이전트 지침

> 상세 계획은 [docs/PLAN.md](docs/PLAN.md) 참조. 이 파일은 핵심 원칙만 담는다.

## 커밋 규칙

- **Conventional Commits** 형식 사용: `type(scope): 설명`
- 메시지는 **한국어**로 작성
- 예: `docs: Phase 0 실행 계획 문서 추가`, `feat(scripts): macOS 설치 스크립트 작성`

## Phase 반복 프로세스

[PLAN.md](docs/PLAN.md)의 각 Phase는 아래 사이클로 진행한다. 전체 현황은 `docs/PROGRESS.md`에, 검증 상세와 핸드오프는 `docs/phases/phase-*.md`에 남긴다.

1. **착수**: `PROGRESS.md`와 해당 Phase 문서에서 상태를 🚧로 표시
2. **실행**: 체크리스트 항목을 순서대로 진행. 각 단계의 **검증 기준을 먼저 정하고 실행**
3. **검증 기록**: 검증 결과(성공/실패 + 근거)는 해당 Phase 문서의 `검증 결과` 표에 기록. 실패 시 원인·대응책도 함께 기록
4. **핸드오프**: Phase 완료 시 해당 Phase 문서에 `다음 Phase로 핸드오프` 섹션 작성 — 다음 Phase가 알아야 할 결정 사항, 산출물 위치, 미해결 이슈, 즉시 실행할 작업을 기록. `PROGRESS.md`에는 요약과 링크만 반영
5. **완료**: `PROGRESS.md`와 해당 Phase 문서의 상태를 ✅로 표시하고, `PROGRESS.md` 로그에 커밋 해시를 추가한 뒤 두 문서를 **같은 커밋에 포함해** 커밋

**문서 역할 규칙**:
- `PROGRESS.md`는 현재 상태, Phase별 한 줄 요약, 다음 작업, 핸드오프 링크를 제공하는 인덱스다.
- `docs/phases/phase-*.md`는 체크리스트, 검증 기준·결과, 결정 사항, 산출물, 미해결 이슈, 핸드오프의 원본이다.
- 상세 내용을 두 문서에 중복 기록하지 않는다. 핸드오프의 상세 내용은 Phase 문서를 기준으로 하고 `PROGRESS.md`에는 현재 작업에 필요한 요약과 링크만 둔다.

**게이트 규칙**: 검증 실패/미해결 이슈가 있으면 다음 Phase로 넘어가지 않는다. (단, 이슈를 핸드오프에 명시하고 보류 처리한 경우는 예외)

## 프로젝트 개요

- Steam Twilight Struggle(App ID 406290, Unity 6 / 6000.0.58f2, IL2CPP) 한글 패치 복원
- 핵심 난제: **CJK 글리프를 포함한 TMP SDF 폰트 아틀라스 주입** — 한글 네모(□)의 원인 → ✅ 해결 (Phase 3~4, 24개 폰트 주입)
- **남은 난제: IL2CPP 코드 문자열(global-metadata.dat)의 턴 히스토리 로그** — 파일 패치 불가, BepInEx 런타임 훅만 가능 (보류)
- 기존 패치(블루칩 v1/v2, 우드킹)의 **번역문을 재사용**하며, 처음부터 번역하지 않음

## 게임 텍스트 3계층 구조 (Phase 5 확정)

| 계층 | 위치 | 상태 | 해결 수단 |
|---|---|---|---|
| 1. TextAsset 키 참조 | `resources.assets` — Common_Strings/TS_Ingame 등 (`${Key_XXX}`) | ✅ 한글화 | 번역 주입 + **게임 언어=ko** (아래) |
| 2. 씬 하드코딩 문자열 | level1(메인 메뉴)·level2(인게임)·level3(보드) MonoBehaviour | ✅ 한글화 (2,548개) | `patch_scenes.py` |
| 3. IL2CPP 코드 문자열 | global-metadata.dat (턴 히스토리 템플릿 등) | ❌ 영어 잔존 | BepInEx 런타임 훅 (보류) |

## 불변 원칙

1. **Steam 폴더에서 직접 작업하지 않는다.** 수정 파일은 `patched/`, 원본 백업은 `original/`(git 제외)에 둔다.
2. 모든 패치는 **멱등한 설치 스크립트**(`scripts/install-*.sh`)로만 적용 — 백업 → 복사 → 재서명 순서 유지.
3. macOS는 수정 후 반드시 애드혹 재서명: `codesign --force --sign -`
4. 번역 소스(진짜 코드)는 `translation/`의 JSON/CSV로 관리. 텍스트 주입은 반복 실행 가능한 스크립트로만 수행.
5. UTF-8 일관 사용. 인코딩 깨짐 의심 시 게임 로드 테스트로 확인.
6. TMP 리치텍스트 태그(`<color>`, `<font="...">`, `<br>`, `<indent>`)는 보존한다.
7. 텍스처에 구워진 문자(보드맵 국가명 등)는 현재 범위에서 제외.
8. **EN 열은 보존하고 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않음 — 영문 폴백·원문 대조·번역 검수를 유지하고, 게임 언어 선택기가 한국어를 인식하도록 교체 대상 언어 열(또는 새 컬처)을 한글로 채운다.
9. **언어=KO에서 모든 텍스트가 한글이 되려면 모든 언어 테이블에 KO 열이 필요하다.** SmartLocalization은 언어별 열 헤더("EN"/"KO")로 해석한다. Common_Strings만 KO 열을 만들면 메뉴만 한글화되고, 카드/스코어링(TS_Cards·TS_Ingame 등)은 `${Key}`가 노출된다 (2026-08-12 2차 테스트 확인). `scripts/add_ko_columns.py`가 KO 열을 추가·유지한다. ⚠️ **KO 열은 원본에 존재하는 열 번호 범위 내 빈 열에 배치** (TS_Cards 9열, 나머지 8~10열) — 원본 밖 열 번호에 셀을 추가하면 파서가 무시한다 (3차 테스트 확인).
10. **JSON 저장 시 LF 강제 (CRLF 방지)** — Windows Python의 `write_text()`/`open('w')`는 `\n`을 `os.linesep`(`\r\n`)으로 변환해 저장한다 (2026-08-12 실측). `translation/*.json`을 저장하는 스크립트는 반드시 **LF 강제**: `open(path, 'w', encoding='utf-8', newline='\n')` 또는 `Path.write_text(text, encoding='utf-8', newline='\n')`을 사용한다. CRLF로 저장되면 (a) git status에 내용이 같아도 M 노이즈, (b) 커밋 시 CRLF/LF 혼재 위험. 판정 기준: `git diff --no-index --ignore-cr-at-eol <HEAD버전> <현재파일>`이 비어있으면 내용 동일(무해) — 단, **git이 autocrlf(input)로 정규화하므로 CRLF 저장 후에도 내용 손실은 없다.**

## 텍스트 소스 (우선순위)

| 소재 | 위치 | 난이도 |
|---|---|---|
| 다국어 문자열 테이블 | `resources.assets` 내 **Common_Strings** (키값 방식 `Key_XXX`) | 🟢 최우선 — ✅ 주입 완료 |
| 카드/국가 텍스트 | `resources.assets` 내 `TS_Cards` 등 TextAsset (`"행:열":"값"` JSON) | 🟢 실게임 반영 확인 — ✅ 주입 완료 |
| 인게임/도움말 키 | `TS_Ingame`·`TS_Strings`·`Common_Ingame` | 🟢 실게임 반영 확인 — ✅ 주입 완료 (잔존 53키 수동 번역 포함) |
| **씬 하드코딩 문자열** | level1~3 MonoBehaviour (TextMeshProUGUI.m_text, Text.m_Text) | 🟢 패치 완료 — `patch_scenes.py` |
| 번역 재사용 소스 | 블루칩 v1.0.1 MonoBehaviour string 필드 (432개 고유 한글) | 🟢 raw 바이트 수동 파싱으로 추출 가능 (Phase 2) |
| **IL2CPP 코드 문자열** | global-metadata.dat (턴 히스토리 로그 템플릿) | 🔴 파일 패치 불가 — BepInEx 런타임 훅 필요 (보류) |
| 카드/국가 Lua | `StreamingAssets/Lua/*.lua` | ❌ Phase 1에서 죽은 잔재로 확인, 작업 대상 아님 |
| SDF 폰트 아틀라스 | `resources.assets` (CJK 없음) | ✅ 해결 — 24개 폰트 주입 (Phase 3~4) |

⚠️ **작업 착수 전 필수**: 아직 사용 여부가 확인되지 않은 소스는 수정 → 실게임 반영 테스트로 "살아있는 소스"를 먼저 검증한다. Phase 1 결과 `StreamingAssets/Lua`는 작업 대상에서 제외한다.

### 번역 소스 재사용 전략 (Phase 2 확정)

- 블루칩 v1.0.1(100% 한글화)의 번역은 MonoBehaviour string 필드에 직접 주입돼 있다. UnityPy `obj.read()`는 IL2CPP 타입트리 불완전으로 실패하나, `obj.get_raw_data()`에서 Unity string 표준 레이아웃(`int32 len + bytes + pad4`)을 수동 파싱하면 432개 고유 한글 문자열을 추출할 수 있다 (카드 이름·본문·사건·TMP 태그 포함).
- 블루칩 v1.0.1 번역(Blueprint) + 원본 `TS_Cards`·`Common_Strings` 영문 원문을 **원문 전체 비교**로 매칭해 `translation/` 소스를 구축한다. 우드킹 패치는 보조/검증용(입수 안 해도 진행 가능).
- 블루칩 Lua(`twilight_cards.lua`)에는 한글 10줄(카드 3개 능력 설명 일부)만 있어 사실상 무의미.

## 게임 경로

- macOS: `~/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data/`
- Windows: `steamapps/common/Twilight Struggle/TwilightStruggle_Data/` (⚠️ **공백 없음** — 실측, 2026-08-11)
- 에셋 파일은 플랫폼 공용(동일 빌드) → 한쪽에서 수정한 파일은 다른 플랫폼에도 그대로 복사 가능
- **게임 언어 설정(PlayerPrefs)**: `HKCU\Software\Playdek\TwilightStruggle` 레지스트리 키 `localization_h2525087814` — `KO`로 설정해야 TextAsset KO 열이 로드됨 (`EN`이면 영어). 게임 내 설정 → Languages에서도 선택 가능. **설치 스크립트(`install-windows.ps1`/`install.sh`)가 파일 복사와 함께 자동으로 KO 설정** (Windows: 레지스트리, macOS: `~/Library/Preferences/unity.Playdek.TwilightStruggle.plist` plist)

## 주요 도구

- **UABEA** (에셋 추출/수정, 크로스플랫폼) — 문제 시 UABEANext/AssetRipper 대안
- **Unity_Font_Replacer** v1.2.8: `make_sdf.py`로 Unity 없이 TTF → TMP SDF 생성, Windows에서 `unity_font_replacer_ko.exe --parse/--list`로 에셋 주입 (⚠️ `oneshot`은 없음, `Managed` 폴더 제거 필요 — Runbook 참조)
- **번역 주입**: `scripts/inject_translations.py` (TextAsset) — 포크 UnityPy + typetree_generator 필수 (공식 UnityPy 저장 금지)
- **씬 패치**: `scripts/patch_scenes.py` (level1-3 하드코딩 문자열) — Unity 6 헤드 레이아웃 실측 기반 (m_text @ head_end+56 / +112)
- **번역 소스**: `translation/runtime-20260315.json`(런타임 TSV) + `manual-extra.json`(TextAsset 잔존키) + `manual-scenes.json`(씬 문자열)
- 폰트: Noto Serif KR(본문), Black Han Sans(제목), Gugi, 나눔손글씨 — 모두 재배포 허용 라이선스만 사용
- IL2CPP 바이너리 패치는 **최후의 수단** (턴 히스토리는 길이 제약으로 사실상 불가 → BepInEx 훅)

## 리스크 체크리스트

- Steam 무결성 확인/업데이트로 파일 원복 가능 → 스크립트 재적용 + 버전 해시 검증
- Unity 6 직렬화 포맷 변경 → 도구 파싱 실패 시 대안 도구로 전환
- SDF 아틀라스 용량 → 사용 글자만 추출한 문자셋 + 2048² 기준, 필요 시 분할
- 멀티플레이 버전 체크 → 에셋 교체 후 멀티 동작 반드시 테스트
- **UnityPy 저장 시 로드 파일 ≠ 저장 파일 필수** — 같은 경로 저장 시 지연 스트리밍(Replacer)이 깨져 EOFError
- **턴 히스토리(IL2CPP 코드 문자열)** — 파일 패치 불가, 기존 런타임 패치도 미커버 → BepInEx 훅 필요시 별도 프로젝트
- **폰트 크기 불일치** — 24개 원본 폰트 → 한글 2종 통일로 크기/줄 간격 차이. `--use-game-line-metrics` 재주입 또는 m_FaceInfo 배율 조정으로 보정 가능 (미적용)

## 저장소 구조

```
patched/      # 수정 파일 (git 관리) — resources.assets, sharedassets0.assets, level1~3
              # ⚠️ *.assets는 100MB 초과로 gitignore — 배포는 package-release.sh의 dist/ zip으로
original/     # 원본 백업 (git 제외)
dist/         # 배포 zip 산출물 (git 제외, scripts/package-release.sh가 생성)
translation/  # 번역 소스 JSON/CSV — runtime-20260315.json, manual-extra.json, manual-scenes.json (+ 용어표는 Phase 7 착수 시 신설 예정)
fonts/        # TTF 원본 + 생성된 SDF 산출물
scripts/      # install/verify/inject/patch 스크립트
docs/         # PLAN.md 등
```
