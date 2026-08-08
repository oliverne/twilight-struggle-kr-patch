#!/usr/bin/env python3
"""Phase 4: 번역 소스를 resources.assets TextAsset에 주입한다.

전략:
  - Common_Strings: RU(10열) → KO로 교체 (헤더 "RU"→"KO", 322행→한글)
  - TS_Cards: row-key 기반 col 2(EN) → 한국어 교체
  - TS_Ingame: key 기반 EN→KO (런타임 TSV에서 117/157행 커버)
  - Common_Ingame: key 기반 EN→KO (수동 번역 포함, 22행)
  - TS_Strings: key 기반 EN→KO (런타임 TSV에서 38/50행 커버)
  - TS_RulesTutorial: 건너뜀 (File/String 참조만 있고 표시 텍스트 아님)
  - AvailableCultures: ru → ko (한국어 선택 가능하게)
  - EN 열(2열)은 절대 수정하지 않음

사용법:
  python scripts/inject_translations.py [--target original|patched]

출력:
  patched/resources.assets (수정된 에셋)
"""

import json
import struct
import sys
from pathlib import Path


def pad4(n: int) -> int:
    return (4 - n % 4) % 4


def parse_raw_textasset(raw: bytes) -> tuple[str, bytes]:
    name_len = struct.unpack_from("<i", raw, 0)[0]
    name = raw[4 : 4 + name_len].decode("utf-8")
    off = 4 + name_len + pad4(4 + name_len)
    script_len = struct.unpack_from("<i", raw, off)[0]
    script = raw[off + 4 : off + 4 + script_len]
    return name, script


def encode_textasset(name: str, script: bytes) -> bytes:
    name_bytes = name.encode("utf-8")
    buf = bytearray()
    buf += struct.pack("<i", len(name_bytes))
    buf += name_bytes
    buf += b"\x00" * pad4(4 + len(name_bytes))
    buf += struct.pack("<i", len(script))
    buf += script
    buf += b"\x00" * pad4(len(script))
    return bytes(buf)


def build_key_to_ko(translations: dict) -> dict:
    """translation JSON에서 key → 한글 매핑"""
    mapping = {}
    for row in translations.get("rows", []):
        k = row.get("key", "")
        ko = row.get("ko", "")
        if k and ko and k != "Key":
            mapping[k] = ko
    return mapping


def build_rt_index() -> dict:
    """런타임 TSV에서 EN→KO 인덱스 구축"""
    base = Path(__file__).resolve().parent.parent
    rt = json.loads((base / "translation/runtime-20260315.json").read_text("utf-8"))
    return {e["original"]: e["translation_ko"] for e in rt["entries"]}


def inject_simple_table(text: str, key_to_ko: dict, rt_index: dict, manual: dict) -> tuple[str, int]:
    """TS_Ingame, Common_Ingame, TS_Strings: key → EN 교체
    
    우선순위: key_to_ko > rt_index > manual
    """
    date_end = text.index("\n") + 1
    date_line = text[:date_end]
    data = json.loads(text[date_end:].strip())
    cells = data.get("0", {})
    changed = 0
    
    for cell_key, val in list(cells.items()):
        if ":" not in cell_key:
            continue
        _, col = cell_key.split(":", 1)
        if col != "2" or val in ("null", "", "EN", "ENTER PATH"):
            continue
        
        ko = key_to_ko.get(val) or rt_index.get(val) or manual.get(val)
        if ko:
            cells[cell_key] = ko
            changed += 1
    
    return date_line + json.dumps(data, ensure_ascii=False, separators=(",", ":")), changed


def inject_common_strings(text: str, key_to_ko: dict) -> tuple[str, int]:
    """Common_Strings: RU(10열) → KO"""
    date_end = text.index("\n") + 1
    date_line = text[:date_end]
    data = json.loads(text[date_end:].strip())
    
    # 셀 데이터는 "0" 키 아래 column:row 형식
    cells = data.setdefault("0", {})
    changed = 0
    
    for row_num in range(2, 324):  # row 2~323 (row 1은 header)
        key_cell = f"{row_num}:1"
        ru_cell = f"{row_num}:10"
        key_name = cells.get(key_cell, "")
        if key_name in key_to_ko:
            cells[ru_cell] = key_to_ko[key_name]
            changed += 1
    
    cells["1:10"] = "KO"  # header: RU → KO
    return date_line + json.dumps(data, ensure_ascii=False, separators=(",", ":")), changed


def inject_tscards(text: str, key_to_ko: dict) -> tuple[str, int]:
    """TS_Cards: row-key 기반 EN(2열) → 한글 교체
    
    TS_Cards 구조: data["0"] = header, data[timestamp] = 실제 데이터 셀
    각 row는 col:row 형태의 셀로 구성, col 1 = path, col 2 = EN
    """
    date_end = text.index("\n") + 1
    date_line = text[:date_end]
    data = json.loads(text[date_end:].strip())
    
    changed = 0
    
    for top_key, cells in data.items():
        if top_key == "0" or not isinstance(cells, dict):
            continue
        
        # col 1 (path) 기준으로 row → key 매핑 구축
        row_to_key = {}
        for cell_key, value in cells.items():
            if ":" not in cell_key:
                continue
            row_s, col_s = cell_key.split(":", 1)
            if col_s == "1" and value and value != "null":
                row_to_key[int(row_s)] = value
        
        # 각 row에 대해 번역 주입 (col 2 = EN → 한국어)
        for row_num, key_name in row_to_key.items():
            if key_name in key_to_ko:
                en_cell = f"{row_num}:2"
                if en_cell in cells:
                    cells[en_cell] = key_to_ko[key_name]
                    changed += 1
    
    return date_line + json.dumps(data, ensure_ascii=False, separators=(",", ":")), changed


