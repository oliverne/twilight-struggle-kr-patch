# 진행 상황 (Progress)

> 이 문서는 전체 진행 상태를 빠르게 파악하기 위한 인덱스다.
> Phase별 검증 상세, 결정 사항, 산출물, 핸드오프의 원본은 [`docs/phases/`](phases/) 아래 문서에 기록한다.
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**다음 작업:** Phase 3 — 한글 SDF 폰트 아틀라스 생성 ⬜ 대기

- 완료: Phase 0 — 준비, Phase 1 — 텍스트 위치 검증, Phase 2 — 문자열 추출 & 번역 소스 구축
- 다음 실행: Phase 2 핸드오프를 읽고 사용 글자 추출 → SDF 폰트 아틀라스 생성
- 현재 차단 이슈: 없음
- 주요 후속 이슈: TS_Ingame 등 추가 TextAsset 사용 여부는 Phase 4에서 확인
- 보류 이슈: 처리 보류한 경고·정보 이슈는 [`docs/ISSUES.md`](ISSUES.md) 참조

### 작업 재개 순서

1. [Phase 2 상세 및 Phase 3 핸드오프](phases/phase-2-translation-source.md#다음-phase로-핸드오프)
2. `scripts/restore-original.sh`로 테스트 상태 복원 여부 확인
3. [Phase 3 상세 계획](phases/phase-3-sdf-font.md)

## 핵심 확정 사항

- 실제 텍스트 소스는 `resources.assets` 내 TextAsset이다.
- `Common_Strings`와 `TS_Cards`는 실게임 반영이 확인됐다.
- `StreamingAssets/Lua`는 죽은 잔재 파일이므로 작업 대상에서 제외한다.
- UnityPy로 에셋을 수정한다. 항상 원본에서 한 번에 치환하고, UnityPy가 저장한 파일을 다시 입력으로 재저장하지 않는다.
- 한글 입력과 인코딩은 정상이나 기존 SDF 폰트에 CJK 글리프가 없어 게임에서 `ㅁ`으로 표시된다.
- **번역 주입 방식: EN 열은 보존하고 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않아 영문 폴백·검수가 가능하며, 게임 언어 선택기가 한국어를 인식하도록 교체 대상 열(또는 새 컬처)에 한글을 채운다. 교체할 구체적 열과 컬처 등록(`AvailableCultures`)은 Phase 4에서 검증 결정한다.
- **번역 재사용 소스: 블루칩 v1.0.1 `resources.assets` 내 MonoBehaviour.** UnityPy `read()`는 IL2CPP로 실패하나 `get_raw_data()` + Unity string 표준 레이아웃 수동 파싱으로 432개 고유 한글 문자열 추출 가능. 원본 영문과 매칭해 `translation/` 구축. 우드킹 패치는 보조/검증용(입수 안 해도 진행 가능).

## Phase 요약

| Phase                                  | 상태 | 요약                                           | 상세 기록                                    |
| -------------------------------------- | ---- | ---------------------------------------------- | -------------------------------------------- |
| Phase 0 — 준비                         | ✅   | 도구 설치, 원본 백업, 기존 패치 확보 완료      | [상세](phases/phase-0-preparation.md)        |
| Phase 1 — 텍스트 위치 검증             | ✅   | `resources.assets`가 실제 텍스트 소스임을 확인 | [상세](phases/phase-1-source-validation.md)  |
| Phase 2 — 문자열 추출 & 번역 소스 구축 | ✅   | 666/666행 번역 완료. 런타임 TSV + 수동 번역     | [상세](phases/phase-2-translation-source.md) |
| Phase 3 — 한글 SDF 폰트 아틀라스 생성  | ⬜   | 사용 글자 기반 CJK SDF 생성 대기               | [상세](phases/phase-3-sdf-font.md)           |
| Phase 4 — 텍스트 주입 & 레이아웃 조정  | ⬜   | 번역 주입 및 UI 검증 대기                      | [상세](phases/phase-4-injection-layout.md)   |
| Phase 5 — 플랫폼 적용 & 테스트         | ⬜   | macOS·Windows·멀티플레이 검증 대기             | [상세](phases/phase-5-platform-test.md)      |
| Phase 6 — 배포                         | ⬜   | 사용자 안내 및 배포 대기                       | [상세](phases/phase-6-release.md)            |

## 현재 핸드오프 요약

Phase 3 착수 준비 완료. 상세는 [Phase 2 문서](phases/phase-2-translation-source.md#다음-phase로-핸드오프) 참조.

- 수신 Phase: Phase 3
- 선행 조건: `translation/strings.json` + `translation/cards.json` 666행 번역 완료
- 우선 작업: 번역문에서 고유 한글 글자 추출 → SDF 폰트 아틀라스 생성
- 사용 도구: Unity_Font_Replacer의 `make_sdf.py`
- 주의: 4096² 아틀라스로 CJK 글리프 수용 가능한지 먼저 확인

## 로그

| 날짜                                              | 내용                                                             | 커밋      |
| ------------------------------------------------- | ---------------------------------------------------------------- | --------- |
| 2026-08-04                                        | 프로젝트 계획서·에이전트 지침 작성                               | `915feb2` |
| 2026-08-04                                        | 저장소 스켈레톤 + `.gitignore`                                   | `0abad37` |
| 2026-08-04                                        | 진행 상황 문서 추가 및 업데이트 규칙 명시                        | `8f51f42` |
| 2026-08-04                                        | Phase 반복 프로세스 명시 및 PROGRESS 구조 개편                   | `79a029d` |
| 2026-08-04                                        | 도구 설치 완료 (dotnet 10, UABEA v8, Python venv)                | `688838e` |
| 2026-08-04                                        | 원본 백업 + 무결성 검증                                          | `71e7609` |
| 2026-08-04                                        | 기존 패치 확보 (블루칩 v1/v2, 한글 Lua 확인) → Phase 0 완료      | `e55fa20` |
| 2026-08-04                                        | 백업/복원 스크립트화 + CLEANUP.md 추가                           | `2a3c550` |
| 2026-08-04                                        | 실험 A 준비 및 Phase 1 착수                                      | `844cf75` |
| 2026-08-05                                        | 실험 B용 TextAsset 치환 도구 및 적용 스크립트 추가               | `224e4fc` |
| 2026-08-05                                        | 실험 A/C 실패 및 실험 B 준비 상황 기록                           | `acf3e19` |
| 2026-08-05                                        | 실험 B 실게임 성공 — 두 소스 유효, `ㅁ` 현상 확인 → Phase 1 완료 | `d135d1b` |
| 2026-08-05                                        | .NET 빌드 산출물 추적 제거, UnityPy 버전 pin, .gitignore 보강    | `chore`   |
| 2026-08-05                                        | asset-tool 문서화, Phase 2 번역 소스 키/셀 구조 설계             | `50feea1` |
| 2026-08-05                                        | 번역 소스 재사용 전략 및 EN 열 보존 원칙 문서 반영               | `4cad12e` |
| 2026-08-05                                        | pi --session 019fd212-0452-715f-b302-c395d2e19565                |           |
| codex resume 019fd729-445e-7021-9a9c-3fbf576fc1c2 |
