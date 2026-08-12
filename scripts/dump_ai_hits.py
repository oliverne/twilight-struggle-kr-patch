#!/usr/bin/env python3
"""스캔 히트 전체를 JSON으로 덤프 (원문 포함)."""
import json, re, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import importlib.util
spec = importlib.util.spec_from_file_location('s', 'scripts/scan_ai_patterns.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

TAG_RE = re.compile(r"<[^>]+>")
items = s.collect()
hits = []
for pid, label, en, ko in items:
    ko_plain = TAG_RE.sub("", ko)
    for name, sev, rx, desc in s.PATTERNS:
        for m in rx.finditer(ko_plain):
            hits.append({
                "severity": sev, "pattern": name, "id": pid, "source": label,
                "matched": m.group(0), "context": ko_plain[max(0,m.start()-40):m.end()+40],
                "ko_full": ko, "en_full": en
            })
hits.sort(key=lambda h: (h["severity"], h["pattern"], h["id"]))
with open('dist-ai-hits.json', 'w', encoding='utf-8') as f:
    json.dump(hits, f, ensure_ascii=False, indent=1)
print("dumped", len(hits))
