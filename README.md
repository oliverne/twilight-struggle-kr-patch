# Twilight Struggle 한글 패치

Steam판 **Twilight Struggle**(App ID `406290`)의 최신 버전용 한글 패치를 복원·개발하는 프로젝트입니다.

> **현재 개발 중입니다.** 아직 실게임에 적용할 수 있는 완성 패치나 공식 릴리스는 없습니다.
> 현재 설치된 게임 파일은 수정하지 않았으며, Phase 1 텍스트 반영 검증을 준비 중입니다.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 대상 게임 | Steam Twilight Struggle v1.4.11 |
| Unity/플랫폼 | Unity 6 `6000.0.58f2`, IL2CPP |
| Phase 0: 준비 | ✅ 완료 |
| Phase 1: 텍스트 위치 검증 | ⬜ 다음 작업 |
| 기존 번역 확보 | ✅ 블루칩 v1.0.1/v2.0.1 Lua에서 한글 번역 확인 |
| 한글 SDF 폰트 | ⬜ 미착수 |
| 패치 설치 스크립트 | ⬜ 미착수 — 현재는 백업/복원 스크립트만 제공 |
| Windows 테스트 | ⬜ 미착수 |

상세 진행 상황은 [`docs/PROGRESS.md`](docs/PROGRESS.md)를 참조하세요.

## 목표

1. 기존 한글 패치에서 번역문을 추출합니다.
2. 현재 v1.4.11의 실제 텍스트 소스를 확인합니다.
3. 기존 번역을 최신 문자열 구조에 맞게 재사용합니다.
4. CJK 글리프를 포함한 TextMeshPro SDF 폰트 아틀라스를 생성·주입합니다.
5. macOS와 Windows에서 반복 적용 가능한 설치 패치를 제공합니다.

카드·UI 텍스트를 우선 대상으로 하며, 보드맵에 이미지로 구워진 국가명 등은 1차 범위에서 제외합니다.

## 안전 원칙

- Steam 설치 폴더에서 직접 개발하지 않습니다.
- 원본은 `original/`에 백업하고, 수정 결과는 `patched/`에 둡니다.
- 모든 실제 패치 적용은 멱등적인 설치 스크립트로 수행합니다.
- macOS에서 게임 파일을 수정하면 애드혹 코드 서명이 필요합니다.
- 원본 백업과 레거시 패치 파일은 용량 및 저작권 문제로 Git에 포함하지 않습니다.

## macOS 준비

### 필수 조건

- macOS
- Steam에 설치된 Twilight Struggle v1.4.11
- Homebrew
- Python 3
- .NET SDK/runtime — UABEA 실행용

### 저장소 준비

```bash
git clone git@github.com:oliverne/twilight-struggle-kr-patch.git
cd twilight-struggle-kr-patch
```

### 도구 설치

.NET이 없다면 설치합니다.

```bash
brew install dotnet
dotnet --version
```

UABEA는 공식 macOS 빌드가 없어 Ubuntu 빌드와 macOS 네이티브 라이브러리를 조합합니다. 설치 스크립트는 이미 설치된 파일을 재사용하므로 재실행할 수 있습니다.

```bash
./scripts/setup-uabea-mac.sh
```

실행:

```bash
DOTNET_ROLL_FORWARD=LatestMajor \
  dotnet tools/uabea/UABEAvalonia.dll
```

Python 작업 환경:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install \
  'numpy==2.0.2' \
  'scipy==1.13.1' \
  'Pillow==11.3.0'
