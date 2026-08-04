#!/usr/bin/env bash
# 원본 복원 (멱등): original/ → 게임 Data 폴더
# 용도: 실험 후 복원, Steam 무결성 확인으로 망가진 파일 복구
set -euo pipefail

GAME_DIR="${GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data}"
ORIG_DIR="$(cd "$(dirname "$0")/../original" && pwd)"

[ -d "$ORIG_DIR" ] || { echo "백업 없음: $ORIG_DIR (backup-original.sh 먼저 실행)"; exit 1; }
[ -d "$GAME_DIR" ] || { echo "게임 폴더 없음: $GAME_DIR"; exit 1; }

# 복원 전 백업 무결성 확인
cd "$ORIG_DIR"
shasum -a 256 -c hashes.txt --quiet || { echo "백업 해시 검증 실패 — 복원 중단"; exit 1; }

# 파일 복원
while read -r hash f; do
  mkdir -p "$GAME_DIR/$(dirname "$f")"
  cp "$ORIG_DIR/$f" "$GAME_DIR/$f"
done < hashes.txt

# macOS: 수정된 앱 재서명 (코드 서명 무결성 복구)
APP_PATH="$GAME_DIR/../../.."
codesign --force --sign - "$APP_PATH" 2>/dev/null \
  && echo "복원 완료 + 재서명 완료" \
  || echo "복원 완료 (재서명 실패 — 수동 확인 필요)"
