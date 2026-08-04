# 진행 상황 (Progress)

> Phase 반복 프로세스에 따라 **이 문서를 항상 함께 업데이트**한다. (규칙: AGENTS.md)
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**Phase 1 — 텍스트 위치 검증** ✅ 완료 · 최종 업데이트: 2026-08-05
> 다음: Phase 2 — 문자열 추출 & 번역 소스 구축 (핸드오프 참조)

---

## Phase 0 — 준비 ✅

### 체크리스트
- [x] Git 저장소 초기화
- [x] 저장소 디렉터리 스켈레톤 + `.gitignore` (commit `0abad37`)
- [x] 게임 설치 확인: v1.4.11, build-guid `beff29feda834098ab218792d4d80249`
- [x] .NET 8 설치 (`brew install dotnet`) — 실제로는 .NET 10.0.302 설치
- [x] UABEA 설치 → `tools/uabea/` + 기동 확인
- [x] Python venv + numpy/scipy/Pillow 설치
- [x] 원본 백업 → `original/` (resources.assets, level0~3, StreamingAssets, globalgamemanagers*) — 24MB
- [x] `original/hashes.txt` (sha256) + `original/VERSION.txt` 기록
- [x] 기존 패치 다운로드 (블루칩 v1/v2) → `tools/legacy-patches/` — 한패는 중개 사이트로 블루칩과 동일한 Drive 링크 + 네이버 카페 링크(로그인 필요, 보류)

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| 게임 설치/버전 | `Info.plist`, `boot.config` 읽기 | ✅ v1.4.11, build-guid `beff29feda834098ab218792d4d80249` |
| Lua 파일 존재 | `ls`, `wc -l` | ✅ 6개 파일, `twilight_cards.lua` 3,764줄 |
| 스켈레톤 구조 | `git status` clean + PLAN §3 대조 | ✅ commit `0abad37` |
| dotnet 설치 | `dotnet --version` | ✅ 10.0.302 |
| UABEA 기동 (macOS) | 프로세스 12초 생존 확인 | ✅ 성공 — 공식 macOS 빌드 없음 → ubuntu 빌드 + macOS 네이티브 dylib 3종 보강(SkiaSharp/HarfBuzzSharp/AvaloniaNative) + `DOTNET_ROLL_FORWARD=LatestMajor` 필요. 재현: `scripts/setup-uabea-mac.sh` |
| Python venv | `import numpy, scipy, PIL` | ✅ numpy 2.0.2 / scipy 1.13.1 / Pillow 11.3.0 |
| 기존 패치 확보 | Google Drive 다운로드 + unzip 확인 | ✅ `bluechip-v1.0.1-v2.0.1.zip` (520MB) — 양 버전 resources.assets + Lua 추출 완료. Lua에 한글 번역 포함 확인 (UTF-8). 네이버 카페 백업(짜짜)은 로그인 필요로 보류 |

### 다음 Phase로 핸드오프
**도구**
- UABEA 실행: `DOTNET_ROLL_FORWARD=LatestMajor dotnet tools/uabea/UABEAvalonia.dll` (재현: `scripts/setup-uabea-mac.sh`)
- Python: `.venv/bin/python` (numpy 2.0.2 / scipy 1.13.1 / Pillow 11.3.0)

**원본 백업**
- `original/` 24MB, 14파일, 무결성 검증 완료 (v1.4.11, build-guid `beff29feda834098ab218792d4d80249`)
- 복원 방법: `scripts/restore-original.sh` (백업: `scripts/backup-original.sh`, 정리: [CLEANUP.md](CLEANUP.md))

**기존 패치 (번역 추출 대상)**
- `tools/legacy-patches/v1.0.1/TwilightStruggle_Data/` — 100% 한글화 버전 (v1.1.3 대상, TTF 방식)
- `tools/legacy-patches/v2.0.1/TwilightStruggle_Data/` — 멀티 유지 버전 (v1.4.2 대상)
- 양쪽 모두 `resources.assets` + `StreamingAssets/Lua/` 추출 완료, Lua에 한글 번역 포함 (UTF-8, CRLF)
- ⚠️ 기존 패치는 구버전(v1.1.3/v1.4.2) 대상 → 현재 게임(v1.4.11)과 문자열 대조 시 버전차 예상

## Phase 1 — 텍스트 위치 검증 ✅

### 체크리스트
- [x] 실험 A: Lua 카드 이름 변경 → 실게임 반영 확인 — ❌ 미반영
- [x] 실험 C: Lua 로드 경로 매핑 확인 — ❌ Lua는 죽은 코드
- [x] 실험 B: 에셋 `Common_Strings` / `TS_Cards` 문자열 변경 → 실게임 반영 확인 — ✅ 둘 다 반영됨
- [x] 살아있는 텍스트 소스 확정 → 주 작업 대상 기록

