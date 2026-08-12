#!/bin/bash
# Twilight Struggle 한글 패치 — 제거 스크립트 (macOS)
#
# 용도: 패치 제거 + 원래 언어 복귀 (영문 유저는 EN으로)
#   - patched 파일 → 원본(.bak) 복원
#   - 게임 언어 → 설치 전 값으로 복원 (krpatch-install-info.txt 기록 기준)
#   - 코드사인 재수행
#
# 사용법:
#   ./scripts/uninstall.sh
#
# 참고:
#   - .bak이 없으면 Steam "파일 무결성 확인"으로 원복 후 이 스크립트 재실행
#   - Steam 업데이트로 .bak이 옛 버전이면 Steam 무결성 확인이 더 안전 (아래 안내 출력)
#   - 게임 삭제·재설치를 해도 언어 설정(plist)은 게임 폴더 밖에 있어 KO가 남는다
#     → 기록 파일(krpatch-install-info.txt)이 없으므로 아래 경고 안내대로 수동 복원 필요
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ── 경로 설정 ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GAME_APP="$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app"
GAME_DATA="$GAME_APP/Contents/Resources/Data"

FILES=(resources.assets sharedassets0.assets sharedassets1.assets sharedassets2.assets sharedassets3.assets level1 level2 level3)
INFO_FILE="$GAME_DATA/krpatch-install-info.txt"

echo -e "${YELLOW}=== Twilight Struggle 한글 패치 제거 ===${NC}"
echo ""

if [ ! -d "$GAME_DATA" ]; then
    echo -e "${RED}[오류] 게임을 찾을 수 없습니다:${NC}"
    echo "  $GAME_DATA"
    exit 1
fi

# ── 설치 정보 읽기 (언어 복원용) ──
PREV_LOCALIZATION=""
PREV_LOCALIZATION_H=""
if [ -f "$INFO_FILE" ]; then
    while IFS='=' read -r key value; do
        case "$key" in
            previous_localization) PREV_LOCALIZATION="$value" ;;
            previous_localization_h2525087814) PREV_LOCALIZATION_H="$value" ;;
        esac
    done < "$INFO_FILE"
    echo -e "${GREEN}[정보]${NC} 설치 기록 확인: $INFO_FILE"
    echo "  이전 언어: localization=${PREV_LOCALIZATION:-없음} / localization_h2525087814=${PREV_LOCALIZATION_H:-없음}"
else
    echo -e "${YELLOW}[경고]${NC} 설치 기록 파일이 없습니다: krpatch-install-info.txt"
    echo "  (구버전 설치 또는 게임 삭제·재설치로 기록이 사라진 경우입니다.)"
    echo "  ⚠️ 게임을 삭제·재설치해도 언어 설정(plist)은 게임 폴더 밖에 있어 KO가 남습니다."
    echo "     이 상태로 실행하면 메뉴·카드가 \${Key}로 표시되니 언어를 수동으로 되돌리세요:"
    echo ""
    echo "    defaults write \"$HOME/Library/Preferences/unity.Playdek.TwilightStruggle.plist\" localization -string \"EN\""
    echo "    defaults write \"$HOME/Library/Preferences/unity.Playdek.TwilightStruggle.plist\" localization_h2525087814 -string \"EN\""
    echo "    (⚠️ 이 게임에는 언어 선택 UI가 없습니다 — 위 defaults 명령으로만 변경 가능)"
fi

# ── 원본(.bak) 복원 ──
echo ""
echo -e "${YELLOW}[복원] 패치 파일 → 원본(.bak) 복원 중...${NC}"

RESTORED=0
MISSING=0
for asset in "${FILES[@]}"; do
    if [ -f "$GAME_DATA/${asset}.bak" ]; then
        cp "$GAME_DATA/${asset}.bak" "$GAME_DATA/$asset"
        echo "  $asset ← ${asset}.bak"
        RESTORED=$((RESTORED + 1))
    elif [ -f "$GAME_DATA/$asset" ]; then
        MISSING=$((MISSING + 1))
    fi
done

if [ $RESTORED -eq 0 ]; then
    echo -e "${YELLOW}  ⚠️  복원할 .bak이 없습니다.${NC}"
    echo -e "${YELLOW}     Steam → 라이브러리 → Twilight Struggle → 속성 → 설치된 파일 → \"파일 무결성 확인\"을 실행하세요.${NC}"
else
    echo -e "${GREEN}  ✅ ${RESTORED}개 파일 원본 복원 완료${NC}"
    if [ $MISSING -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  ${MISSING}개 파일은 .bak이 없어 Steam 무결성 확인이 필요할 수 있습니다.${NC}"
    fi
fi

# ── 게임 언어 복원 ──
echo ""
echo -e "${YELLOW}[언어] 원래 언어로 복원 중...${NC}"

PLIST="$HOME/Library/Preferences/unity.Playdek.TwilightStruggle.plist"
if [ ! -f "$PLIST" ]; then
    PLIST=$(ls "$HOME/Library/Preferences"/unity.*TwilightStruggle*.plist 2>/dev/null | head -1)
fi

if [ -z "$PLIST" ] || [ ! -f "$PLIST" ]; then
    echo -e "${YELLOW}  ⚠️  PlayerPrefs plist를 찾을 수 없어 언어 설정을 건드리지 않았습니다.${NC}"
else
    restore_key() {  # $1=키  $2=이전 값
        if [ -n "$2" ]; then
            defaults write "$PLIST" "$1" -string "$2"
            echo "  ✅ $1 = $2"
        else
            defaults delete "$PLIST" "$1" 2>/dev/null || true
            echo "  ✅ $1 = (설치 전에 없었음 — 키 제거)"
        fi
    }
    restore_key "localization" "$PREV_LOCALIZATION"
    restore_key "localization_h2525087814" "$PREV_LOCALIZATION_H"
fi

# ── 설치 정보 파일 제거 ──
if [ -f "$INFO_FILE" ]; then
    rm "$INFO_FILE"
    echo ""
    echo -e "${GREEN}[정리]${NC} 설치 정보 파일 삭제: krpatch-install-info.txt"
fi

# ── macOS 코드사인 ──
echo ""
echo -e "${YELLOW}[코드사인] macOS 보안 서명 중...${NC}"

if [ -d "$GAME_APP" ]; then
    codesign --force --sign - "$GAME_APP" 2>/dev/null && \
        echo -e "${GREEN}  ✅ $GAME_APP${NC}" || \
        echo -e "${YELLOW}  ⚠️  서명 실패 (관리자 권한 필요 가능성)${NC}"
fi

for f in "$GAME_DATA"/*.dylib "$GAME_DATA"/*.bundle; do
    [ -f "$f" ] && codesign --force --sign - "$f" 2>/dev/null
done

# ── 완료 ──
echo ""
echo -e "${GREEN}=== 제거 완료! ===${NC}"
echo ""
echo "  Steam에서 Twilight Struggle을 실행하면 원래 언어로 돌아갑니다."
echo "  (이 게임에는 언어 선택 UI가 없어, 언어 변경은 plist 값으로만 가능합니다)"
echo ""
echo "  ※ 재설치: ./scripts/install.sh"
