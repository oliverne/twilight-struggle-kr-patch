# 진행 상황 (Progress)

> 이 문서는 전체 진행 상태를 빠르게 파악하기 위한 인덱스다.
> Phase별 검증 상세, 결정 사항, 산출물, 핸드오프의 원본은 [`docs/phases/`](phases/) 아래 문서에 기록한다.
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**한글화 완료 (2026-08-13)** — 파일 패치 가능 범위 100% (계층 1 TextAsset + 계층 2 씬).
**Windows 배포 완료 (2026-08-14, v0.1.0)** — [GitHub Releases](https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.0). **macOS 배포 포함 v0.1.1 릴리스 완료 (2026-08-14)** — [v0.1.1](https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1)
남은 영어는 전부 계층 3(IL2CPP 코드 문자열: 턴 히스토리·튜토리얼 안내)로 BepInEx 런타임 훅 필요.

- 완료: Phase 0 — 준비, Phase 1 — 텍스트 위치 검증, Phase 2 — 번역 소스 구축
- 완료: Phase 3 SDF 생성 (2048² 최적화) + Windows 폰트 주입 (24개 TMP 폰트)
- 완료: Phase 4 텍스트 주입 재구축 (m_Script 무손상) + **잔존 키 52개 수동 번역 재주입**
- 완료: **Windows 실게임 1차 테스트 + 진단** — 메뉴 영어 원인 3계층 규명
- 완료: **씬 패치 (level1-3)** — 하드코딩 문자열 2,548개 한글화
- 완료: **게임 언어 KO 전환** (레지스트리) + 2차 테스트 (카드 키 노출 발견)
- 완료: **2차 후속 — 5개 언어 테이블 KO 열 추가 + SDF 문자셋 확장 (739자) 재주입**
- 완료: **3차 후속 — KO 열 원본 범위 내 재배치 (8/9/10열)** — 파서가 원본 밖 열 무시 확인
- ✅ **4차 테스트 — 대부분의 UI·카드 한글화 확인 (2026-08-12)**
- ✅ **폰트 교체 — 제목 Paperlogy 5 Medium, 본문 D2Coding Regular (2026-08-12)**
- ✅ **폰트 크기 조절 — m_PointSize 70→77 (~9% 축소), 줄 간격 유지 (2026-08-12)**
- ✅ **번역 다듬기 — humanizer 스캔(556건) → 일괄 교정 52개 + 런타임 장문 10개, grammar-checker 조사 오류 11건 교정 (2026-08-12)** — 상세: [translation-polish-review.md](translation-polish-review.md)
- ✅ **미번역 텍스트 화면 단위 확인 (2026-08-12)** — 사용자 실게임으로 대부분 한글 확인, 영어 잔존 미발견 (전수 조사는 미실시)
- ✅ **macOS 전체 파이프라인 재현 + 적용 완료 (2026-08-12)** — Windows 전송 없이 macOS에서 번역 주입→KO 열→폰트 주입→설치까지 전부 성공 (Windows 빌드 GameAssembly.dll + global-metadata.dat만 original/에 보관)
- ✅ **macOS 실게임 확인 (2026-08-12)** — 메뉴·카드 한글, 폰트 정상. 크래시 원인 해결: **Windows 원본 기준 씬 패치본(level1~3)이 macOS 빌드와 비호환** → macOS 원본 기준으로 재패치해 해결 (에셋도 플랫폼별 확인). 언어 키도 플랫폼별: macOS는 `localization`(plist), Windows는 `localization_h2525087814`(레지스트리)
- ✅ **Steam 무결성 재설치 테스트 (2026-08-12)** — 무결성 후 ${Key} 노출(원본 에셋+언어 KO) 확인 → uninstall.sh 정상 동작 → 언어 EN 복귀 → install.sh 재설치 확인. 배포 유저의 제거·복구 경로 확보 (uninstall 2종, `b16ea22`)
- ✅ **Phase 7 완료 (2026-08-13)** — 규칙북 313행 + 씬 규칙 문단 번역·주입·설치 완료. 튜토리얼 안내는 계층 3(IL2CPP)으로 보류
- ✅ **배포 보류 결정 (2026-08-13)** — 한글화는 여기까지로 마무리, 배포는 추후 재검토

