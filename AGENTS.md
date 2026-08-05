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
- 핵심 난제: **CJK 글리프를 포함한 TMP SDF 폰트 아틀라스 주입** — 한글 네모(□)의 원인
- 기존 패치(블루칩 v1/v2, 우드킹)의 **번역문을 재사용**하며, 처음부터 번역하지 않음

## 불변 원칙

1. **Steam 폴더에서 직접 작업하지 않는다.** 수정 파일은 `patched/`, 원본 백업은 `original/`(git 제외)에 둔다.
2. 모든 패치는 **멱등한 설치 스크립트**(`scripts/install-*.sh`)로만 적용 — 백업 → 복사 → 재서명 순서 유지.
3. macOS는 수정 후 반드시 애드혹 재서명: `codesign --force --sign -`
4. 번역 소스(진짜 코드)는 `translation/`의 JSON/CSV로 관리. 텍스트 주입은 반복 실행 가능한 스크립트로만 수행.
5. UTF-8 일관 사용. 인코딩 깨짐 의심 시 게임 로드 테스트로 확인.
6. TMP 리치텍스트 태그(`<color>`, `<font="...">`, `<br>`, `<indent>`)는 보존한다.
7. 텍스처에 구워진 문자(보드맵 국가명 등)는 현재 범위에서 제외.
8. **EN 열은 보존하고 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않음 — 영문 폴백·원문 대조·번역 검수를 유지하고, 게임 언어 선택기가 한국어를 인식하도록 교체 대상 언어 열(또는 새 컬처)을 한글로 채운다.

## 텍스트 소스 (우선순위)

| 소재 | 위치 | 난이도 |
|---|---|---|
| 다국어 문자열 테이블 | `resources.assets` 내 **Common_Strings** (키값 방식 `Key_XXX`) | 🟢 최우선 |
| 카드/국가 텍스트 | `resources.assets` 내 `TS_Cards` 등 TextAsset (`"행:열":"값"` JSON) | 🟢 실게임 반영 확인 |
| 번역 재사용 소스 | 블루칩 v1.0.1 `resources.assets` 내 **MonoBehaviour** string 필드 (432개 고유 한글) | 🟢 raw 바이트 수동 파싱으로 추출 가능 |
| 다국어 UI 문자열 | `resources.assets` 내 `Common_Strings` | 🟢 실게임 반영 확인 |
| UI/튜토리얼 | `resources.assets` 내 `TS_Ingame`·`TS_Strings`·`TS_RulesTutorial`·`Common_Ingame` | 🟡 사용 여부 미검증 |
| 카드/국가 Lua | `StreamingAssets/Lua/*.lua` | ❌ Phase 1에서 죽은 잔재로 확인, 작업 대상 아님 |
| SDF 폰트 아틀라스 | `resources.assets` (CJK 없음) | 🔴 핵심 장벽 |

⚠️ **작업 착수 전 필수**: 아직 사용 여부가 확인되지 않은 소스는 수정 → 실게임 반영 테스트로 "살아있는 소스"를 먼저 검증한다. Phase 1 결과 `StreamingAssets/Lua`는 작업 대상에서 제외한다.

### 번역 소스 재사용 전략 (Phase 2 확정)

- 블루칩 v1.0.1(100% 한글화)의 번역은 MonoBehaviour string 필드에 직접 주입돼 있다. UnityPy `obj.read()`는 IL2CPP 타입트리 불완전으로 실패하나, `obj.get_raw_data()`에서 Unity string 표준 레이아웃(`int32 len + bytes + pad4`)을 수동 파싱하면 432개 고유 한글 문자열을 추출할 수 있다 (카드 이름·본문·사건·TMP 태그 포함).
- 블루칩 v1.0.1 번역(Blueprint) + 원본 `TS_Cards`·`Common_Strings` 영문 원문을 **원문 전체 비교**로 매칭해 `translation/` 소스를 구축한다. 우드킹 패치는 보조/검증용(입수 안 해도 진행 가능).
- 블루칩 Lua(`twilight_cards.lua`)에는 한글 10줄(카드 3개 능력 설명 일부)만 있어 사실상 무의미.

## 게임 경로

- macOS: `~/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data/`
- Windows: `steamapps/common/Twilight Struggle/Twilight Struggle_Data/`
- 에셋 파일은 플랫폼 공용(동일 빌드) → 맥에서 수정한 파일은 Windows에도 그대로 복사 가능

## 주요 도구

- **UABEA** (에셋 추출/수정, 크로스플랫폼) — 문제 시 UABEANext/AssetRipper 대안
- **Unity_Font_Replacer**: `make_sdf.py`로 Unity 없이 TTF → TMP SDF 생성 (우선 시도)
- 폰트: Noto Serif KR(본문), Black Han Sans(제목), Gugi, 나눔손글씨 — 모두 재배포 허용 라이선스만 사용
- IL2CPP 바이너리 패치는 **최후의 수단**

## 리스크 체크리스트

- Steam 무결성 확인/업데이트로 파일 원복 가능 → 스크립트 재적용 + 버전 해시 검증
- Unity 6 직렬화 포맷 변경 → 도구 파싱 실패 시 대안 도구로 전환
- SDF 아틀라스 용량 → 사용 글자만 추출한 문자셋 + 4096² 기준, 필요 시 분할
- 멀티플레이 버전 체크 → 에셋 교체 후 멀티 동작 반드시 테스트

## 저장소 구조

```
patched/      # 수정 파일 (git 관리)
original/     # 원본 백업 (git 제외)
translation/  # 번역 소스 JSON/CSV + 용어표
fonts/        # TTF 원본 + 생성된 SDF 산출물
scripts/      # install/uninstall/verify 스크립트
docs/         # PLAN.md 등
```