```

## 원본 백업·복원

Steam과 게임을 종료한 뒤 백업합니다.

```bash
./scripts/backup-original.sh
```

백업 대상은 `resources.assets`, `level0~3`, `StreamingAssets/`, `globalgamemanagers*`이며, 대용량 `.resS` 파일은 제외합니다. 백업 후 `original/VERSION.txt`와 `original/hashes.txt`가 생성되고 SHA-256 무결성 검사가 실행됩니다.

실험 후 원본으로 되돌릴 때:

```bash
./scripts/restore-original.sh
```

복원 스크립트는 먼저 백업 해시를 검증하고, macOS 앱을 애드혹 재서명합니다. 게임이 실행 중일 때는 사용하지 마세요.

시스템 변경 및 생성물 정리 방법은 [`docs/CLEANUP.md`](docs/CLEANUP.md)에 정리되어 있습니다.

## 기존 패치 자료

다음 자료를 번역 추출용 참고 자료로 사용합니다.

- [블루칩 한글 패치 안내](https://bluechip2022.tistory.com/2)
- [한패 백업 목록](https://hanpe.net/hanguls/t)

현재 로컬에 확보된 자료:

```text
tools/legacy-patches/
├── bluechip-v1.0.1-v2.0.1.zip
├── v1.0.1/TwilightStruggle_Data/
└── v2.0.1/TwilightStruggle_Data/
```

두 버전의 `StreamingAssets/Lua/`에서 한글 번역이 포함된 것을 확인했습니다. 레거시 패치 파일은 Git에 업로드하지 않으며, 각 배포처의 저작권·배포 조건을 따릅니다.

## 개발 순서

현재 다음 순서로 진행합니다.

1. **Phase 1 — 텍스트 위치 검증**
   - Lua 카드 이름을 임시 문자열로 변경해 실제 반영 여부 확인
   - 필요하면 Lua 로드 경로를 확인
   - UABEA로 `Common_Strings` / `TS_Cards` 수정 반영 여부 확인
2. **Phase 2 — 문자열 추출 및 번역 소스 구축**
   - 현재 문자열을 JSON으로 추출
   - 기존 한글 번역과 자동 매칭
   - 용어집 및 TMP 리치 텍스트 태그 보존 규칙 작성
3. **Phase 3 — 한글 SDF 폰트 생성·주입**
   - 실제 번역에 필요한 글자만 수집
   - TMP SDF 아틀라스 생성
   - 게임 에셋에 주입하고 `□` 출력 여부 검증
4. **Phase 4 — 텍스트 주입 및 레이아웃 조정**
5. **Phase 5 — macOS/Windows 및 멀티플레이 테스트**
6. **Phase 6 — 릴리스 패키지 및 배포 문서 작성**

Phase는 검증 실패나 미해결 이슈를 기록하기 전에는 다음 단계로 넘어가지 않습니다.

## 저장소 구조

```text
.
├── AGENTS.md                 # 에이전트 작업 규칙
├── docs/
│   ├── PLAN.md               # 전체 계획
│   ├── PROGRESS.md           # Phase별 진행·검증·핸드오프
│   ├── PHASE-0-PLAN.md       # Phase 0 실행 계획
│   └── CLEANUP.md            # 설치 도구와 산출물 정리 방법
├── fonts/                    # 폰트 및 SDF 산출물
├── patched/                  # 최종 수정 파일
├── scripts/
│   ├── backup-original.sh    # 게임 원본 백업 및 해시 검증
│   ├── restore-original.sh   # 원본 복원 및 macOS 재서명
│   └── setup-uabea-mac.sh    # macOS용 UABEA 설치
├── tools/                    # 도구 안내 및 로컬 도구(일부 Git 제외)
└── translation/              # JSON/CSV 번역 소스
```

`original/`, `tools/uabea/`, `tools/legacy-patches/`, `.venv/`는 로컬 전용이며 `.gitignore`에 등록되어 있습니다.

## 관련 문서

- [전체 계획](docs/PLAN.md)
- [현재 진행 상황](docs/PROGRESS.md)
- [Phase 0 실행 계획](docs/PHASE-0-PLAN.md)
- [시스템 변경 및 정리 가이드](docs/CLEANUP.md)
- [도구 안내](tools/README.md)

## 라이선스 및 크레딧

이 프로젝트는 기존 번역 패치의 번역문을 참고·재사용하기 위한 연구 및 개인용 개발 프로젝트입니다. 기존 패치 제작자와 사용 폰트의 라이선스를 확인하고, 배포 시 적절한 크레딧과 라이선스 전문을 포함해야 합니다.

- 기존 패치 제작자: 우드킹, 블루칩 등
- 게임 저작권: Playdek 및 각 권리자
- 본 저장소는 게임 원본 파일이나 레거시 패치 바이너리를 배포하지 않습니다.
