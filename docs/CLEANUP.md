# 시스템 변경 사항 & 정리(Cleanup) 가이드

> 설치한 도구로 인한 시스템 변경과, 나중에 전부 되돌리는 방법을 기록한다.
> 최종 업데이트: 2026-08-12 (macOS 파이프라인 재현·uninstall 스크립트 반영)

## 설치/변경된 항목

### macOS (초기 작업)

| 항목 | 위치 | 설치 방법 | 시스템 영향 |
|---|---|---|---|
| .NET 10.0.302 | `/opt/homebrew/Cellar/dotnet/` | `brew install dotnet` | Homebrew 패키지, zsh completions 자동 설치 |
| UABEA v8 + macOS 네이티브 dylib | `tools/uabea/` (프로젝트 내부) | `scripts/setup-uabea-mac.sh` | 없음 (프로젝트 로컬, gitignore) |
| Python venv | `.venv/` (프로젝트 내부) | `python3 -m venv .venv` | 없음 (프로젝트 로컬, gitignore) |
| 원본 백업 | `original/` (약 24MB) | `scripts/backup-original.sh` | 없음 (프로젝트 로컬, gitignore) |
| 기존 패치 | `tools/legacy-patches/` (약 930MB) | Google Drive 수동 다운로드 | 없음 (프로젝트 로컬, gitignore) |

### Windows (2026-08-11 작업 위치)

| 항목 | 위치 | 비고 |
|---|---|---|
| Python venv (포크 UnityPy + TypeTreeGeneratorAPI) | 프로젝트 `.venv/` | 게임 에셋 편집용 |
| Unity_Font_Replacer v1.2.8 | `tools/unity-font-replacer/` | exe + KR_ASSETS + Il2CppDumper |
| 폰트 주입 작업 폴더 | `tools/font-inject-work/` | 가상 게임 폴더 + font-output |
| fontTools | `.venv/` | TTF 메트릭 분석용 |

### macOS (2026-08-12 이후 작업 위치 — Windows 전송 불필요)

| 항목 | 위치 | 비고 |
|---|---|---|
| 폰트 주입 가상 작업 폴더 | `tools/font-inject-work-mac/` | macOS에서 소스 실행으로 폰트 주입 (Windows 빌드 GameAssembly.dll + global-metadata.dat 필요 — `original/`에 보관) |
| Unity_Font_Replacer 파이썬 소스 | `tools/unity-font-replacer/src/` | venv 패치 2건 필요 (Runbook Step 5) |

### 게임 파일 변경 (Windows Steam 설치본, 2026-08-11)

| 파일 | 변경 내용 | 백업 위치 |
|---|---|---|
| `TwilightStruggle_Data/resources.assets` | 번역 주입(666+52행) + 한글 SDF 폰트 24개 주입 | `backup-20260811/resources.assets.prev-patch` |
| `TwilightStruggle_Data/sharedassets0.assets` | atwriter SDF 폰트 주입 | `backup-20260811/sharedassets0.assets.prev-patch` |
| `TwilightStruggle_Data/level1` | 씬 하드코딩 문자열 883개 한글화 | `backup-20260811/level1.pre-scene-patch` |
| `TwilightStruggle_Data/level2` | 씬 하드코딩 문자열 1,391개 한글화 | `backup-20260811/level2.pre-scene-patch` |
| `TwilightStruggle_Data/level3` | 씬 하드코딩 문자열 274개 한글화 | `backup-20260811/level3.pre-scene-patch` |
| ~~레지스트리 `HKCU\Software\Playdek\TwilightStruggle`~~ | ~~`localization_h2525087814` = `KO` (게임 언어)~~ — **2026-08-14 폐기: 언어 설정 무조작** (EN 로케일 덮어쓰기 방식) | — |

> 백업 폴더 위치: `D:\Games\steamapps\common\Twilight Struggle\TwilightStruggle_Data\backup-20260811\`

### 게임 파일 변경 (macOS Steam 설치본, 2026-08-12)

| 파일 | 변경 내용 |
|---|---|
| `TwilightStruggle_Data/resources.assets` | macOS 원본 기준 번역+KO 열+폰트 주입본 |
| `TwilightStruggle_Data/sharedassets0.assets` | atwriter SDF 폰트 주입본 |
| `TwilightStruggle_Data/level1~3` | macOS 원본 기준 씬 패치본 (Windows 씬 패치본과 호환 불가) |
| ~~plist `~/Library/Preferences/unity.Playdek.TwilightStruggle.plist`~~ | ~~`localization` = `KO` (macOS 키)~~ — **2026-08-14 폐기: 언어 설정 무조작** (EN 로케일 덮어쓰기 방식) |

> 현재 저장소 `patched/`는 **macOS 원본 기준**이다. 설치·제거는 `scripts/install.sh` / `scripts/uninstall.sh`가 백업·복원을 자동 처리한다 (언어 설정은 건드리지 않음 — 2026-08-14 개정).

## 전체 정리 (완전 되돌리기)

```bash
# 1. 게임 파일을 원본으로 복원 (백업에서)
cd ~/Projects/twilight-struggle-kr-patch
./scripts/uninstall.sh                          # macOS — 원본(.bak) 복원 + 언어 복원 + 재서명 자동
# Windows: powershell -ExecutionPolicy Bypass -File scripts\uninstall-windows.ps1
#  (백업이 없으면 Steam "파일 무결성 확인" 후 uninstall 스크립트 재실행)

# 2. Homebrew dotnet 제거 (macOS)
brew uninstall dotnet

# 3. 프로젝트 로컬 산출물 제거 (git 관리 대상 파일은 남음)
rm -rf tools/uabea tools/legacy-patches original .venv tools/font-inject-work* tools/unity-font-replacer/src

# 4. 임시 파일 제거
rm -rf /tmp/hanpe*.html /tmp/bluechip*.html /tmp/uabea.log \
       /tmp/skiasharp-macos /tmp/harfbuzz-macos /tmp/avalonia-native \
       /tmp/*.nupkg /tmp/gcookie /tmp/ts-ga
```

## 부분 정리

- **UABEA만 재설치**: `rm -rf tools/uabea && ./scripts/setup-uabea-mac.sh`
- **패치만 되돌리기**: Steam "파일 무결성 확인" 또는 uninstall 스크립트(백업 복원 + 언어 복원)
- **언어만 되돌리기**: uninstall 스크립트가 자동 처리 (설치 전 값 복원). 수동: 레지스트리/plist `localization*` = `EN`
- **디스크 확보**: `tools/legacy-patches/bluechip-v1.0.1-v2.0.1.zip` (520MB) 삭제 가능 — Drive에서 재다운 가능

## 주의

- `brew uninstall dotnet` 후에도 UABEA는 동작 불가 (런타임 의존) — 작업 중에는 제거하지 말 것
- 게임 업데이트 후에는 백업 해시가 무효화됨 → `backup-original.sh` 재실행 필요
- Steam 무결성 확인 시 패치가 원복되므로, 재적용은 `install.sh`(macOS) / `install-windows.ps1`(Windows)로
