#!/bin/bash
# Twilight Struggle 한글 패치 — 배포 패키징 스크립트
#
# 용도: GitHub Releases 업로드용 zip 2종 + SHA256SUMS 생성
#   사용자용: patched/* + 설치/복원 스크립트 + README (+ LICENSE/CREDITS 존재 시)
#   재현용  : translation/ + fonts/ + 패치 파이프라인 스크립트 + 핵심 문서
#
# 사용법:
#   ./scripts/package-release.sh [버전]
#     예: ./scripts/package-release.sh v0.1.0
#         → dist/twilight-struggle-kr-patch-v0.1.0.zip
#         → dist/twilight-struggle-kr-patch-v0.1.0-src.zip
#
# 산출물: dist/ (gitignore 대상 — Releases 첨부로 업로드)
# 업로드: gh release create <버전> dist/*.zip --title "..." --notes "..."

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="${1:-v0.1.0}"
OUT_DIR="$PROJECT_DIR/dist"
BASE="twilight-struggle-kr-patch-$VERSION"
USER_ZIP="$OUT_DIR/$BASE.zip"
SRC_ZIP="$OUT_DIR/$BASE-src.zip"

cd "$PROJECT_DIR"

# ── 사전 검증 ──
echo "=== Twilight Struggle 한글 패치 패키징 ($VERSION) ==="
for f in patched/resources.assets patched/sharedassets0.assets \
         patched/level1 patched/level2 patched/level3; do
    if [ ! -f "$f" ]; then
        echo -e "\033[0;31m[오류] $f 없음 — 패치 파이프라인을 먼저 실행하세요.\033[0m"
        exit 1
    fi
done

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$OUT_DIR"

# 해시 명령 자동 선택 (macOS: shasum / Linux·Windows Git Bash: sha256sum)
if command -v sha256sum >/dev/null 2>&1; then
    HASH_CMD=(sha256sum)
else
    HASH_CMD=(shasum -a 256)
fi

# zip 명령 대신 Python zipfile 사용 (전 플랫폼 호환, 최대 압축)
zip_dir() {  # $1=폴더  $2=출력 zip
    python - "$1" "$2" <<'EOF'
import sys, zipfile, os
src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, _, files in os.walk(src):
        for f in sorted(files):
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, src))
print('  zip ok:', dst)
EOF
}

# ── 1. 사용자용 zip ──
echo ""
echo "=== [1/2] 사용자용 패키지 생성 중... ==="
USER_ROOT="$WORK/user/$BASE"
mkdir -p "$USER_ROOT/patched" "$USER_ROOT/scripts"

cp patched/resources.assets patched/sharedassets0.assets \
   patched/level1 patched/level2 patched/level3 patched/hashes.txt \
   "$USER_ROOT/patched/"
cp scripts/install.sh scripts/install-windows.ps1 scripts/restore-original.sh \
   "$USER_ROOT/scripts/"
cp README.md "$USER_ROOT/"

for f in LICENSE.txt CREDITS.md; do
    if [ -f "$f" ]; then
        cp "$f" "$USER_ROOT/"
    else
        echo "  [경고] $f 없음 — Phase 6에서 라이선스/크레딧 정리 필요 (미포함)"
    fi
done

( cd "$USER_ROOT" && find . -type f -print0 | sort -z | xargs -0 "${HASH_CMD[@]}" > SHA256SUMS )
zip_dir "$USER_ROOT" "$USER_ZIP"
echo "  ✅ $USER_ZIP ($(du -h "$USER_ZIP" | cut -f1))"

# ── 2. 재현용 zip ──
echo ""
echo "=== [2/2] 재현용 패키지 생성 중... ==="
SRC_ROOT="$WORK/src/$BASE-src"
mkdir -p "$SRC_ROOT/scripts" "$SRC_ROOT/docs"

cp -R translation "$SRC_ROOT/translation"
cp -R fonts "$SRC_ROOT/fonts"
rm -rf "$SRC_ROOT"/fonts/backup-* "$SRC_ROOT/fonts/.gitkeep"

# 패치/검증 파이프라인 스크립트 (설치 스크립트 포함 — 재현·복구용)
for s in inject_translations.py add_ko_columns.py patch_scenes.py verify_assets.py \
         extract_textassets.py extract_charset.py apply_font_mapping.py \
         analyze_scene_texts.py install.sh install-windows.ps1 restore-original.sh; do
    [ -f "scripts/$s" ] && cp "scripts/$s" "$SRC_ROOT/scripts/"
done

cp docs/PLAN.md docs/PROGRESS.md "$SRC_ROOT/docs/"

( cd "$SRC_ROOT" && find . -type f -print0 | sort -z | xargs -0 "${HASH_CMD[@]}" > SHA256SUMS )
zip_dir "$SRC_ROOT" "$SRC_ZIP"
echo "  ✅ $SRC_ZIP ($(du -h "$SRC_ZIP" | cut -f1))"

# ── 결과 ──
echo ""
echo "=== 완료 ($VERSION) ==="
ls -lh "$OUT_DIR"
echo ""
echo "업로드 (GitHub Releases):"
echo "  gh release create $VERSION $USER_ZIP $SRC_ZIP \\"
echo "      --title \"Twilight Struggle 한글 패치 $VERSION\" \\"
echo "      --notes \"설치 방법: zip 압축 해제 후 README.md 참조\""
