# Phase 0 — 준비

## 상태

- 상태: ✅ 완료
- 완료일: 2026-08-04
- 관련 커밋: `e55fa20`

## 목표

작업 저장소를 구성하고, 현재 게임 버전의 원본과 기존 한글 패치를 확보하며, 에셋 분석·수정에 필요한 도구를 준비한다.

## 체크리스트

- [x] Git 저장소 초기화
- [x] 저장소 디렉터리 스켈레톤 및 `.gitignore` 구성
- [x] 게임 설치 및 버전 확인
- [x] .NET 및 UABEA 설치·기동 확인
- [x] Python venv 및 `numpy`/`scipy`/`Pillow` 설치
- [x] 패치 대상 원본 백업 및 해시 기록
- [x] 블루칩님 기존 패치 v1/v2 확보
- [ ] 한패(hanpe.net) 백업 확보 — 로그인 필요로 보류

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| 게임 설치/버전 | `Info.plist`, `boot.config` 확인 | ✅ v1.4.11, build-guid `beff29feda834098ab218792d4d80249` |
| 저장소 스켈레톤 | `git status` 및 계획서 대조 | ✅ commit `0abad37` |
| .NET | `dotnet --version` | ✅ 10.0.302 |
| UABEA | macOS에서 12초 이상 프로세스 생존 확인 | ✅ 성공 |
| Python venv | `import numpy, scipy, PIL` | ✅ numpy 2.0.2 / scipy 1.13.1 / Pillow 11.3.0 |
| 원본 백업 | 파일 복사 및 SHA-256 기록 | ✅ `original/`, 24MB, 14파일 |
| 기존 패치 | Google Drive 다운로드 및 압축 해제 | ✅ v1.0.1/v2.0.1의 `resources.assets`와 Lua 확보 |

## 도구 및 환경

- UABEA 실행:
  ```sh
  DOTNET_ROLL_FORWARD=LatestMajor dotnet tools/uabea/UABEAvalonia.dll
  ```
- 재현 스크립트: `scripts/setup-uabea-mac.sh`
- Python: `.venv/bin/python`
- 원본 복원: `scripts/restore-original.sh`
- 백업: `scripts/backup-original.sh`
- 정리 안내: `docs/CLEANUP.md`

UABEA 공식 macOS 빌드가 없어 Ubuntu 빌드에 macOS 네이티브 dylib(SkiaSharp/HarfBuzzSharp/AvaloniaNative)를 보강하고 `DOTNET_ROLL_FORWARD=LatestMajor`를 사용했다.

## 산출물

- 원본 백업: `original/`
- 원본 해시: `original/hashes.txt`
- 원본 버전: `original/VERSION.txt`
- 기존 패치: `tools/legacy-patches/v1.0.1/`, `tools/legacy-patches/v2.0.1/`
- 도구: `tools/uabea/`, `.venv/`

## 다음 Phase로 핸드오프

### 수신 Phase

- Phase 1 — 텍스트 위치 검증

### 반드시 알아야 할 사실

- 현재 설치본은 v1.4.11, build-guid `beff29feda834098ab218792d4d80249`다.
- 기존 패치는 구버전(v1.1.3/v1.4.2) 대상이므로 현재 버전과 문자열 대조 시 버전 차이가 있을 수 있다.
- 블루칩 v1/v2의 Lua에는 UTF-8 한글 번역이 포함되어 있어 Phase 2의 번역 추출 대상으로 사용할 수 있다.

### 다음 작업

1. Lua 카드 이름 변경으로 실제 로드 여부를 검증한다.
2. `resources.assets`의 TextAsset를 확인한다.
3. 소스별 수정이 실게임에 반영되는지 확인한 뒤 주 작업 대상을 확정한다.

### 미해결 이슈

- Lua 파일이 현재 게임에서 살아 있는 소스인지 미검증
- 한패(hanpe.net) 백업은 로그인 필요로 보류
