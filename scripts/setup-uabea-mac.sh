#!/usr/bin/env bash
# UABEA macOS 설치/복구 스크립트 (멱등)
# UABEA는 공식 macOS 빌드가 없어 ubuntu 빌드 + macOS 네이티브 라이브러리 조합으로 실행한다.
set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "$0")/../tools" && pwd)"
UABEA_DIR="$TOOLS_DIR/uabea"
UABEA_URL="https://github.com/nesrak1/UABEA/releases/download/v8/uabea-ubuntu.zip"

command -v dotnet >/dev/null || { echo "dotnet 미설치: brew install dotnet"; exit 1; }

# 1. UABEA 본체 다운로드 (이미 있으면 건너뜀)
if [ ! -f "$UABEA_DIR/UABEAvalonia.dll" ]; then
  echo "UABEA v8 다운로드..."
  TMP="$(mktemp -d)"
  curl -sL -o "$TMP/uabea.zip" "$UABEA_URL"
  mkdir -p "$UABEA_DIR"
  unzip -q -o "$TMP/uabea.zip" -d "$UABEA_DIR"
  rm -rf "$TMP"
fi

# 2. macOS 네이티브 라이브러리 보강 (NuGet)
NATIVE_DIR="$UABEA_DIR/runtimes/osx/native"
mkdir -p "$NATIVE_DIR"
fetch_nuget_native() {
  local pkg="$1" ver="$2" lib="$3"
  [ -f "$NATIVE_DIR/$lib" ] && { echo "$lib 존재, 건너뜀"; return; }
  echo "$lib 다운로드 ($pkg $ver)..."
  local TMP; TMP="$(mktemp -d)"
  curl -sL -o "$TMP/pkg.nupkg" "https://www.nuget.org/api/v2/package/$pkg/$ver"
  unzip -q -o "$TMP/pkg.nupkg" 'runtimes/osx/native/*' -d "$TMP/ext"
  cp "$TMP/ext/runtimes/osx/native/$lib" "$NATIVE_DIR/"
  rm -rf "$TMP"
}
fetch_nuget_native SkiaSharp.NativeAssets.macOS 2.88.3 libSkiaSharp.dylib
fetch_nuget_native HarfBuzzSharp.NativeAssets.macOS 2.8.2.3 libHarfBuzzSharp.dylib
fetch_nuget_native Avalonia.Native 11.0.1 libAvaloniaNative.dylib

echo ""
echo "완료. 실행 방법:"
echo "  DOTNET_ROLL_FORWARD=LatestMajor dotnet $UABEA_DIR/UABEAvalonia.dll"