def inject_available_cultures(text: str) -> str:
    """AvailableCultures XML: ru → ko"""
    text = text.replace(
        "<languageCode>ru</languageCode>", "<languageCode>ko</languageCode>"
    )
    text = text.replace(
        "<englishName>Russian</englishName>", "<englishName>Korean</englishName>"
    )
    text = text.replace(
        "<nativeName>Русский</nativeName>", "<nativeName>한국어</nativeName>"
    )
    return text


def main():
    base = Path(__file__).resolve().parent.parent
    
    import UnityPy
    
    # 번역 소스 로드
    strings = json.loads((base / "translation/strings.json").read_text("utf-8"))
    cards = json.loads((base / "translation/cards.json").read_text("utf-8"))
    key_to_ko_cs = build_key_to_ko(strings)
    key_to_ko_cards = build_key_to_ko(cards)
    rt_index = build_rt_index()
    
    # Common_Ingame 수동 번역 (런타임 TSV 커버 불가)
    common_ingame_manual = {
        "Are you sure you want to end your turn?": "턴을 종료하시겠습니까?",
        "Your timer has expired! <br>You have forfeited this game.": "시간이 만료되었습니다!<br>게임에서 기권 처리되었습니다.",
        "All opponents have forfeited.  You win!": "모든 상대가 기권했습니다. 승리!",
        "Loading... %d%%": "로딩 중... %d%%",
        "Play": "사용",
        "Buy": "구매",
        "Copy": "복사",
        "Delete": "삭제",
        "Reveal": "공개",
        "Discard": "버리기",
        "Target": "대상",
        "Select": "선택",
        "Defend": "방어",
        "Use": "사용",
        "Give": "주기",
        "You May End Your Turn": "턴을 종료할 수 있습니다",
        "You Must End Your Turn": "턴을 종료해야 합니다",
        "OK": "확인",
        "Undo": "실행 취소",
        "Dismiss": "닫기",
        "Commit": "확정",
        "Not a valid target": "유효한 대상이 아닙니다",
    }
    
    print(f"Common_Strings keys: {len(key_to_ko_cs)}")
    print(f"TS_Cards keys: {len(key_to_ko_cards)}")
    print(f"Runtime TSV entries: {len(rt_index)}")
    
    # 원본 로드
    src_path = base / "original/resources.assets"
    env = UnityPy.load(str(src_path))
    
    results = {}
    
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw_textasset(obj.get_raw_data())
        text = script.decode("utf-8")
        new_text = None
        
        if name == "Common_Strings":
            new_text, changed = inject_common_strings(text, key_to_ko_cs)
            print(f"  Common_Strings: {changed}행 (RU→KO)")
            results["Common_Strings"] = changed
        
        elif name == "TS_Cards":
            new_text, changed = inject_tscards(text, key_to_ko_cards)
            print(f"  TS_Cards: {changed}행 (EN→KO)")
            results["TS_Cards"] = changed
        
        elif name == "TS_Ingame":
            new_text, changed = inject_simple_table(text, {}, rt_index, {})
            print(f"  TS_Ingame: {changed}행 (EN→KO)")
            results["TS_Ingame"] = changed
        
        elif name == "Common_Ingame":
            new_text, changed = inject_simple_table(text, {}, rt_index, common_ingame_manual)
            print(f"  Common_Ingame: {changed}행 (EN→KO)")
            results["Common_Ingame"] = changed
        
        elif name == "TS_Strings":
            new_text, changed = inject_simple_table(text, {}, rt_index, {})
            print(f"  TS_Strings: {changed}행 (EN→KO)")
            results["TS_Strings"] = changed
        
        elif name == "AvailableCultures":
            new_text = inject_available_cultures(text)
            print(f"  AvailableCultures: ru → ko")
            results["AvailableCultures"] = True
        
        if new_text is not None:
            new_raw = encode_textasset(name, new_text.encode("utf-8"))
            obj.set_raw_data(new_raw)
    
    # 저장
    out_dir = base / "patched"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "resources.assets"
    with open(out_path, "wb") as f:
        f.write(env.file.save(packer="original"))
    
    print(f"\n→ {out_path}")
    
    # EN 보존 검증
    print("\n=== EN 열 보존 검증 ===")
    env2 = UnityPy.load(str(out_path))
    for obj2 in env2.objects:
        if obj2.type.name != "TextAsset":
            continue
        name2, script2 = parse_raw_textasset(obj2.get_raw_data())
        if name2 == "Common_Strings":
            text2 = script2.decode("utf-8")
            date_end2 = text2.index("\n") + 1
            data2 = json.loads(text2[date_end2:].strip())
            cells2 = data2.get("0", {})
            en_ok = True
            for r in range(2, min(324, 10)):
                en_val = cells2.get(f"{r}:2", "")
                ko_val = cells2.get(f"{r}:10", "")
                if en_val == ko_val and en_val not in ("null", "", "EN"):
                    en_ok = False
                    print(f"  ❌ Row {r}: EN == KO ({en_val})")
            if en_ok:
                print(f"  ✅ Common_Strings EN 열 무결함")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