### 준비 상황
- 테스트 파일: `patched/StreamingAssets/Lua/twilight_cards.lua` — `Asia Scoring` 카드 이름을 `테스트카드_KR_아시아스코어링`으로 변경 (UTF-8, LF 유지)
- 적용 스크립트: `scripts/install-lua-test.sh` — 원본 해시 검증 후 복사 (멱등, 2회 실행 검증 완료)
- 적용 결과: 게임 폴더 Lua 변경 완료. 복원: `scripts/restore-original.sh`
- **확인 방법**: 게임 실행 → 새 게임 시작 → 손패에 Asia Scoring 카드 확인 시 이름이 `테스트카드_KR_아시아스코어링`으로 표시되는지

**실험 B 준비 (에셋 소스 발견)**
- AssetsTools.NET(UABEA 동봉)은 이 게임의 Unity 6 포맷 파싱 실패 (ClassId 전부 0) → **UnityPy(Python)** 로 전환, 파싱 성공
- `resources.assets` 내 TextAsset 18개 발견 — 핵심: `Common_Strings`(200KB, 323행, 열: Key/EN/FR/DE/ES/PL/PT/JP/IT/RU/NL/CH), `TS_Cards`(162KB), `TS_Strings`, `TS_Ingame`, `TS_RulesTutorial`(195KB)
- 텍스트 덤프: `tools/dump/*.txt` (git 제외)
- 수정 도구: `scripts/patch_textasset.py` (raw 편집 방식)
- ⚠️ **알려진 문제**: UnityPy가 자신이 저장한 파일을 다시 읽어 재저장하면 데이터 유실 → 항상 원본에서 한 번에 모든 치환 적용
- 테스트 파일: `patched/resources.assets` — TS_Cards 카드 이름 → `테스트카드_KR_아시아스코어링`, Common_Strings Key_PlayOffline EN → `[KR]오프라인_플레이_테스트`
- 적용: `scripts/install-asset-test.sh` (해시 검증, 멱등) — **게임에 적용됨**
- **확인 방법**: 게임 실행 → (1) 메인 메뉴 "Play Offline" 버튼 문구, (2) 새 게임에서 Asia Scoring 카드 이름
- 분기: 메뉴만 변경 → Common_Strings / 카드만 변경 → TS_Cards / 둘 다 → 둘 다 유효

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| 실험 A | Lua 수정 → 실게임 실행 | ❌ 실패 — 카드 이름 미반영 (`Asia Scoring` 그대로) |
| 실험 C (원인 분석) | `LoadLuaFile`/`twilight/database` 문자열을 GameAssembly.dylib·전체 에셋·global-metadata에서 검색 | ❌ 전부 0건 → StreamingAssets/Lua는 **죽은 잔재 파일**, 로드되지 않음. 반면 `Asia Scoring`은 `resources.assets`에 11회 존재 → 진짜 소스는 에셋 |
| 실험 B 준비 | UnityPy 파싱 + TextAsset 구조 확인 + 치환 + 무결성 검증 | ✅ 파싱 성공 (오브젝트 42,653개), 치환 후 재읽기 검증 통과 (byte_size 합계 13.13MB = 원본 동일) |
| 실험 B 실게임 | 수정 `resources.assets` 적용 후 게임 실행 | ✅ 성공 — **메뉴 문구·카드 이름 둘 다 변경됨** (두 소스 모두 유효). 한글은 `ㅁ`으로 깨져 표시 → 인코딩/주입은 정상, **SDF 폰트에 CJK 글리프가 없어 렌더링만 실패** (Phase 3 핵심 난제 확인) |

### 다음 Phase로 핸드오프

**확정된 텍스트 소스 (실험 B로 검증됨)**
- `resources.assets` 내 TextAsset — `Common_Strings`(메뉴/UI), `TS_Cards`(카드) 둘 다 실게임 반영 확인
- 기타 후보(미검증): `TS_Strings`, `TS_Ingame`, `Common_Ingame`, `TS_RulesTutorial`(튜토리얼·규칙) — Phase 2에서 사용 여부 확인
- `StreamingAssets/Lua`는 죽은 코드 — 작업 대상 아님

**문자열 포맷**
- 스프레드시트형 JSON: `"행:열"` 키 구조. 1행=헤더, 열1=키, 열2=EN (Common_Strings는 열3~12에 FR/DE/ES/PL/PT/JP/IT/RU/NL/CH)
- 첫 줄에 날짜 헤더 (예: `28 July, (22:46)`) 있음 — 치환 시 JSON 본문만 다룰 것
- UTF-8 한글 주입 성공 확인 (렌더링만 폰트 문제)

**수정 파이프라인 (검증 완료)**
- 추출·수정: UnityPy(Python) + `scripts/patch_textasset.py` (원본에서 한 번에 모든 치환 적용 — 재저장 시 데이터 유실 버그 있음)
- 적용: `scripts/install-asset-test.sh` 패턴 (해시 검증 후 복사, 멱등) — Phase 4에서 정식 install 스크립트로 발전
- 복원: `scripts/restore-original.sh`
- UABEA(AssetsTools.NET)는 이 게임의 Unity 6 포맷 파싱 불가 — 사용하지 말 것

**현재 게임 상태 및 재개 시 할 일**
- 게임에 테스트 문자열 2건 적용된 상태 (메뉴·카드) — 재개 시 `restore-original.sh`로 원본 복원 후 시작
- `patched/resources.assets`(테스트본)는 폐기하거나 Phase 2에서 재생성

