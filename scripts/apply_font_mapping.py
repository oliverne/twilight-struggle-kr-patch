#!/usr/bin/env python3
"""Unity_Font_Replacer의 'Twilight Struggle.json' 매핑 재설정 도구.

parse(또는 새 게임 버전)가 JSON을 초기화하면 Replace_to가 전부 비워진다.
이 스크립트는 기존 폰트 매핑(24개 TMP SDF → 한글 SDF 2종)을 재적용한다.

사용법:
  python scripts/apply_font_mapping.py [--json <경로>] [--dry-run]

기본 경로: tools/unity-font-replacer/Twilight Struggle.json
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 본문 계열 → NotoSerifKR, 제목 계열 → BlackHanSans
# ⚠️ 2026-08-13: IMPACT 3종(트랙 라벨 H가 칸을 벗어나는 문제) → NotoSerifKR(D2Coding 모노스페이스)로 이동
MAPPING = {
    "NotoSerifKR SDF.json": [
        "Unity SDF", "FRADMCN SDF", "FRAMD SDF Outline", "FRAMD SDF",
        "FRAMDCN SDF", "FRAMDIT SDF", "GOTHIC SDF", "GOTHICB Outline SDF",
        "GOTHICB SDF", "LiberationSans SDF - Fallback", "LiberationSans SDF",
        "TIMES SDF", "TIMESI SDF",
        "IMPACT NUM Outline SDF", "IMPACT SDF", "IMPACT Shadow SDF",
    ],
    "BlackHanSans-Regular SDF.json": [
        "Anton SDF", "Bangers SDF", "Electronic Highway Sign SDF",
        "Oswald Bold SDF", "Roboto-Bold SDF", "Gunplay SDF",
        "atwriter_outline SDF", "atwriter SDF",
    ],
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="폰트 매핑 Replace_to 재설정")
    parser.add_argument("--json", default=None, help="매핑 JSON 경로")
    parser.add_argument("--dry-run", action="store_true", help="변경 없이 출력만")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    path = Path(args.json) if args.json else base / "tools/unity-font-replacer/Twilight Struggle.json"
    if not path.exists():
        raise SystemExit(f"매핑 JSON 없음: {path}")

    data = json.loads(path.read_text("utf-8"))
    items = data if isinstance(data, list) else data.get("items", data)
    if isinstance(items, dict):
        items = list(items.values())

    set_cnt = 0
    for it in items:
        nm = it.get("FontName") or it.get("Name") or it.get("name") or ""
        st = it.get("State") or it.get("Type") or it.get("type") or ""
        if st != "SDF":
            continue
        for sdf_name, targets in MAPPING.items():
            if nm in targets:
                it["Replace_to"] = sdf_name
                set_cnt += 1
                break

    print(f"Replace_to 설정: {set_cnt}개 ({path.name})")
    if not args.dry_run:
        json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("저장 완료")


if __name__ == "__main__":
    raise SystemExit(main())
