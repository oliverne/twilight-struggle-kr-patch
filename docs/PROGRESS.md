# 진행 상황 (Progress)

> Phase 반복 프로세스에 따라 **이 문서를 항상 함께 업데이트**한다. (규칙: AGENTS.md)
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**Phase 0 — 준비** ✅ 완료 · 최종 업데이트: 2026-08-04
> 다음: Phase 1 — 텍스트 위치 검증

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

## Phase 1 — 텍스트 위치 검증 ⬜

### 체크리스트
- [ ] 실험 A: Lua 카드 이름 변경 → 실게임 반영 확인
- [ ] 실험 C: Lua 로드 경로 매핑 확인 (A 실패 시)
- [ ] 실험 B: UABEA로 `Common_Strings` / `TS_Cards` 문자열 변경 → 실게임 반영 확인
- [ ] 살아있는 텍스트 소스 확정 → 주 작업 대상 기록

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

### 다음 Phase로 핸드오프
> 확정된 텍스트 소스 위치, 수정 방법, 주의사항

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