**미해결 이슈 / 다음 단계 결정 필요**
1. `ㅁ` 현상 — Phase 3(SDF 폰트)에서 해결. 한글이 폰트까지 도달하므로 인코딩 이슈 아님
2. Phase 2와 Phase 3 병행 여부 — 글자셋 확정은 번역 이후 가능하나, 폰트 도구 검증(`make_sdf.py` 동작 여부·폰트 에셋 구조 파악)은 독립이라 병행 가능. 사용자 결정 대기
3. 기타 TextAsset(TS_Ingame 등)이 실제로 화면에 쓰이는지 — Phase 2 추출 시 병행 확인

**산출물 위치**
- 텍스트 덤프: `tools/dump/*.txt` (git 제외, 재생성: UnityPy로 TextAsset 추출)
- 원본 백업: `original/` (무결성 검증됨, v1.4.11)
- 기존 패치: `tools/legacy-patches/v1.0.1|v2.0.1/` (한글 번역 추출 대상)

## Phase 2 — 문자열 추출 & 번역 소스 구축 ⬜

### 체크리스트
- [ ] 영문 문자열 추출 → `translation/` JSON
- [ ] 기존 패치에서 한글 번역 추출
- [ ] 자동 매칭 (기존 번역 ↔ 현재 문자열)
- [ ] 용어 통일표 `translation/glossary.md`
- [ ] TMP 리치텍스트 태그 보존 규칙 수립

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

### 다음 Phase로 핸드오프
> 문자열 수, 매칭률, 미번역 분량, 사용 글자 수 등

## Phase 3 — 한글 SDF 폰트 아틀라스 생성 ⬜

### 체크리스트
- [ ] 사용 글자 문자셋 산출
- [ ] 대체 폰트 준비 (Noto Serif KR, Black Han Sans, Gugi, 나눔손글씨)
- [ ] SDF 아틀라스 생성 (`make_sdf.py` 우선, 실패 시 Unity Editor)
- [ ] 아틀라스 주입 (UABEA) + 게임 내 한글 출력 확인

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

### 다음 Phase로 핸드오프
> 아틀라스 크기, 주입 방법, Material 보정값, 잔존 □ 글자 목록 등

## Phase 4 — 텍스트 주입 & 레이아웃 조정 ⬜

### 체크리스트
- [ ] 번역 주입 스크립트 (반복 적용 가능)
- [ ] 레이아웃/줄바꿈 조정
- [ ] 튜토리얼·규칙 문서 번역

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

### 다음 Phase로 핸드오프
> 수정 파일 목록, 레이아웃 이슈 목록, 플랫폼별 주의사항

## Phase 5 — 플랫폼 적용 & 테스트 ⬜

### 체크리스트
- [ ] macOS: `scripts/install-mac.sh` + codesign 재서명 테스트
- [ ] Windows: `scripts/install-windows.ps1` 테스트
- [ ] 멀티플레이 동작 테스트
- [ ] Steam 무결성 확인 후 재설치 테스트

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

### 다음 Phase로 핸드오프
> 테스트 통과 범위, 알려진 이슈, 배포 포함 파일 목록

## Phase 6 — 배포 ⬜

### 체크리스트
- [ ] README 사용자 안내
- [ ] GitHub Releases / zip 배포
- [ ] 기존 패치 제작자 크레딧·연락

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

---

## 로그

| 날짜 | 내용 | 커밋 |
|---|---|---|
| 2026-08-04 | 프로젝트 계획서·에이전트 지침 작성 | `915feb2` |
| 2026-08-04 | 저장소 스켈레톤 + `.gitignore` | `0abad37` |
| 2026-08-04 | 진행 상황 문서 추가 및 업데이트 규칙 명시 | `8f51f42` |
| 2026-08-04 | Phase 반복 프로세스 명시 및 PROGRESS 구조 개편 | `79a029d` |
| 2026-08-04 | 도구 설치 완료 (dotnet 10, UABEA v8, Python venv) | `688838e` |
| 2026-08-04 | 원본 백업 + 무결성 검증 | `71e7609` |
| 2026-08-04 | 기존 패치 확보 (블루칩 v1/v2 zip, 한글 Lua 확인) → **Phase 0 완료** | `e55fa20` |
| 2026-08-04 | 백업/복원 스크립트화 + CLEANUP.md 추가 | `15e82e8` |
| 2026-08-04 | README 작성 | `aa02bf1` |
| 2026-08-04 | 실험 A 준비: 테스트 Lua + 적용 스크립트 → **Phase 1 착수** | `844cf75` |
| 2026-08-05 | 실험 A/C 실패 기록, UnityPy 도구 전환, 실험 B 적용 | `224e4fc` |
| 2026-08-05 | 실험 B 실게임 성공 (두 소스 유효, ㅁ 확인) → **Phase 1 완료** | 이번 커밋 |
| 2026-08-04 | 실험 A 준비: 테스트 Lua + 적용 스크립트 → **Phase 1 착수** | 이번 커밋 |
