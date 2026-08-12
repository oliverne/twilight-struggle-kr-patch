#!/usr/bin/env python3
"""humanizer 2차: 수동 교정(translation/polish-runtime.json)을 런타임 번역에 반영.

- source_line → 교정된 번역 전체 (EN 원문 불변)
- 멱등: 이미 교정된 항목은 변화 없음
- diff는 dist/polish-2.diff

사용: python3 scripts/apply_polish.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLISH = ROOT / "translation" / "polish-runtime.json"
RUNTIME = ROOT / "translation" / "runtime-20260315.json"


def main():
    polish = json.loads(POLISH.read_text(encoding="utf-8"))["entries"]
    data = json.loads(RUNTIME.read_text(encoding="utf-8"))
    by_line = {e["source_line"]: e for e in data["entries"]}
    diff = []
    applied = 0
    missing = []
    for ln, new_ko in polish.items():
        ln = int(ln)
        e = by_line.get(ln)
        if e is None:
            missing.append(ln)
            continue
        old_ko = e["translation_ko"]
        if old_ko == new_ko:
            continue
        e["translation_ko"] = new_ko
        e["polished_at"] = "2026-08-12"
        applied += 1
        diff.append(f"--- L{ln}")
        diff.append(f"- {old_ko[:200]}")
        diff.append(f"+ {new_ko[:200]}")
    if applied:
        RUNTIME.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "polish-2.diff").write_text("\n".join(diff), encoding="utf-8")
    print(f"적용: {applied}개 / 미발견 라인: {missing}")


if __name__ == "__main__":
    main()
