# 진행 상황 (Progress)

> 이 문서는 전체 진행 상태를 빠르게 파악하기 위한 인덱스다.
> Phase별 검증 상세, 결정 사항, 산출물, 핸드오프의 원본은 [`docs/phases/`](phases/) 아래 문서에 기록한다.
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**다음 작업:** 미번역 텍스트 전체 확인 (4차 테스트 — 대부분 UI/카드 한글화 확인 완료)

- 완료: Phase 0 — 준비, Phase 1 — 텍스트 위치 검증, Phase 2 — 번역 소스 구축
- 완료: Phase 3 SDF 생성 (2048² 최적화) + Windows 폰트 주입 (24개 TMP 폰트)
- 완료: Phase 4 텍스트 주입 재구축 (m_Script 무손상) + **잔존 키 53개 수동 번역 재주입**
- 완료: **Windows 실게임 1차 테스트 + 진단** — 메뉴 영어 원인 3계층 규명
- 완료: **씬 패치 (level1-3)** — 하드코딩 문자열 2,548개 한글화
- 완료: **게임 언어 KO 전환** (레지스트리) + 2차 테스트 (카드 키 노출 발견)
- 완료: **2차 후속 — 5개 언어 테이블 KO 열 추가 + SDF 문자셋 확장 (739자) 재주입**
- 완료: **3차 후속 — KO 열 원본 범위 내 재배치 (8/9/10열)** — 파서가 원본 밖 열 무시 확인
- ✅ **4차 테스트 — 대부분의 UI·카드 한글화 확인 (2026-08-12)**
- ✅ **폰트 교체 — 제목 Paperlogy 5 Medium, 본문 D2Coding Regular (2026-08-12)**
- ✅ **폰트 크기 조절 — m_PointSize 70→77 (~9% 축소), 줄 간격 유지 (2026-08-12)**
- **Phase 5 잔여: 미번역 텍스트 전체 확인 → macOS 적용 → 멀티플레이 → 설치 스크립트**

### 작업 재개 순서

1. **미번역 텍스트 전체 확인** — 인게임 전 화면/팝업을 돌며 영어 잔존 수집 → `translation/manual-*.json`에 추가 → 재주입 (KO 열 값은 EN 열 값 복사라 EN 열만 교체하면 자동 반영)
2. 잔존 `□` 확인 → `fonts/chars.txt`에 글자 추가 → SDF 재생성 → 재주입
3. macOS로 `patched/` 전체(level 포함) 전송 → `scripts/install.sh` → 테스트
4. Windows 설치 스크립트(`install-windows.ps1`) 작성 → 멀티플레이 테스트

## 핵심 확정 사항

- 실제 텍스트 소스는 `resources.assets` 내 TextAsset이다.
- `Common_Strings`와 `TS_Cards`는 실게임 반영이 확인됐다.
- `StreamingAssets/Lua`는 죽은 잔재 파일이므로 작업 대상에서 제외한다.
- 한글 입력과 인코딩은 정상이나 기존 SDF 폰트에 CJK 글리프가 없어 게임에서 `ㅁ`으로 표시된다.
- **번역 주입 방식: EN 열 보존 + RU(10열)→KO 교체 + AvailableCultures에 ko 등록 + 모든 언어 테이블에 KO 열 추가.**
  SmartLocalization이 언어별 열 헤더("EN"/"KO")로 해석하므로, 언어=KO에서도 한글이 표시되려면
  **모든 테이블(TS_Cards·TS_Ingame·TS_Strings·Common_Ingame·TS_RulesTutorial)에 KO 열이 필요**
  (Common_Strings만 KO 열이면 메뉴만 한글, 카드/스코어링은 ${Key} 노출 — 2차 테스트에서 확인).
  `scripts/add_ko_columns.py`가 KO 열을 추가·유지한다.
  ⚠️ **KO 열은 반드시 원본에 존재하는 열 번호 범위 내의 빈 열에 배치** (TS_Cards 9, 나머지 8~10).
  원본에 없는 열 번호(27열 등)에 셀을 추가하면 게임 파서가 무시한다 (3차 테스트 확인).
