#!/bin/bash
# Twilight Struggle 한글 패치 — 배포 패키징 스크립트
#
# 용도: GitHub Releases 업로드용 zip 3종 + SHA256SUMS 생성
#   사용자용(windows): patched/windows/ + install-windows.ps1 + uninstall-windows.ps1 + README
#   사용자용(macos)  : patched/macos/ + install.sh + uninstall.sh + restore-original.sh + README
#   재현용(src)      : translation/ + fonts/ + 패치 파이프라인 스크립트 + 핵심 문서
#
# 사용법:
#   ./scripts/package-release.sh [버전]
#     예: ./scripts/package-release.sh v0.1.0
#         → dist/twilight-struggle-kr-patch-v0.1.0-windows.zip
#         → dist/twilight-struggle-kr-patch-v0.1.0-macos.zip
#         → dist/twilight-struggle-kr-patch-v0.1.0-src.zip
#
# 산출물: dist/ (gitignore 대상 — Releases 첨부로 업로드)
# 업로드: gh release create <버전> dist/*.zip --title "..." --notes "..."
#
# ⚠️ patched/는 플랫폼별 (level1~3은 크래시 위험 — 2026-08-12 실측):
#   patched/windows/  — Windows 원본 기준 (install-windows.ps1이 사용)
#   patched/macos/    — macOS 원본 기준 (install.sh가 사용)
#   존재하는 플랫폼만 패키징하며, 없으면 경고 후 스킵한다.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="${1:-v0.1.0}"
OUT_DIR="$PROJECT_DIR/dist"
BASE="twilight-struggle-kr-patch-$VERSION"
WIN_ZIP="$OUT_DIR/$BASE-windows.zip"
MAC_ZIP="$OUT_DIR/$BASE-macos.zip"
SRC_ZIP="$OUT_DIR/$BASE-src.zip"

cd "$PROJECT_DIR"

# ── 사전 검증 ──
echo "=== Twilight Struggle 한글 패치 패키징 ($VERSION) ==="

check_platform() {  # $1=platform  $2=설치 스크립트
    local plat="$1" script="$2"
    local ok=1
    for f in "patched/$plat/resources.assets" "patched/$plat/sharedassets0.assets" \
             "patched/$plat/level1" "patched/$plat/level2" "patched/$plat/level3"; do
        if [ ! -f "$f" ]; then
            echo -e "\033[0;33m[경고] $f 없음 — $plat 패키지는 스킵.\033[0m"
            ok=0
        fi
    done
    if [ $ok -eq 1 ] && [ ! -f "$script" ]; then
        echo -e "\033[0;33m[경고] $script 없음 — $plat 패키지는 스킵.\033[0m"
        ok=0
    fi
    return $((1 - ok))
}

HAVE_WIN=0; HAVE_MAC=0
check_platform windows scripts/install-windows.ps1 && HAVE_WIN=1
check_platform macos scripts/install.sh && HAVE_MAC=1
if [ $HAVE_WIN -eq 0 ] && [ $HAVE_MAC -eq 0 ]; then
    echo -e "\033[0;31m[오류] 패치할 플랫폼 폴더가 없습니다 — 패치 파이프라인을 먼저 실행하세요.\033[0m"
    exit 1
fi

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
# 최상위 폴더(폴더 basename)를 포함해 압축 해제 시 파일이 섞이지 않게 한다.
zip_dir() {  # $1=폴더  $2=출력 zip
    python - "$1" "$2" <<'EOF'
import sys, zipfile, os
src, dst = sys.argv[1], sys.argv[2]
root = os.path.basename(src.rstrip('/\\'))
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dirpath, _, files in os.walk(src):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            z.write(p, os.path.join(root, os.path.relpath(p, src)))
print('  zip ok:', dst)
EOF
}