### 작업 재개 순서

1. ~~macOS 적용~~ — ✅ 완료 (2026-08-12): macOS 파이프라인 재현 + 실게임 확인 (메뉴/카드 한글, 턴 히스토리 영어는 보류 — Windows와 동일)
2. ~~게임 실행 확인~~ — ✅ 메뉴·카드 한글 + 폰트 정상 (2026-08-12)
3. ~~Steam 무결성 확인 후 재설치 테스트~~ — ✅ 완료 (2026-08-12): ${Key} 노출 → uninstall.sh → EN 복귀 → 재설치 확인
4. Phase 6 배포 (package-release.sh 사용) — ✅ 플랫폼별 분리 완료: `patched/windows/`·`patched/macos/` (2026-08-14)

## 핵심 확정 사항

- 실제 텍스트 소스는 `resources.assets` 내 TextAsset이다.
- `Common_Strings`와 `TS_Cards`는 실게임 반영이 확인됐다.
- `StreamingAssets/Lua`는 죽은 잔재 파일이므로 작업 대상에서 제외한다.
- 한글 입력과 인코딩은 정상이나 기존 SDF 폰트에 CJK 글리프가 없어 게임에서 `ㅁ`으로 표시된다.
- **번역 주입 방식 (2026-08-14 개정 — EN 로케일 덮어쓰기): 모든 언어 테이블의 EN 열에 한글 주입** (Common_Strings 포함).
  게임 언어 설정(레지스트리/plist)은 **건드리지 않음** — 유저는 기본 언어 EN을 그대로 사용,
  **설치=한글, 제거=원본 복원 시 영어**가 된다. KO 열(8/9/10열)은 `add_ko_columns.py`가
  유지해 언어=KO로 설정된 구형 설치본과도 호환된다.
  (구방식: Common_Strings만 RU(10열)→KO 교체 + 언어=KO 설정 + 기록·복원 — 2026-08-14 폐기)
  ⚠️ KO 열은 반드시 원본에 존재하는 열 번호 범위 내의 빈 열에 배치 (TS_Cards 9, 나머지 8~10).
  원본에 없는 열 번호(27열 등)에 셀을 추가하면 게임 파서가 무시한다 (3차 테스트 확인).
- **번역 재사용 소스: 신규 런타임 패치 `runtime_exact.tsv` (2,253쌍).** 블루칩 v1.0.1의 MonoBehaviour 한글(432개)은 v1.0.1에 `Common_Strings`/`TS_Cards`가 없어 매칭 불가. 런타임 TSV + 수동 번역으로 666행 전체 커버.
- **게임 텍스트 3계층 구조** (Phase 5 확정):
  1. TextAsset 키 참조 (`${Key_XXX}`) — **EN 열에 한글 주입 (EN 로케일 덮어쓰기, 언어 설정 무조작)**
  2. 씬 하드코딩 문자열 (level1-3 MonoBehaviour) — **씬 패치(`patch_scenes.py`)로 해결**
  3. IL2CPP 코드 문자열 (global-metadata.dat, 턴 히스토리 템플릿) — BepInEx 런타임 훅 필요, 보류
- **게임 언어 설정: 설치/제거 스크립트는 언어 설정을 건드리지 않는다 (2026-08-14 확정).**
  EN 로케일 덮어쓰기 방식 — 유저는 기본 언어 EN 사용. 참고: 언어 저장 위치는
  Windows `HKCU\Software\Playdek\TwilightStruggle` 레지스트리 `localization_h2525087814`,
  macOS `~/Library/Preferences/unity.Playdek.TwilightStruggle.plist`의 `localization`.
  ⚠️ **게임 내 언어 선택 UI는 없음 (2026-08-12 실측)**. 언어=KO 구형 설정은 KO 열 덕분에 계속 한글 표시 (호환).
