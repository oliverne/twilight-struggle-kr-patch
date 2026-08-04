# 진행 상황 (Progress)

> Phase 반복 프로세스에 따라 **이 문서를 항상 함께 업데이트**한다. (규칙: AGENTS.md)
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**Phase 0 — 준비** (🚧 진행 중) · 최종 업데이트: 2026-08-04
> 남은 항목: 기존 패치 확보 (수동 다운로드 필요)

---

## Phase 0 — 준비 🚧

### 체크리스트
- [x] Git 저장소 초기화
- [x] 저장소 디렉터리 스켈레톤 + `.gitignore` (commit `0abad37`)
- [x] 게임 설치 확인: v1.4.11, build-guid `beff29feda834098ab218792d4d80249`
- [x] .NET 8 설치 (`brew install dotnet`) — 실제로는 .NET 10.0.302 설치
- [x] UABEA 설치 → `tools/uabea/` + 기동 확인
- [x] Python venv + numpy/scipy/Pillow 설치
- [x] 원본 백업 → `original/` (resources.assets, level0~3, StreamingAssets, globalgamemanagers*) — 24MB
- [x] `original/hashes.txt` (sha256) + `original/VERSION.txt` 기록
- [ ] 기존 패치 다운로드 (블루칩 v1/v2, 한패) → `tools/legacy-patches/`

### 검증 결과
| 항목 | 방법 | 결과 |
|---|---|---|
| 게임 설치/버전 | `Info.plist`, `boot.config` 읽기 | ✅ v1.4.11, build-guid `beff29feda834098ab218792d4d80249` |
| Lua 파일 존재 | `ls`, `wc -l` | ✅ 6개 파일, `twilight_cards.lua` 3,764줄 |
| 스켈레톤 구조 | `git status` clean + PLAN §3 대조 | ✅ commit `0abad37` |
| dotnet 설치 | `dotnet --version` | ✅ 10.0.302 |
| UABEA 기동 (macOS) | 프로세스 12초 생존 확인 | ✅ 성공 — 공식 macOS 빌드 없음 → ubuntu 빌드 + macOS 네이티브 dylib 3종 보강(SkiaSharp/HarfBuzzSharp/AvaloniaNative) + `DOTNET_ROLL_FORWARD=LatestMajor` 필요. 재현: `scripts/setup-uabea-mac.sh` |
| Python venv | `import numpy, scipy, PIL` | ✅ numpy 2.0.2 / scipy 1.13.1 / Pillow 11.3.0 |
| 원본 백업 무결성 | `shasum -a 256 -c hashes.txt` + 게임 원본 직접 대조 | ✅ 14개 파일 전부 일치 (직접 대조 시 초기 스크립트 grep 오탐 있었으나 실해시 동일 확인) |

### 다음 Phase로 핸드오프
> Phase 0 완료 시 작성: 도구 버전, 백업 위치/해시, 기존 패치에서 확인한 번역 파일 목록 등
> (임시) UABEA 실행: `DOTNET_ROLL_FORWARD=LatestMajor dotnet tools/uabea/UABEAvalonia.dll` — GUI는 실사용 시 수동 실행 필요
> (임시) 원본 백업: `original/` 24MB, 14파일, 무결성 검증 완료. 복원: `original/` → 게임 Data 폴더로 역복사

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
| 2026-08-04 | 도구 설치 완료 (dotnet 10, UABEA v8, Python venv) | — |
| 2026-08-04 | Phase 반복 프로세스(검증·핸드오프) 명시 | `79a029d` |
| 2026-08-04 | 도구 설치: dotnet 10.0.302 · UABEA v8(macOS 보강) · Python venv | 이번 커밋 |
