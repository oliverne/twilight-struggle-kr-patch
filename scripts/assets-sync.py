#!/usr/bin/env python3
"""patched/*/*.assets 를 git 공유용으로 압축/해제하는 스크립트

배경:
  patched/*/*.assets 는 100MB+ (GitHub 100MB 단일 파일 제한 초과) + 플랫폼별(맥/윈도우)로
  별도 생성되는 대형 산출물이라 gitignore 대상이다. 하지만 gzip 압축 시 ~8MB로
  줄어들어 .assets.gz 로 git 추적이 가능하다 (Git LFS 불필요 — 2026-08-15 확정).

  - .assets      : 로컬 작업 실체 (gitignore — 패치 파이프라인이 재생성)
  - .assets.gz   : git 추적 — 전송용 결정적 압축본
  - 작업 후 push 전에 compress, pull/checkout 후에 decompress 하면 된다.

사용법:
  python scripts/assets-sync.py status              # 상태만 출력 (파일 변경 없음)
  python scripts/assets-sync.py compress           # .assets → .assets.gz (갱신분만)
  python scripts/assets-sync.py decompress         # .assets.gz → .assets (갱신분만)
  python scripts/assets-sync.py compress --force   # 갱신 여부 무시하고 전체 재압축

동작:
  compress   — .gz가 없거나 .assets가 .gz보다 새로우면 재압축 + 왕복 검증
  decompress — .assets가 없거나 .gz가 .assets보다 새로우면 해제
  처리 후 양쪽 mtime을 맞춰 '동기화됨' 상태를 유지한다 (mtime 기반 판정의 안정화).

결정적 압축:
  gzip 헤더를 직접 작성해 mtime=0, OS=255(unknown) 고정 — 내용이 같으면
  바이트가 항상 동일하므로 git diff 노이즈가 없다 (Python 버전/OS 무관).
"""

import argparse
import shutil
import struct
import sys
import zlib
from pathlib import Path

# Windows 콘솔(cp949)에서 UTF-8 출력 보장
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = Path(__file__).resolve().parent.parent
PATCHED_DIR = PROJECT_DIR / "patched"

GZIP_HEADER = b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff"  # mtime=0, XFL=2, OS=255
CHUNK = 1 << 20


def find_pairs() -> list[tuple[Path, Path]]:
    """patched/*/*.assets 와 대응 .assets.gz 쌍 목록 (사전순 정렬)"""
    pairs = []
    for assets in sorted(PATCHED_DIR.glob("*/*.assets")):
        pairs.append((assets, assets.with_name(assets.name + ".gz")))
    return pairs


def gzip_compress(src: Path, dst: Path) -> None:
    """결정적 gzip 압축 (헤더 직접 작성 — mtime/OS 바이트 고정)"""
    comp = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    crc = 0
    isize = 0
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        fout.write(GZIP_HEADER)
        while True:
            chunk = fin.read(CHUNK)
            if not chunk:
                break
            crc = zlib.crc32(chunk, crc) & 0xFFFFFFFF
            isize += len(chunk)
            fout.write(comp.compress(chunk))
        fout.write(comp.flush())
        fout.write(struct.pack("<II", crc, isize & 0xFFFFFFFF))


def verify_roundtrip(gz: Path, src: Path) -> bool:
    """압축본을 스트리밍 해제해 원본과 바이트 비교"""
    import gzip as _gzip

    with _gzip.open(gz, "rb") as fin, open(src, "rb") as fref:
        while True:
            a = fin.read(CHUNK)
            b = fref.read(CHUNK)
            if a != b:
                return False
            if not a:
                return True


def sync_mtime(a: Path, b: Path) -> None:
    """a의 mtime을 b에 복사 — 이후 상태 판정이 '동기화됨'이 되도록"""
    import os

    os.utime(b, (a.stat().st_mtime, a.stat().st_mtime))


def compress_file(assets: Path, gz: Path, force: bool) -> bool:
    if gz.exists() and not force and assets.stat().st_mtime <= gz.stat().st_mtime:
        return False
    print(f"  [압축] {assets.relative_to(PROJECT_DIR)}")
    gzip_compress(assets, gz)
    if not verify_roundtrip(gz, assets):
        print(f"  [오류] 압축 검증 실패 — {gz.name} 삭제")
        gz.unlink(missing_ok=True)
        return False
    sync_mtime(assets, gz)  # gz mtime = assets mtime (동기화됨 상태)
    print(f"         → {gz.relative_to(PROJECT_DIR)} ({gz.stat().st_size / 1e6:.1f}MB)")
    return True


def decompress_file(gz: Path, assets: Path, force: bool) -> bool:
    if assets.exists() and not force and gz.stat().st_mtime <= assets.stat().st_mtime:
        return False
    print(f"  [해제] {gz.relative_to(PROJECT_DIR)}")
    import gzip as _gzip

    with _gzip.open(gz, "rb") as fin, open(assets, "wb") as fout:
        shutil.copyfileobj(fin, fout, CHUNK)
    sync_mtime(gz, assets)  # assets mtime = gz mtime (동기화됨 상태)
    print(f"         → {assets.relative_to(PROJECT_DIR)}")
    return True


def describe(assets: Path, gz: Path) -> str:
    if not assets.exists() and not gz.exists():
        return "둘 다 없음"
    if not gz.exists():
        return "압축 필요 (gz 없음)"
    if not assets.exists():
        return "해제 필요 (assets 없음)"
    if assets.stat().st_mtime > gz.stat().st_mtime:
        return "압축 필요 (assets가 최신)"
    if gz.stat().st_mtime > assets.stat().st_mtime:
        return "해제 필요 (gz가 최신)"
    return "동기화됨"


def main() -> int:
    ap = argparse.ArgumentParser(description="patched/*/*.assets ↔ .assets.gz 동기화")
    ap.add_argument("command", choices=["status", "compress", "decompress"])
    ap.add_argument("--force", action="store_true", help="갱신 여부 무시하고 전체 처리")
    args = ap.parse_args()

    pairs = find_pairs()
    if not pairs:
        print("[정보] patched/*/*.assets 파일이 없습니다.")
        return 0

    if args.command == "status":
        print("=== patched 에셋 상태 ===")
        for assets, gz in pairs:
            size = f"{assets.stat().st_size / 1e6:.1f}MB" if assets.exists() else "  -  "
            print(f"  {assets.name:24s} {size:>7s}  {describe(assets, gz)}")
        return 0

    if args.command == "compress":
        print("=== 압축 (작업 후, 커밋 전 실행) ===")
        done = 0
        for assets, gz in pairs:
            if compress_file(assets, gz, args.force):
                done += 1
        if done == 0:
            print("  변경 없음 — 모두 최신입니다.")
        else:
            print(f"  {done}개 처리 완료. git add patched/*/*.assets.gz 후 커밋하세요.")
        return 0

    if args.command == "decompress":
        print("=== 해제 (pull/checkout 후 실행) ===")
        done = 0
        for assets, gz in pairs:
            if gz.exists() and decompress_file(gz, assets, args.force):
                done += 1
        if done == 0:
            print("  변경 없음 — 모두 최신입니다.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