- **배포물은 `scripts/package-release.sh`가 생성하는 zip 3종** (windows/macos 사용자용 ~9MB + 재현용 ~3MB, SHA256SUMS 포함). **patched/는 플랫폼별 분리**: `patched/windows/`(Windows 원본 기준)·`patched/macos/`(macOS 원본 기준) — level1~3은 교차 복사 시 크래시 (2026-08-12 실측), resources.assets는 동일 빌드 전제 하에 공용. `patched/*/*.assets`는 100MB 제한으로 gitignore지만 **압축 시 104MB→~8MB**라 GitHub Releases 첨부(파일당 2GB)로 충분 — gitignore는 Releases 업로드와 무관
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
| Phase 4 — 텍스트 주입 & 레이아웃 조정  | ✅   | 무손상 주입 재구축 + 잔존 키 52개 재주입    | [상세](phases/phase-4-injection-layout.md)   |
| Phase 5 — 플랫폼 적용 & 테스트         | ✅   | **전부 완료 (2026-08-12)** — Windows 4차 테스트·macOS 실게임·Steam 무결성 복구·uninstall 검증. 잔여: 멀티플레이(스킵) | [상세](phases/phase-5-platform-test.md)      |
| Phase 6 — 배포                         | ✅   | **v0.1.1 릴리스 완료 (2026-08-14)** — Windows+macOS+src zip 3종 (실게임 확인 포함) | [상세](phases/phase-6-release.md)            |
| Phase 7 — 도움말/규칙 번역             | ✅   | **완료 (2026-08-13)** — 용어표·규칙 313행·씬 문단·500자 제한 수정 | [상세](phases/phase-7-help-translation.md)   |

## 현재 핸드오프 요약 (프로젝트 마감 — Phase 0~7 전부 완료)