- **번역 재사용 소스: 신규 런타임 패치 `runtime_exact.tsv` (2,253쌍).** 블루칩 v1.0.1의 MonoBehaviour 한글(432개)은 v1.0.1에 `Common_Strings`/`TS_Cards`가 없어 매칭 불가. 런타임 TSV + 수동 번역으로 666행 전체 커버.
- **게임 텍스트 3계층 구조** (Phase 5 확정):
  1. TextAsset 키 참조 (`${Key_XXX}`) — 언어=ko에서 KO 열 사용 → 번역 주입 + 언어 설정으로 해결
  2. 씬 하드코딩 문자열 (level1-3 MonoBehaviour) — **씬 패치(`patch_scenes.py`)로 해결**
  3. IL2CPP 코드 문자열 (global-metadata.dat, 턴 히스토리 템플릿) — BepInEx 런타임 훅 필요, 보류
- **게임 언어 저장 위치: `HKCU\Software\Playdek\TwilightStruggle` 레지스트리 `localization_h2525087814`** (PlayerPrefs) — KO로 변경 완료. **설치 스크립트가 파일 복사와 함께 자동으로 KO 설정** (Windows: 레지스트리 / macOS: `~/Library/Preferences/unity.Playdek.TwilightStruggle.plist` plist)
- **배포물은 `scripts/package-release.sh`가 생성하는 zip 2종** (사용자용 ~9MB / 재현용 ~3MB, SHA256SUMS 포함). `patched/*.assets`는 100MB 제한으로 gitignore지만 **압축 시 104MB→~8MB**라 GitHub Releases 첨부(파일당 2GB)로 충분 — gitignore는 Releases 업로드와 무관
- **SDF 폰트 교체 도구: [Unity_Font_Replacer](https://github.com/snowyegret23/Unity_Font_Replacer) v1.2.8.** `make_sdf.py`로 TTF→SDF 생성, `unity_font_replacer_ko.exe`로 게임 에셋 자동 교체.
- **⚠️ UnityPy(공식) `env.file.save()`는 IL2CPP 게임에서 MonoBehaviour m_Script 참조를 재매핑해 TMP 폰트를 파괴한다** (Phase 4 기존 patched가 m_Script 11,890건 손상). → 포크 UnityPy + TypeTreeGeneratorAPI(typetree_generator) 방식으로 재구축 완료.
- **⚠️ UnityPy 저장 시 로드 파일과 저장 파일은 분리해야 한다** — 같은 경로 저장 시 지연 스트리밍(Replacer)이 깨져 EOFError 발생 (씬 패치에서 확인).
- **폰트 주입 검증: m_Script 0건/raw 0건 불일치.** `scripts/verify_assets.py`로 재검증 가능.

## Phase 요약

| Phase                                  | 상태 | 요약                                           | 상세 기록                                    |
| -------------------------------------- | ---- | ---------------------------------------------- | -------------------------------------------- |
| Phase 0 — 준비                         | ✅   | 도구 설치, 원본 백업, 기존 패치 확보 완료      | [상세](phases/phase-0-preparation.md)        |
| Phase 1 — 텍스트 위치 검증             | ✅   | `resources.assets`가 실제 텍스트 소스임을 확인 | [상세](phases/phase-1-source-validation.md)  |
| Phase 2 — 문자열 추출 & 번역 소스 구축 | ✅   | 666/666행 번역 완료. 런타임 TSV + 수동 번역     | [상세](phases/phase-2-translation-source.md) |
| Phase 3 — 한글 SDF 폰트 아틀라스 생성  | ✅   | 2048² SDF 2종 + Windows 주입 완료 (24개 폰트) | [상세](phases/phase-3-sdf-font.md)           |
| Phase 4 — 텍스트 주입 & 레이아웃 조정  | ✅   | 무손상 주입 재구축 + 잔존 키 53개 재주입    | [상세](phases/phase-4-injection-layout.md)   |
| Phase 5 — 플랫폼 적용 & 테스트         | 🚧   | Windows 1차 테스트·씬 패치 완료, 재실행 대기. 설치 스크립트 언어 자동 설정 추가 | [상세](phases/phase-5-platform-test.md)      |
| Phase 6 — 배포                         | ⬜   | 사용자 안내 및 배포 대기                       | [상세](phases/phase-6-release.md)            |
| Phase 7 — 도움말/규칙 번역 (후순위)   | ⬜   | 배포 후 맨 마지막 수행 — 규칙 6.4만 자 수동   | [상세](phases/phase-7-help-translation.md)   |

## 현재 핸드오프 요약

- 수신: Windows 게임 머신 (2026-08-11 현재 작업 위치)
- **즉시 실행**: 게임 재실행 → 메뉴 한글화 확인 (언어=KO 적용됨) → Player.log에 `Load Language Header: KO` 확인
- 잔존 영어/`□` 확인 → `translation/manual-*.json`에 키 추가 후 재주입 (inject_translations.py / patch_scenes.py)
- macOS 적용: `patched/` 전체 전송(resources.assets, sharedassets0.assets, level1~3) → `scripts/install.sh`
- Windows 설치 스크립트(`install-windows.ps1`) 미작성 — Phase 5 체크리스트 항목
- 멀티플레이 테스트 미실시 — 필수
- **보류**: 턴 히스토리(IL2CPP 코드 문자열) — BepInEx 런타임 훅 프로젝트로만 해결 가능
- ~~보류: 폰트 크기 불일치~~ → **해결 (2026-08-12)**: m_PointSize 70→77로 ~9% 축소.
  m_Scale은 도구가 게임 값으로 덮어쓰므로 변경 불가 — 절차는 `.pi/skills/twilight-struggle-font-size`
- 주의: `patched/*.assets`는 GitHub 100MB 제한 초과로 gitignore — 재생성 방법은 Phase 문서 참조 (level1~3은 git 관리)

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
| 2026-08-05                                        | Phase 2 완료 — 666/666행 번역 적용                                | `9538590` |
| 2026-08-08                                        | Phase 3 SDF 생성 완료 + Windows Runbook 작성                      | `63fa852` |
| 2026-08-08                                        | 런타임 패치 바이너리 235개 gitignore 처리                          | `909820f` |
| 2026-08-08                                        | Phase 4 텍스트 주입 — 6종 TextAsset + install.sh                  | `0ba38c4` |
| 2026-08-08                                        | Phase 3·4 현황 반영 (PROGRESS)                                    | `12bdace` |
| 2026-08-11                                        | Windows 폰트 주입 완료 + m_Script 손상 발견·재구축 (예정)        | -         |
| 2026-08-11                                        | Windows 1차 테스트 진단 + 잔존 키 재주입 + 씬 패치 + 언어 KO     | `35c6cd3` |
| 2026-08-11                                        | 문서 일괄 갱신 (AGENTS/PLAN/README/ISSUES/CLEANUP + 핸드오프)   | `eba470a` |
| 2026-08-12                                        | 2차 테스트 후속: 5테이블 KO 열 추가 + SDF 문자셋 739자 재주입  | `91d0fbc` |
| 2026-08-12                                        | 3차 테스트 후속: KO 열 원본 범위 내 배치(8/9/10열) 재주입      | `438fe63` |
| 2026-08-12                                        | 4차 테스트 성공 — 대부분 UI·카드 한글화 확인, 문서 최신화      | `2ce6216` |
| 2026-08-12                                        | 폴더 정리(scripts/tools/translation) + README·스킬 갱신       | `a0cdff4` |
| 2026-08-12                                        | TextAsset 미번역 전수 조사(0건) + Windows 설치 스크립트        | `5f208a7` |
| 2026-08-12                                        | 설치 스크립트 언어 KO 자동 설정 (레지스트리/plist) + 문서 반영 | `e579de8` |
| 2026-08-12                                        | 배포 패키징 스크립트 작성 (zip 2종 + SHA256SUMS) + Phase 6 문서 반영 | (이번 커밋) |
| 2026-08-12                                        | 폰트 교체(Paperlogy/D2Coding) + 크기 축소 + 크기 조절 스킬 신설 | `405b17a` |
