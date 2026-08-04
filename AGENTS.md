# Twilight Struggle 한글 패치 — 에이전트 지침

> 상세 계획은 [docs/PLAN.md](docs/PLAN.md) 참조. 이 파일은 핵심 원칙만 담는다.

## 커밋 규칙

- **Conventional Commits** 형식 사용: `type(scope): 설명`
- 메시지는 **한국어**로 작성
- 예: `docs: Phase 0 실행 계획 문서 추가`, `feat(scripts): macOS 설치 스크립트 작성`

## Phase 반복 프로세스

[PLAN.md](docs/PLAN.md)의 각 Phase는 아래 사이클로 진행한다. 모든 기록은 `docs/PROGRESS.md`에 남긴다.

1. **착수**: PROGRESS.md에서 해당 Phase를 🚧로 표시
2. **실행**: 체크리스트 항목을 순서대로 진행. 각 단계의 **검증 기준을 먼저 정하고 실행**
3. **검증 기록**: 검증 결과(성공/실패 + 근거)를 Phase의 `검증 결과` 표에 기록. 실패 시 원인·대응책도 함께
4. **핸드오프**: Phase 완료 시 `다음 Phase로 핸드오프` 섹션 작성 — 다음 Phase가 알아야 할 결정 사항, 산출물 위치, 미해결 이슈
5. **완료**: Phase를 ✅로 표시, 로그 테이블에 커밋 해시 추가, **PROGRESS.md를 같은 커밋에 포함해** 커밋

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

## 텍스트 소스 (우선순위)

| 소재 | 위치 | 난이도 |
|---|---|---|
| 다국어 문자열 테이블 | `resources.assets` 내 **Common_Strings** (키값 방식 `Key_XXX`) | 🟢 최우선 |
| 카드/국가 Lua | `StreamingAssets/Lua/*.lua` (평문 ~6,500줄) | 🟢 쉬움 (단, 살아있는지 검증 필요) |
| UI/튜토리얼 | `resources.assets`, `level0~3` 씬 | 🟡 |
| SDF 폰트 아틀라스 | `resources.assets` (CJK 없음) | 🔴 핵심 장벽 |

⚠️ **작업 착수 전 필수**: 수정 → 실게임 반영 테스트로 "살아있는 소스"를 먼저 검증 (Lua는 잔재 파일일 수 있음)

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
