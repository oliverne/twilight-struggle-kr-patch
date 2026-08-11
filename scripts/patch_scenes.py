#!/usr/bin/env python3
"""씬(level1-3) 하드코딩 텍스트 한글 패치

TextMeshProUGUI.m_text(head_end+56) / Text.m_Text(head_end+112)를 raw 레벨에서
찾아 번역 소스(런타임 TSV 정확/정규화 매칭 + 수동 번역)와 매칭되는 경우
한국어로 교체한다. MonoBehaviour 헤드(m_Script 참조)는 건드리지 않으며,
blob은 head + 새 문자열 + 나머지 순으로 재구성한다.

사용법:
  python scripts/patch_scenes.py --gamepath <게임루트> [--outdir <출력폴더>]
  python scripts/patch_scenes.py --gamepath <게임루트> --apply

  기본: 패치된 level 파일을 --outdir(기본: patched/)에 저장
  --apply: 원본을 original/에 백업하고 Steam 폴더에 직접 적용
"""
import argparse
import json
import re
import shutil
import struct
import sys
from pathlib import Path

import UnityPy
from UnityPy.enums.ClassIDType import ClassIDType
from UnityPy.helpers.Tpk import get_typetree_node

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TMP_TEXT_DELTA = 56
LEGACY_TEXT_DELTA = 112
LEVELS = ["level1", "level2", "level3"]


def pad4(n: int) -> int:
    return (4 - n % 4) % 4


def parse_string_at(raw: bytes, off: int):
    if off + 4 > len(raw):
        return None
    ln = struct.unpack_from("<i", raw, off)[0]
    if ln < 0 or ln > 500 or off + 4 + ln > len(raw):
        return None
    try:
        return raw[off + 4 : off + 4 + ln].decode("utf-8")
    except UnicodeDecodeError:
        return None


def head_end(raw: bytes) -> int:
    """Unity 6 MonoBehaviour 헤드 끝 (m_Name 직후)"""
    off = 28
    nlen = struct.unpack_from("<i", raw, off)[0]
    if nlen < 0 or nlen > 200:
        return -1
    return off + 4 + nlen + pad4(4 + nlen)


def encode_string(s: str) -> bytes:
    b = s.encode("utf-8")
    return struct.pack("<i", len(b)) + b + b"\x00" * pad4(4 + len(b))


def normalize_key(s: str) -> str:
    t = s.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n[ \t]+", "\n", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def load_translation_maps(base: Path) -> tuple[dict, dict, dict]:
    """(정확 매칭 맵, 정규화 매칭 맵, 수동 맵)"""
    tsv = json.loads((base / "translation/runtime-20260315.json").read_text("utf-8"))["entries"]
    exact = {}
    for e in tsv:
        orig = e.get("original", "")
        ko = e.get("translation_ko", "")
        if orig and ko:
            exact[orig] = ko
    norm = {}
    for orig, ko in exact.items():
        norm.setdefault(normalize_key(orig), ko)

    manual = {}
    for fname in ("manual-extra.json", "manual-scenes.json"):
        p = base / "translation" / fname
        if p.exists():
            d = json.loads(p.read_text("utf-8"))
            manual.update(d.get("manual", {}))
    return exact, norm, manual


def patch_level(work_path: Path, out_path: Path, game: Path, exact: dict, norm: dict, manual: dict) -> tuple[int, int]:
    """level 파일 1개 패치 → (변경 객체 수, 미변경 매칭 수)

    work_path(복사본)를 로드하고 out_path(별도 파일)에 저장한다.
    같은 파일에 저장하면 지연 스트리밍(Replacer)이 깨지므로 반드시 분리한다.
    """
    env = UnityPy.load(str(work_path))
    env.load_file(str(game / "TwilightStruggle_Data/globalgamemanagers.assets"))

    # typetree_generator 설정 (m_Script 보존 — Phase 4 방식)
    from TypeTreeGeneratorAPI import TypeTreeGenerator

    unity_version = getattr(env.file, "unity_version", None) or "6000.0.58f2"
    gen = TypeTreeGenerator(str(unity_version))
    gen.load_il2cpp(
        (game / "GameAssembly.dll").read_bytes(),
        (game / "TwilightStruggle_Data/il2cpp_data/Metadata/global-metadata.dat").read_bytes(),
    )
    env.typetree_generator = gen

    mb_node = get_typetree_node(ClassIDType.MonoBehaviour, env.file.version)
    changed_objs = 0
    changed_strings = 0
    skipped = 0

    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or work_path.name not in obj.assets_file.name:
            continue
        head = obj.parse_monobehaviour_head(mb_node)
        script = head.m_Script.deref_parse_as_object()
        if script.m_ClassName not in ("TextMeshProUGUI", "Text"):
            continue
        delta = TMP_TEXT_DELTA if script.m_ClassName == "TextMeshProUGUI" else LEGACY_TEXT_DELTA

        raw = obj.get_raw_data()
        he = head_end(raw)
        if he < 0:
            continue
        old = parse_string_at(raw, he + delta)
        if old is None or len(old.strip()) == 0:
            continue
        if any("\uac00" <= ch <= "\ud7af" for ch in old):
            continue  # 이미 한글 → 멱등성

        new = exact.get(old) or norm.get(normalize_key(old)) or manual.get(old)
        if not new:
            skipped += 1
            continue

        # blob 재구성: head + m_text(새) + 나머지
        old_str_off = he + delta
        old_len = struct.unpack_from("<i", raw, old_str_off)[0]
        old_str_end = old_str_off + 4 + old_len + pad4(4 + old_len)
        new_blob = raw[:old_str_off] + encode_string(new) + raw[old_str_end:]
        obj.set_raw_data(new_blob)
        changed_objs += 1
        changed_strings += 1

    # 저장 (무손상: fork + typetree_generator) — work_path와 다른 out_path로 저장
    with open(out_path, "wb") as f:
        f.write(env.file.save(packer="original"))
    env.file.close()
    return changed_objs, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gamepath", required=True)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--apply", action="store_true", help="Steam 폴더에 직접 적용 (백업 후)")
    args = ap.parse_args()

    game = Path(args.gamepath)
    data = game / "TwilightStruggle_Data"
    base = Path(__file__).resolve().parent.parent

    exact, norm, manual = load_translation_maps(base)
    print(f"번역 소스: 정확 {len(exact)} / 정규화 {len(norm)} / 수동 {len(manual)}")

    outdir = Path(args.outdir) if args.outdir else base / "patched"
    outdir.mkdir(parents=True, exist_ok=True)

    for level in LEVELS:
        src = data / level
        if not src.exists():
            print(f"  ⚠️ {level} 없음 — 건너뜀")
            continue
        work = outdir / f"{level}.work"
        dst = outdir / level
        shutil.copy2(src, work)
        changed, skipped = patch_level(work, dst, game, exact, norm, manual)
        try:
            work.unlink(missing_ok=True)
        except PermissionError:
            pass  # 파일 핸들이 남아있으면 삭제 실패할 수 있음 — 무시
        print(f"  {level}: 변경 {changed}개 객체 / 매칭 없음 {skipped}개 → {dst}")

    if args.apply:
        backup_dir = data / "backup-20260811"
        backup_dir.mkdir(exist_ok=True)
        for level in LEVELS:
            src = data / level
            if not src.exists():
                continue
            shutil.copy2(src, backup_dir / f"{level}.pre-scene-patch")
            shutil.copy2(outdir / level, src)
        print("  → Steam 설치본에 적용 완료 (백업: backup-20260811/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
