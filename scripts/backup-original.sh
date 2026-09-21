#!/usr/bin/env bash
# 원본 백업 (멱등): 게임 Data 폴더 → original/
# 용도: Steam 무결성 확인/업데이트 전 백업, 패치 실험 전 안전장치
set -euo pipefail

GAME_DIR="${GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data}"
ORIG_DIR="$(cd "$(dirname "$0")/../original" && pwd)"

[ -d "$GAME_DIR" ] || { echo "게임 폴더 없음: $GAME_DIR"; exit 1; }

mkdir -p "$ORIG_DIR"

# 백업 대상 (.resS 대용량 파일 제외 — 수정 불필요)
# ⚠️ 패치가 수정하는 파일은 전부 포함해야 한다 — 빠지면 restore-original.sh가 그 파일을
#    복원하지 않아 패치 상태로 남는다 (2026-09-21: sharedassets0 누락 발견·수정)
FILES=(
  resources.assets
  sharedassets0.assets sharedassets1.assets sharedassets2.assets sharedassets3.assets
  globalgamemanagers
  globalgamemanagers.assets
  level0 level1 level2 level3
)

for f in "${FILES[@]}"; do
  [ -f "$GAME_DIR/$f" ] && cp "$GAME_DIR/$f" "$ORIG_DIR/$f"
done
rm -rf "$ORIG_DIR/StreamingAssets"  # 재실행 시 중첩 방지
cp -R "$GAME_DIR/StreamingAssets" "$ORIG_DIR/"

# 버전 정보 기록
{
  echo "VERSION=$(defaults read "$GAME_DIR/../../Info.plist" CFBundleShortVersionString 2>/dev/null || echo unknown)"
  echo "BUILD_GUID=$(grep -oE 'build-guid=\S+' "$GAME_DIR/boot.config" | cut -d= -f2)"
  echo "BACKUP_DATE=$(date '+%Y-%m-%d %H:%M:%S')"
} > "$ORIG_DIR/VERSION.txt"

# 해시 기록
# ⚠️ global-metadata.dat(폰트 주입용 IL2CPP 메타데이터, 게임 Data 루트에 없는 파일)와
#    macOS .DS_Store는 제외 — hashes.txt는 restore-original.sh가 그대로 복원하는 목록이다
cd "$ORIG_DIR"
find . -type f ! -name hashes.txt ! -name VERSION.txt ! -name .gitkeep \
  ! -name .DS_Store ! -name 'global-metadata.dat' -print0 \
  | xargs -0 shasum -a 256 | sed 's|\./||' | sort -k2 > hashes.txt

# 검증
shasum -a 256 -c hashes.txt --quiet && echo "백업 완료 + 무결성 검증 통과: $ORIG_DIR ($(du -sh "$ORIG_DIR" | cut -f1))"
