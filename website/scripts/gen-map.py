#!/usr/bin/env python3
"""세계지도 도트맵 마스크 생성기 — Wikimedia Commons 공개 도메인 지도 기반.

산출물 (website/public/img/):
  world-mask-west.png  — 미주(서반구) 육지 마스크 (파랑 도트용)
  world-mask-east.png  — 유라시아·아프리카 육지 마스크 (빨강 도트용)

CSS에서 dot 패턴 배경 + mask-image로 도트 세계지도를 그린다.
재실행: .venv/bin/python website/scripts/gen-map.py
"""
from __future__ import annotations

import io
import os
import subprocess
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
W, H = 1000, 500  # 마스크 해상도 (도트 패턴은 CSS가 담당)


def fetch() -> bytes:
    req = urllib.request.Request(SRC_URL, headers={"User-Agent": "twilight-struggle-kr-patch-site/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def svg_to_png(svg: bytes) -> PIL.Image.Image:
    src = os.path.join("/tmp", "world-map.svg")
    with open(src, "wb") as f:
        f.write(svg)
    png = os.path.join("/tmp", "world-map.png")
    subprocess.run(["sips", "-s", "format", "png", "--resampleWidth", str(W * 2), src, "--out", png],
                   check=True, capture_output=True)
    img = PIL.Image.open(png).convert("RGB")
    img = img.resize((W, H), PIL.Image.LANCZOS)
    return img


def mask(img: PIL.Image.Image, west: bool) -> PIL.Image.Image:
    """육지=흰색(불투명), 바다=투명. west=True면 SPLIT_LON 서쪽만."""
    px = img.load()
    out = PIL.Image.new("RGBA", (W, H), (0, 0, 0, 0))
    opx = out.load()
    for y in range(H):
        lon = 180.0 - (y + 0.5) / H * 360.0  # sips는 상단이 북쪽
        if (lon >= SPLIT_LON) != west:  # y→lon 매핑 확인 후 대입
            pass
        for x in range(W):
            lon2 = -180.0 + (x + 0.5) / W * 360.0
            in_west = lon2 < SPLIT_LON
            if in_west != west:
                continue
            r, g, b = px[x, y]
            if r < 235 and g < 235 and b < 235:  # 육지(어두운 픽셀)
                opx[x, y] = (255, 255, 255, 255)
    return out


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    svg = fetch()
    img = svg_to_png(svg)
    for name, west in (("world-mask-west", True), ("world-mask-east", False)):
        m = mask(img, west)
        path = os.path.join(OUT, name + ".png")
        m.save(path)
        print("ok:", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
