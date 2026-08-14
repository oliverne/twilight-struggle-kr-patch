#!/bin/bash
# Twilight Struggle 한글 패치 — macOS 설치 스크립트
#
# 용도: patched/ → Steam 게임 폴더로 파일 복사 + 코드사인
# 멱등성: 이미 패치된 파일을 다시 덮어써도 안전. uninstall.sh로 복원 가능.
# 언어 설정: 건드리지 않음 (2026-08-14 — EN 로케일을 한글로 대체, 유저는 기본 언어 EN 사용)
#
# 사용법:
#   ./scripts/install.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ── 경로 설정 ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PATCHED_DIR="$PROJECT_DIR/patched/macos"

# Steam 게임 경로 (macOS) — 기본 경로 + libraryfolders.vdf 자동 탐색 (다른 볼륨 설치 대응)
GAME_APP="$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app"
if [ ! -d "$GAME_APP" ]; then
    VDF="$HOME/Library/Application Support/Steam/steamapps/libraryfolders.vdf"
    if [ -f "$VDF" ]; then
        while IFS= read -r line; do
            lib_path=$(printf '%s' "$line" | sed -n 's/.*"path"[[:space:]]*"\([^"]*\)".*/\1/p' | sed 's/\\\\/\\/g')
            [ -n "$lib_path" ] || continue
            cand_app="$lib_path/steamapps/common/Twilight Struggle/TwilightStruggle.app"
            if [ -d "$cand_app" ]; then
                GAME_APP="$cand_app"
                echo -e "${GREEN}  ✅ Steam 위치 자동 탐색: $GAME_APP${NC}"
                break
            fi
        done < "$VDF"
    fi
fi
GAME_DATA="$GAME_APP/Contents/Resources/Data"

# ── 사전 검증 ──
echo -e "${YELLOW}=== Twilight Struggle 한글 패치 설치 ===${NC}"
echo ""

if [ ! -d "$GAME_DATA" ]; then
    echo -e "${RED}[오류] 게임을 찾을 수 없습니다:${NC}"
    echo "  $GAME_DATA"
    echo ""
    echo "  Steam에 Twilight Struggle이 설치되어 있어야 합니다."
    exit 1
fi

if [ ! -f "$PATCHED_DIR/resources.assets" ]; then
    echo -e "${RED}[오류] 패치 파일이 없습니다:${NC}"
    echo "  $PATCHED_DIR/resources.assets"
    echo ""
    echo "  먼저 scripts/inject_translations.py 를 실행하세요."
    exit 1
fi

# ── 원본 해시 확인 (최초 1회만) ──
BACKUP_DIR="$PROJECT_DIR/original"
HASH_FILE="$BACKUP_DIR/hashes.txt"

if [ ! -f "$HASH_FILE" ]; then
    echo -e "${YELLOW}[정보] 원본 해시 파일 생성 중...${NC}"
    mkdir -p "$BACKUP_DIR"
    shasum -a 256 "$GAME_DATA/resources.assets" "$GAME_DATA/sharedassets0.assets" \
        "$GAME_DATA/sharedassets1.assets" "$GAME_DATA/sharedassets2.assets" \
        "$GAME_DATA/sharedassets3.assets" 2>/dev/null > "$HASH_FILE"
    echo "  → $HASH_FILE"
fi

# ── 백업 (최초 1회만) ──
for asset in resources.assets sharedassets0.assets sharedassets1.assets sharedassets2.assets sharedassets3.assets level1 level2 level3; do
    if [ -f "$GAME_DATA/$asset" ] && [ ! -f "$GAME_DATA/${asset}.bak" ]; then
        cp "$GAME_DATA/$asset" "$GAME_DATA/${asset}.bak"
        echo -e "${GREEN}[백업]${NC} $asset → ${asset}.bak"
    fi
done

# ── 패치 파일 복사 ──
echo ""
echo -e "${YELLOW}[설치] 패치 파일 복사 중...${NC}"

COPIED=0
for asset in resources.assets sharedassets0.assets sharedassets1.assets sharedassets2.assets sharedassets3.assets level1 level2 level3; do
    if [ -f "$PATCHED_DIR/$asset" ]; then
        cp "$PATCHED_DIR/$asset" "$GAME_DATA/$asset"
        echo "  $asset"
        COPIED=$((COPIED + 1))
    fi
done

if [ $COPIED -eq 0 ]; then
    echo -e "${RED}[오류] 복사할 패치 파일이 없습니다.${NC}"
    exit 1
fi

# ── macOS 코드사인 ──
echo ""
echo -e "${YELLOW}[코드사인] macOS 보안 서명 중...${NC}"

# .app 번들 서명
if [ -d "$GAME_APP" ]; then
    codesign --force --sign - "$GAME_APP" 2>/dev/null && \
        echo -e "${GREEN}  ✅ $GAME_APP${NC}" || \
        echo -e "${YELLOW}  ⚠️  서명 실패 (관리자 권한 필요 가능성)${NC}"
fi

# 개별 dylib/bundle 파일도 서명 (패턴 미매칭 시 [ -f ] 검사가 무시)
for f in "$GAME_DATA"/*.dylib "$GAME_DATA"/*.bundle; do
    [ -f "$f" ] && codesign --force --sign - "$f" 2>/dev/null
done

# ── 완료 ──
echo ""
echo -e "${GREEN}=== 설치 완료! ===${NC}"
echo ""
echo "  Steam에서 Twilight Struggle을 실행하세요."
echo "  (언어 설정은 변경하지 않습니다 — EN 로케일이 한글로 대체되어 메뉴가 즉시 한글 표시)"
echo ""
echo "  ※ 영문(원래 언어) 복귀: scripts/uninstall.sh (원본 .bak 복원)"
echo "  ※ Steam 무결성 검사 후에는 다시 설치해야 합니다."
