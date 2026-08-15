#!/usr/bin/env python3
"""히어로 도트 세계지도 마스크 생성기 — 냉전 진영 분할(파랑 vs 빨강).

Wikimedia Commons 공개 도메인 국가 경로 SVG(land=알파 255, sea=알파 0)를
rsvg-convert로 렌더링한 뒤, **알파 채널**로 육지를 판별해 이진 마스크를 만든다.
경도 -35°(대서양 중앙) 기준으로 서반구(미주·그린란드=파랑)와
동반구(아프리카·유라시아·호주=빨강)를 나눈다.

산출물 (website/public/img/, 각 1000x500):
  world-mask-west.png  — 서반구 육지 알파 마스크 (파랑 도트용)
  world-mask-east.png  — 동반구 육지 알파 마스크 (빨강 도트용)

CSS(.dotmap .west/.east 의 mask-image)에서 덮어씌운다.

재실행:
  /Users/oliverne/Projects/twilight-struggle-kr-patch/.venv/bin/python \\
      website/scripts/gen-map.py

요구: rsvg-convert(librsvg), Pillow.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request

import PIL.Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "img")
SRC_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/8/80/"
    "World_map_-_low_resolution.svg"
)
# -35° 경도: 대서양 중앙 — 서쪽=미주(파랑 진영), 동쪽=유라시아·아프리카(빨강 진영)
SPLIT_LON = -35.0
RENDER_W, RENDER_H = 2000, 1000  # 고해상도 렌더 → 축소로 매끄러운 해안
OUT_W, OUT_H = 1000, 500  # 마스크 해상도 (도트 패턴 자체는 CSS가 담당)
ALPHA_LAND = 128  # 알파>=128 = 육지


def fetch_svg() -> bytes:
    req = urllib.request.Request(
        SRC_URL, headers={"User-Agent": "twilight-struggle-kr-patch-site/0.1"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def render(svg: bytes) -> PIL.Image.Image:
    """SVG -> RGBA. land=알파 255(경로 기본 검정 fill), sea=알파 0(투명)."""
    for tool in ("rsvg-convert",):
        if shutil.which(tool):
            break
    else:
        sys.exit("rsvg-convert(librsvg)가 필요합니다. `brew install librsvg` 후 재시도.")
    tmp = tempfile.mkdtemp(prefix="svgmap-")
    src = os.path.join(tmp, "src.svg")
    with open(src, "wb") as f:
        f.write(svg)
    rgba_path = os.path.join(tmp, "render.png")
    subprocess.run(
        ["rsvg-convert", "-w", str(RENDER_W), "-h", str(RENDER_H), src, "-o", rgba_path],
        check=True,
        capture_output=True,
    )
    return PIL.Image.open(rgba_path).convert("RGBA").resize((OUT_W, OUT_H), PIL.Image.LANCZOS)


def land_mask(rgba: PIL.Image.Image) -> PIL.Image.Image:
    """알파 채널 → 이진 육지 마스크(L 모드). land=255, sea=0. 축소 AA 재이진화."""
    alpha = rgba.getchannel("A")
    return alpha.point(lambda v: 255 if v >= ALPHA_LAND else 0).convert("L")


def split_mask(land: PIL.Image.Image, west: bool) -> PIL.Image.Image:
    """전체 OUT_W x OUT_H 마스크. west=True면 SPLIT_LON 서쪽 육지만, 아니면 동쪽만."""
    x_split = round((SPLIT_LON + 180.0) / 360.0 * OUT_W)
    rgba = PIL.Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    px = land.load()
    opx = rgba.load()
    for y in range(OUT_H):
        x0, x1 = (0, x_split) if west else (x_split, OUT_W)
        for x in range(x0, x1):
            if px[x, y] >= 250:  # 육지
                opx[x, y] = (255, 255, 255, 255)
    return rgba


def coverage(rgba: PIL.Image.Image) -> tuple[int, float]:
    """디버그: 불투명 알카 픽셀 수와 비율."""
    a = rgba.getchannel("A")
    vals = a.get_flattened_data() if hasattr(a, "get_flattened_data") else list(a.getdata())
    opq = sum(1 for v in vals if v >= 250)
    return opq, opq / (rgba.size[0] * rgba.size[1])


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    svg = fetch_svg()
    rgba = render(svg)
    land = land_mask(rgba)
    for name, west in (("world-mask-west", True), ("world-mask-east", False)):
        m = split_mask(land, west)
        path = os.path.join(OUT, name + ".png")
        m.save(path)
        opx, frac = coverage(m)
        side = "서반구(미주)" if west else "동반구(구대륙)"
        print(f"ok: {path}  {side}  육지 {opx}px = {frac*100:.2f}%")
    ln, lf = coverage(land.convert("RGBA"))
    print(f"전체 육지 {ln}px = {lf*100:.2f}% (지구 실제 ~29%)")


if __name__ == "__main__":
    main()