- **한글화 완료 (2026-08-13)**: 계층 1(TextAsset)·계층 2(씬) 100% — 카드/메뉴/인게임 UI/규칙북/HELP/씬 규칙 문단 전부 한글
- **배포 완료 (2026-08-14)**: v0.1.0(Windows+src) → **v0.1.1(Windows+macOS+src)** — https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1. macOS 실게임 확인 포함. 배포 스킬에 버그 이력·검증 절차 반영
- **남은 영어 (전부 계층 3, 파일 패치 불가)**: ① 턴 히스토리 로그 (ISSUES #11) ② **튜토리얼 단계별 안내 (ISSUES #17)** ③ 보드맵 텍스처 국가명(범위 제외) — BepInEx 런타임 훅 프로젝트로만 해결 가능 (보류)
- 재적용: `scripts/install.sh` / 제거: `scripts/uninstall.sh` (Windows: `install-windows.ps1`/`uninstall-windows.ps1`) — Steam 업데이트/무결성 원복 시 `twilight-struggle-update` 스킬로 재적용
- 잔존 영어/`□` 발견 시 → `translation/manual-*.json`에 추가 → 재주입 (inject → add_ko → 필요시 폰트 → verify)
- **보류 이슈**: 배포 후 외부 사용자 설치 검증, 멀티플레이 검증, 폰트 줄 간격 보조 보정, ISSUES #6·#7·#9 — 상세는 phase-6 핸드오프 참조
- 주의: `patched/*/*.assets`는 GitHub 100MB 제한 초과로 gitignore — 재생성 방법은 Phase 문서 참조 (level1~3은 git 관리)

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
| 2026-08-05                                        | .NET 빌드 산출물 추적 제거, UnityPy 버전 pin, .gitignore 보강    | `fbb70bc` |
| 2026-08-05                                        | asset-tool 문서화, Phase 2 번역 소스 키/셀 구조 설계             | `50feea1` |
| 2026-08-05                                        | 번역 소스 재사용 전략 및 EN 열 보존 원칙 문서 반영               | `3779ea7` |
| 2026-08-05                                        | Phase 2 완료 — 666/666행 번역 적용                                | `9538590` |
| 2026-08-08                                        | Phase 3 SDF 생성 완료 + Windows Runbook 작성                      | `63fa852` |
| 2026-08-08                                        | 런타임 패치 바이너리 248개 gitignore 처리                          | `909820f` |
| 2026-08-08                                        | Phase 4 텍스트 주입 — 6종 TextAsset + install.sh                  | `0ba38c4` |
| 2026-08-08                                        | Phase 3·4 현황 반영 (PROGRESS)                                    | `12bdace` |
| 2026-08-11                                        | Windows 폰트 주입 완료 + m_Script 손상 발견·재구축 (예정)        | `fa8b241` |
| 2026-08-11                                        | Windows 1차 테스트 진단 + 잔존 키 재주입 + 씬 패치 + 언어 KO     | `35c6cd3` |
| 2026-08-11                                        | 문서 일괄 갱신 (AGENTS/PLAN/README/ISSUES/CLEANUP + 핸드오프)   | `eba470a` |
| 2026-08-12                                        | 2차 테스트 후속: 5테이블 KO 열 추가 + SDF 문자셋 739자 재주입  | `91d0fbc` |
| 2026-08-12                                        | 3차 테스트 후속: KO 열 원본 범위 내 배치(8/9/10열) 재주입      | `438fe63` |
| 2026-08-12                                        | 4차 테스트 성공 — 대부분 UI·카드 한글화 확인, 문서 최신화      | `2ce6216` |
| 2026-08-12                                        | 폴더 정리(scripts/tools/translation) + README·스킬 갱신       | `a0cdff4` |
| 2026-08-12                                        | TextAsset 미번역 전수 조사(0건) + Windows 설치 스크립트        | `5f208a7` |
| 2026-08-12                                        | 설치 스크립트 언어 KO 자동 설정 (레지스트리/plist) + 문서 반영 | `e579de8` |
| 2026-08-12                                        | 배포 패키징 스크립트 작성 (zip 2종 + SHA256SUMS) + Phase 6 문서 반영 | `d01141e` |
| 2026-08-12                                        | 폰트 교체(Paperlogy/D2Coding) + 크기 축소 + 크기 조절 스킬 신설 | `405b17a` |
| 2026-08-12                                        | 번역 다듬기 스킬 신설 + CRLF 정규화 (내용 무변화)             | `02497c2`, `986246f` |
| 2026-08-12                                        | 미번역 텍스트 화면 단위 확인 완료 (사용자 실게임, 전수 조사 미실시) | `5c5492a`, `5181950` |
| 2026-08-12                                        | **macOS 전체 파이프라인 재현** — Windows 전송 불필요 (GameAssembly.dll+metadata 2개만). venv 패치 2건·Il2CppDumper 스킵·metadata 플랫폼별 확인 + install.sh level1~3 버그 수정 | `4b53d1a`, `effbe84` |
| 2026-08-12                                        | **macOS 실게임 확인** — 크래시 원인(Windows 씬 패치본 비호환) 발견·해결, macOS 원본 기준 재패치. 언어 키 플랫폼별 확인 (macOS: localization) | `cb2dba0` |
| 2026-08-12                                        | **uninstall 스크립트 2종 + 설치 시 이전 언어 기록** — 제거 시 영문 복귀 지원 (게임 삭제·재설치/무결성 후 언어 잔존 시나리오 포함), 게임 내 언어 선택 UI 없음 실측 반영 | `b16ea22` |
| 2026-08-12                                        | **Phase 5 완료 처리** — Steam 무결성 복구·uninstall 검증 반영, Phase 6 핸드오프 작성 | `8a95a59` |
| 2026-08-13                                        | Phase 7 배포 전 수행으로 변경 + 착수 — 용어표·규칙 소스 추출 | `616b5b8` |
| 2026-08-13                                        | 용어표 전수 확정 (Control=장악 등, 검색+기존 번역 대조) | `b8122bd`, `8702616` |
| 2026-08-13                                        | TS_RulesTutorial 313행 전량 번역 (런타임 매칭 83% 재사용) | `9c31bb6` |
| 2026-08-13                                        | 주입 파이프라인 확장 + 폰트 문자셋 794자 재생성 | `2a0d7d9` |
| 2026-08-13                                        | 유사 매칭 오염 8건 교정 (Help_Help 팝업 제목 등) | `bcf2e18` |
| 2026-08-13                                        | 씬 규칙 문단 번역 — level2 +160개 객체 한글화 | `89bbe9b` |
| 2026-08-13                                        | parse_string_at 500자 제한 완화 — 긴 규칙 문단 번역 (level1 +17, level2 +12) | `02be348` |
| 2026-08-13                                        | 튜토리얼 안내 IL2CPP 코드 문자열 실측 — 계층 3 보류 (ISSUES #17) | `86aaa08` |
| 2026-08-13                                        | **Phase 7 완료 + 배포 보류 결정** — 한글화 마무리, 한계 문서화 | 본 커밋 |
| 2026-08-14                                        | Runbook 삭제 — 폰트 주입 절차를 twilight-struggle-font-injection 스킬로 이관 (참조 일괄 교체) | 본 커밋 |
| 2026-08-13                                        | **IMPACT SDF 3종 → D2Coding** — 트랙 첫 칸 H 넘침 해결 (원인: Paperlogy H 폭이 숫자보다 20% 넓음), 실게임 확인 완료 | `7ecf94e` |
| 2026-08-14                                        | **EN 로케일 덮어쓰기 전환 (언어 설정 무조작)** — Common_Strings EN 열(2열)에도 한글 주입, 설치/제거 스크립트에서 레지스트리·plist 조작·기록·복원 전부 제거. 유저는 기본 EN 사용 → 설치=한글, 제거=영어. KO 열은 구형 KO 설정 호환으로 유지 | 본 커밋 |
| 2026-08-14                                        | **EN 로케일 실게임 검증 완료 (Windows)** — 레지스트리 EN 설정에서 메뉴/카드 한글 확인. Steam 위치 자동 탐색 추가 (레지스트리+VDF, D 드라이브 검증) | `64a512f`, `e9cf6dd` |
| 2026-08-14                                        | **patched 플랫폼별 분리** — `patched/windows/`(Windows 원본 기준)·`patched/macos/`(macOS 재생성 예정), install 스크립트 경로 갱신, inject/patch_scenes에 `--platform` 인자, package-release.sh zip 3종(windows/macos/src) 개편 | 본 커밋 |
| 2026-08-14                                        | **배포 라이선스 정리** — README '감사의 말' 섹션 추가(한식구·블루칩), package-release.sh가 LICENSE를 LICENSE.txt로 자동 포함(사용자·src zip), 스킬/Phase 6 문서의 CREDITS.md·경고 설명 불일치 정리 | 본 커밋 |
| 2026-08-14                                        | **Windows 배포 (v0.1.0)** — 패키징·SHA256SUMS 검증·gh release 생성 완료. [릴리스](https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.0) (windows 9.3MB + src 3.6MB). macOS는 패치본 미생성으로 제외, 추후 릴리스 예정 | 본 커밋 |
| 2026-08-14                                        | **zip 레이아웃 버그 수정** — zip 내부를 `patched/<플랫폼>/` 구조로 변경 (설치 스크립트 경로와 불일치하던 버그, v0.1.0 zip 영향). `patched/windows/` 대형 에셋은 v0.1.0 릴리스 zip에서 복원. 잔재 `patched-mac/` 삭제 + gitignore 정리 | `aab7c7f` |
| 2026-08-14                                        | **macOS 패치본 재생성 완료** — EN 로케일 방식 파이프라인 재실행 (macOS 원본 기준): 번역 주입(322행)→KO 열→씬 패치(902/1563/274)→폰트 주입(verify 90건)→`patched/macos/` 완성 + hashes.txt. macOS zip 패키징 검증(v0.1.1-test) + install.sh 설치·코드사인 완료. v0.1.1 릴리스 대기 | `9627c8e` |
| 2026-08-14                                        | **v0.1.1 릴리스** — Windows+macOS+src zip 3종 (macOS 10MB·Windows 9MB·src 16MB). SHA256SUMS 자기 자신 포함 버그 수정(`find ! -name SHA256SUMS`) + 전체 검증 완료. [릴리스](https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1) | `7587793` |
| 2026-08-14                                        | **release 스킬 현행화** — 릴리스 이력·zip `patched/<플랫폼>/` 구조 검증·SHA256SUMS 검증 절차 반영 | `e36fe80` |
| 2026-08-14                                        | **Phase 6 완료 + 프로젝트 마감** — v0.1.1 배포(실게임 확인 포함)·버그 수정 2건 완료 처리, phase-6 핸드오프(보류 이슈 정리) 작성. Phase 0~7 전부 ✅ | 본 커밋 |
