#!/bin/bash
# Twilight Struggle 한글 패치 — macOS 설치 스크립트
#
# 용도: patched/ → Steam 게임 폴더로 파일 복사 + 코드사인 + 게임 언어 KO 설정
# 멱등성: 이미 패치된 파일을 다시 덮어써도 안전. restore.sh로 복원 가능.
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
PATCHED_DIR="$PROJECT_DIR/patched"

# Steam 게임 경로 (macOS)
GAME_APP="$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app"
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

# ── 게임 언어 KO 설정 (PlayerPrefs plist) ──
echo ""
echo -e "${YELLOW}[언어 설정] 한국어(KO)로 변경 중...${NC}"

# Unity macOS 규약: ~/Library/Preferences/unity.<Company>.<Product>.plist
PLIST="$HOME/Library/Preferences/unity.Playdek.TwilightStruggle.plist"
if [ ! -f "$PLIST" ]; then
    # 실제 파일명이 다를 수 있으므로 glob으로 검색 (게임을 1회 이상 실행한 경우)
    PLIST=$(ls "$HOME/Library/Preferences"/unity.*TwilightStruggle*.plist 2>/dev/null | head -1)
fi

# 이전 언어 값 기록 (uninstall 시 복원용) — plist 존재 여부와 무관하게 저장
# ⚠️ 기존 기록 파일이 있으면 덮어쓰지 않는다 (첫 설치 시점 값 보존).
#    Steam 무결성 재설치 후 재실행 시 언어가 KO로 남아 있어도 첫 설치 때의 원래 값을 유지해야
#    uninstall이 올바른 언어(보통 EN)로 복원한다.
if [ -f "$GAME_DATA/krpatch-install-info.txt" ]; then
    echo "  [기록] 기존 설치 정보 유지: $GAME_DATA/krpatch-install-info.txt (첫 설치 시점 값 보존)"
else
    PREV_LOCALIZATION=$(defaults read "$PLIST" localization 2>/dev/null || true)
    PREV_LOCALIZATION_H=$(defaults read "$PLIST" localization_h2525087814 2>/dev/null || true)
    printf '# Twilight Struggle 한글 패치 설치 정보 (uninstall.sh에서 사용)\nplatform=macos\nprevious_localization=%s\nprevious_localization_h2525087814=%s\n' \
        "${PREV_LOCALIZATION:-}" "${PREV_LOCALIZATION_H:-}" > "$GAME_DATA/krpatch-install-info.txt"
    echo "  [기록] 이전 언어 값 → $GAME_DATA/krpatch-install-info.txt (uninstall 시 복원)"
fi

if [ -z "$PLIST" ] || [ ! -f "$PLIST" ]; then
    # plist가 없으면 표준 경로에 새로 생성 (Unity가 최초 실행 시 읽음)
    PLIST="$HOME/Library/Preferences/unity.Playdek.TwilightStruggle.plist"
    defaults write "$PLIST" localization -string "KO"
    defaults write "$PLIST" localization_h2525087814 -string "KO"
    echo -e "${YELLOW}  ⚠️  PlayerPrefs plist가 없어 새로 생성했습니다: $(basename "$PLIST")${NC}"
    echo -e "${YELLOW}  ⚠️  게임을 1회 실행한 뒤 언어가 KO인지 확인하세요.${NC}"
else
    # macOS는 'localization' 키를 읽는다 (2026-08-12 실측: localization_h2525087814=KO인데도
    # Load Language Header: EN — Windows와 키가 다름)
    OLD=$(defaults read "$PLIST" localization 2>/dev/null || echo "없음")
    defaults write "$PLIST" localization -string "KO"
    defaults write "$PLIST" localization_h2525087814 -string "KO"
    echo -e "${GREEN}  ✅ $(basename "$PLIST") — localization = ${OLD} → KO${NC}"
fi

# ── 완료 ──
echo ""
echo -e "${GREEN}=== 설치 완료! ===${NC}"
echo ""
echo "  Steam에서 Twilight Struggle을 실행하세요."
echo "  (게임 언어는 KO로 자동 설정됨 — 메뉴가 즉시 한글 표시)"
echo ""
echo "  ※ 영문(원래 언어) 복귀: scripts/uninstall.sh (원본 .bak 복원 + 언어 복원)"
echo "  ※ Steam 무결성 검사 후에는 다시 설치해야 합니다."
