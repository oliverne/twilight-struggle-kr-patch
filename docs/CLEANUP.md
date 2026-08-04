# 시스템 변경 사항 & 정리(Cleanup) 가이드

> 설치한 도구로 인한 시스템 변경과, 나중에 전부 되돌리는 방법을 기록한다.
> 최종 업데이트: 2026-08-04

## 설치/변경된 항목

| 항목 | 위치 | 설치 방법 | 시스템 영향 |
|---|---|---|---|
| .NET 10.0.302 | `/opt/homebrew/Cellar/dotnet/` | `brew install dotnet` | Homebrew 패키지, zsh completions 자동 설치 |
| UABEA v8 + macOS 네이티브 dylib | `tools/uabea/` (프로젝트 내부) | `scripts/setup-uabea-mac.sh` | 없음 (프로젝트 로컬, gitignore) |
| Python venv | `.venv/` (프로젝트 내부) | `python3 -m venv .venv` | 없음 (프로젝트 로컬, gitignore) |
| 원본 백업 | `original/` (약 24MB) | `scripts/backup-original.sh` | 없음 (프로젝트 로컬, gitignore) |
| 기존 패치 | `tools/legacy-patches/` (약 930MB) | Google Drive 수동 다운로드 | 없음 (프로젝트 로컬, gitignore) |
| 임시 파일 | `/tmp/hanpe*.html`, `/tmp/bluechip*.html`, `/tmp/uabea.log`, `/tmp/{skiasharp,harfbuzz,avalonia}-*` | 분석 중 생성 | 재부팅 시 자동 삭제 |

**게임 파일은 아직 수정하지 않음** (Phase 1부터 변경 시작).

## 전체 정리 (완전 되돌리기)

```bash
cd ~/Projects/twilight-struggle-kr-patch

# 1. 게임 파일을 원본으로 복원 (실험/패치 적용했던 경우에만)
./scripts/restore-original.sh

# 2. Homebrew dotnet 제거
brew uninstall dotnet

# 3. 프로젝트 로컬 산출물 제거 (git 관리 대상 파일은 남음)
rm -rf tools/uabea tools/legacy-patches original .venv

# 4. 임시 파일 제거
rm -rf /tmp/hanpe*.html /tmp/bluechip*.html /tmp/uabea.log \
       /tmp/skiasharp-macos /tmp/harfbuzz-macos /tmp/avalonia-native \
       /tmp/*.nupkg /tmp/gcookie
```

## 부분 정리

- **UABEA만 재설치**: `rm -rf tools/uabea && ./scripts/setup-uabea-mac.sh`
- **패치만 되돌리기**: `./scripts/restore-original.sh` (Steam "파일 무결성 확인"도 대안)
- **디스크 확보**: `tools/legacy-patches/bluechip-v1.0.1-v2.0.1.zip` (520MB) 삭제 가능 — Drive에서 재다운 가능

## 주의

- `brew uninstall dotnet` 후에도 UABEA는 동작 불가 (런타임 의존) — Phase 1~4 작업 중에는 제거하지 말 것
- 게임 업데이트 후에는 `original/` 해시가 무효화됨 → `backup-original.sh` 재실행 필요