# ── 1. Windows 사용자용 zip ──
if [ $HAVE_WIN -eq 1 ]; then
    echo ""
    echo "=== [1/3] Windows 패키지 생성 중... ==="
    WIN_ROOT="$WORK/win/$BASE"
    # ⚠️ zip 내부도 patched/<플랫폼>/ 구조 유지 — install-windows.ps1이 ..\patched\windows 에서 찾음
    mkdir -p "$WIN_ROOT/patched/windows" "$WIN_ROOT/scripts"
    cp patched/windows/resources.assets patched/windows/sharedassets0.assets \
       patched/windows/level1 patched/windows/level2 patched/windows/level3 \
       patched/windows/hashes.txt "$WIN_ROOT/patched/windows/"
    cp scripts/install-windows.ps1 scripts/uninstall-windows.ps1 "$WIN_ROOT/scripts/"
    cp README.md LICENSE "$WIN_ROOT/"
    mv "$WIN_ROOT/LICENSE" "$WIN_ROOT/LICENSE.txt"
    ( cd "$WIN_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 "${HASH_CMD[@]}" > SHA256SUMS )
    zip_dir "$WIN_ROOT" "$WIN_ZIP"
    echo "  ✅ $WIN_ZIP ($(du -h "$WIN_ZIP" | cut -f1))"
fi

# ── 2. macOS 사용자용 zip ──
if [ $HAVE_MAC -eq 1 ]; then
    echo ""
    echo "=== [2/3] macOS 패키지 생성 중... ==="
    MAC_ROOT="$WORK/mac/$BASE"
    # ⚠️ zip 내부도 patched/<플랫폼>/ 구조 유지 — install.sh가 patched/macos 에서 찾음
    mkdir -p "$MAC_ROOT/patched/macos" "$MAC_ROOT/scripts"
    cp patched/macos/resources.assets patched/macos/sharedassets0.assets \
       patched/macos/level1 patched/macos/level2 patched/macos/level3 \
       patched/macos/hashes.txt "$MAC_ROOT/patched/macos/"
    cp scripts/install.sh scripts/uninstall.sh scripts/restore-original.sh "$MAC_ROOT/scripts/"
    cp README.md LICENSE "$MAC_ROOT/"
    mv "$MAC_ROOT/LICENSE" "$MAC_ROOT/LICENSE.txt"
    ( cd "$MAC_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 "${HASH_CMD[@]}" > SHA256SUMS )
    zip_dir "$MAC_ROOT" "$MAC_ZIP"
    echo "  ✅ $MAC_ZIP ($(du -h "$MAC_ZIP" | cut -f1))"
fi

# ── 3. 재현용 zip ──
echo ""
echo "=== [3/3] 재현용 패키지 생성 중... ==="
SRC_ROOT="$WORK/src/$BASE-src"
mkdir -p "$SRC_ROOT/scripts" "$SRC_ROOT/docs"

cp -R translation "$SRC_ROOT/translation"
cp -R fonts "$SRC_ROOT/fonts"
rm -rf "$SRC_ROOT"/fonts/backup-* "$SRC_ROOT/fonts/.gitkeep"

# 패치/검증 파이프라인 스크립트 (설치 스크립트 포함 — 재현·복구용)
for s in inject_translations.py add_ko_columns.py patch_scenes.py verify_assets.py \
         extract_textassets.py extract_charset.py apply_font_mapping.py \
         analyze_scene_texts.py install.sh install-windows.ps1 uninstall.sh uninstall-windows.ps1 \
         restore-original.sh; do
    [ -f "scripts/$s" ] && cp "scripts/$s" "$SRC_ROOT/scripts/"
done

cp docs/PLAN.md docs/PROGRESS.md "$SRC_ROOT/docs/"
cp LICENSE "$SRC_ROOT/LICENSE.txt"

( cd "$SRC_ROOT" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 "${HASH_CMD[@]}" > SHA256SUMS )
zip_dir "$SRC_ROOT" "$SRC_ZIP"
echo "  ✅ $SRC_ZIP ($(du -h "$SRC_ZIP" | cut -f1))"

# ── 결과 ──
echo ""
echo "=== 완료 ($VERSION) ==="
ls -lh "$OUT_DIR"
echo ""
echo "업로드 (GitHub Releases):"
echo "  gh release create $VERSION dist/${BASE}-windows.zip dist/${BASE}-macos.zip dist/${BASE}-src.zip \\"
echo "      --title \"$VERSION\" --notes \"...\""
