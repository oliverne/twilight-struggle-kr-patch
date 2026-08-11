#!/usr/bin/env python3
"""씬(level1-3) 하드코딩 텍스트 추출 및 번역 매칭 분석

TextMeshProUGUI.m_text / Text.m_Text 위치를 raw 파싱으로 찾아
하드코딩된 영어 문자열을 추출하고, 번역 소스(런타임 TSV + 수동)와 매칭한다.

사용법:
  python scripts/analyze_scene_texts.py --gamepath <게임루트> [--report <출력.json>]

출력:
  - 매칭 번역 목록 (씬 패치에 사용)
  - 미매칭 문자열 리포트 (수동 번역 필요)
"""
import argparse
import json
import struct
import sys
from pathlib import Path

import UnityPy
from UnityPy.enums.ClassIDType import ClassIDType
from UnityPy.helpers.Tpk import get_typetree_node

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# TextMeshProUGUI: m_text @ head_end+56, Text: m_Text @ head_end+112 (실측값)
TMP_TEXT_DELTA = 56
LEGACY_TEXT_DELTA = 112

TEXT_CLASSES = ("TextMeshProUGUI", "Text")
IGNORE_PATTERNS = ("${", "http://", "https://", "www.", "Message text goes here!")

import re

def normalize_key(s: str) -> str:
    """\r\n/\r → \n, 연속 공백 축소, 앞뒤 공백 제거"""
    t = s.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n[ \t]+", "\n", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def is_noise(s: str) -> bool:
    """번역 불필요 문자열 (숫자/기호/가격 등)"""
    t = s.strip()
    if not re.search(r"[A-Za-z가-힣]", t):
        return True  # 알파벳/한글 없음 (숫자, 기호, 시간 등)
    if re.fullmatch(r"\$[\d.,]+.*", t):
        return True  # 가격
    return False


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
    """Unity 6 MonoBehaviour 헤드 끝 오프셋 (m_Name 직후)"""
    off = 28  # m_GameObject(12) + m_Enabled(1)+pad(3) + m_Script(12)
    nlen = struct.unpack_from("<i", raw, off)[0]
    if nlen < 0 or nlen > 200:
        return -1
    return off + 4 + nlen + pad4(4 + nlen)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gamepath", required=True)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    game = Path(args.gamepath)
    data = game / "TwilightStruggle_Data"
    levels = ["level1", "level2", "level3"]

    # 번역 소스: 런타임 TSV
    base = Path(__file__).resolve().parent.parent
    tsv = json.loads((base / "translation/runtime-20260315.json").read_text("utf-8"))["entries"]
    ko_map = {}
    for e in tsv:
        orig = e.get("original", "")
        ko = e.get("translation_ko", "")
        if orig and ko:
            ko_map[orig] = ko
    manual = json.loads((base / "translation/manual-extra.json").read_text("utf-8"))

    # 씬 문자열 수집
    texts = {}  # 문자열 -> [객체 위치]
    for level in levels:
        env = UnityPy.load(str(data / level))
        env.load_file(str(data / "globalgamemanagers.assets"))
        mb_node = get_typetree_node(ClassIDType.MonoBehaviour, env.file.version)
        for obj in env.objects:
            if obj.type.name != "MonoBehaviour" or level not in obj.assets_file.name:
                continue
            head = obj.parse_monobehaviour_head(mb_node)
            script = head.m_Script.deref_parse_as_object()
            if script.m_ClassName not in TEXT_CLASSES:
                continue
            raw = obj.get_raw_data()
            he = head_end(raw)
            if he < 0:
                continue
            delta = TMP_TEXT_DELTA if script.m_ClassName == "TextMeshProUGUI" else LEGACY_TEXT_DELTA
            s = parse_string_at(raw, he + delta)
            if s is None or len(s.strip()) == 0:
                continue
            if any(p in s for p in IGNORE_PATTERNS):
                continue
            if any("\uac00" <= ch <= "\ud7af" for ch in s):
                continue  # 이미 한글
            texts.setdefault(s, []).append(f"{level}#{obj.path_id}")

    # 정규화 매칭용 인덱스 (개행/공백 변형 흡수)
    norm_index = {}
    for orig, ko in ko_map.items():
        norm_index.setdefault(normalize_key(orig), ko)

    print(f"고유 하드코딩 문자열: {len(texts)}")

    matched = {}
    unmatched = {}
    skipped_noise = 0
    for s, locs in sorted(texts.items()):
        if is_noise(s):
            skipped_noise += 1
            continue
        ko = ko_map.get(s) or norm_index.get(normalize_key(s)) or manual.get("TS_Ingame", {}).get(s) or manual.get("TS_Strings", {}).get(s)
        if ko:
            matched[s] = {"ko": ko, "locs": locs[:5], "total": len(locs)}
        else:
            unmatched[s] = locs[:5]

    print(f"번역 매칭: {len(matched)} / {len(texts)} (노이즈 제외 {skipped_noise}) — {100*len(matched)/max(1,len(texts)-skipped_noise):.1f}% (노이즈 제외 기준)")
    print(f"미매칭: {len(unmatched)}")

    print("\n=== 매칭된 번역 (씬 패치 적용 대상) ===")
    for s, info in matched.items():
        print(f"  {info['total']:3d}×  {s[:55]!r} => {info['ko'][:40]!r}")

    print("\n=== 미매칭 (수동 번역 필요) ===")
    for s, locs in unmatched.items():
        print(f"  {s[:80]!r}  @{locs[:3]}")

    if args.report:
        out = {
            "source": str(data),
            "matched": {s: v["ko"] for s, v in matched.items()},
            "matched_details": matched,
            "unmatched": unmatched,
        }
        Path(args.report).write_text(json.dumps(out, ensure_ascii=False, indent=1), "utf-8")
        print(f"\n→ {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
