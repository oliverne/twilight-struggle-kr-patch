#!/usr/bin/env bash
# 실험 B: 수정된 resources.assets를 게임에 적용 (멱등)
# - 게임 파일이 원본 해시와 일치할 때만 복사
# - 이미 적용된 상태면 아무 것도 하지 않음
set -euo pipefail

GAME_DIR="${GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REL="resources.assets"
SRC="$ROOT/patched/$REL"
DST="$GAME_DIR/$REL"

[ -f "$SRC" ] || { echo "patched 파일 없음: $SRC"; exit 1; }
[ -d "$GAME_DIR" ] || { echo "게임 폴더 없음: $GAME_DIR"; exit 1; }

hash_of() { shasum -a 256 "$1" | awk '{print $1}'; }

SRC_HASH=$(hash_of "$SRC")
DST_HASH=$(hash_of "$DST")
ORIG_HASH=$(grep "  $REL\$" "$ROOT/original/hashes.txt" | awk '{print $1}')

if [ "$DST_HASH" = "$SRC_HASH" ]; then
  echo "이미 적용된 상태입니다."
elif [ "$DST_HASH" = "$ORIG_HASH" ]; then
  cp "$SRC" "$DST"
  echo "적용 완료: $REL"
else
  echo "경고: 게임 파일이 원본 백업과 일치하지 않습니다. 중단." >&2
  echo "  게임 업데이트 또는 외부 수정 가능성 — backup-original.sh 재실행 후 확인하세요." >&2
  exit 1
fi
