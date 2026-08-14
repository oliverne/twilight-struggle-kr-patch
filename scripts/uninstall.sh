#!/bin/bash
# Twilight Struggle 한글 패치 — 제거 스크립트 (macOS)
#
# 용도: 패치 제거 (파일 복원만)
#   - patched 파일 → 원본(.bak) 복원
#   - 코드사인 재수행
# 언어 설정: 건드리지 않음 (2026-08-14 — EN 로케일 대체 방식, 복원 불필요)
#
# 사용법:
#   ./scripts/uninstall.sh
#
# 참고:
#   - .bak이 없으면 Steam "파일 무결성 확인"으로 원복 후 이 스크립트 재실행
#   - Steam 업데이트로 .bak이 옛 버전이면 Steam 무결성 확인이 더 안전 (아래 안내 출력)
#   - 언어 설정은 건드리지 않는다 (EN 로케일 덮어쓰기 방식 — 파일 복원만으로 영어 복귀)
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

echo -e "${YELLOW}=== Twilight Struggle 한글 패치 제거 ===${NC}"
echo ""

if [ ! -d "$GAME_DATA" ]; then
    echo -e "${RED}[오류] 게임을 찾을 수 없습니다:${NC}"
    echo "  $GAME_DATA"
    exit 1
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
echo "  Steam에서 Twilight Struggle을 실행하면 원래(영문) 상태로 돌아갑니다."
echo ""
echo "  ※ 재설치: ./scripts/install.sh"
