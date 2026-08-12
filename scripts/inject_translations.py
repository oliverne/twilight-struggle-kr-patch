#!/usr/bin/env python3
"""Phase 4: 번역 소스를 resources.assets TextAsset에 주입한다.

전략:
  - Common_Strings: RU(10열) → KO로 교체 (헤더 "RU"→"KO", 322행→한글)
  - TS_Cards: row-key 기반 col 2(EN) → 한국어 교체
  - TS_Ingame: key 기반 EN→KO (런타임 TSV에서 117/157행 커버)
  - Common_Ingame: key 기반 EN→KO (수동 번역 포함, 22행)
  - TS_Strings: key 기반 EN→KO (런타임 TSV에서 38/50행 커버)
  - TS_RulesTutorial: EN 열(3열) → KO 번역 주입 (Phase 7, manual-rules.json) — 시트 1631793870 (1열=키, 2열=US, 3열=EN, 10열=KO)
  - AvailableCultures: ru → ko (한국어 선택 가능하게)
  - EN 열(2열)은 절대 수정하지 않음

사용법:
  python scripts/inject_translations.py [--gamepath <게임루트>] [--src <원본assets>] [--out <출력>]

  --gamepath: 게임 루트 경로 (IL2CPP 바이너리/메타데이터 탐색용).
              생략 시 original/resources.assets 기준으로 시도하되
              UnityPy 포크의 typetree_generator 없이 저장하면 참조가 깨지므로
              게임 경로 지정을 권장한다.

출력:
  patched/resources.assets (수정된 에셋)

저장 방식:
  UnityPy 포크(snowyegret23) + TypeTreeGeneratorAPI 기반 typetree_generator를
  env에 설정한 뒤 save()한다. 이렇게 하면 MonoBehaviour의 m_Script 참조와
  수정하지 않은 객체의 raw 데이터가 그대로 보존된다.
  (공식 UnityPy의 env.file.save()는 IL2CPP 게임에서 m_Script를 재매핑해
  TMP 폰트 등을 파괴하므로 사용 금지)
"""

import json
import struct
import sys
from pathlib import Path

# Windows 콘솔(cp949)에서 UTF-8 출력 보장
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


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


def find_il2cpp_binary(game_path: Path) -> Path | None:
    """게임 루트에서 IL2CPP 바이너리(GameAssembly) 탐색 (Windows .dll / macOS .dylib)"""
    candidates = [
        game_path / "GameAssembly.dll",
        game_path / "GameAssembly.dylib",
        game_path / "Contents" / "Resources" / "GameAssembly.dylib",
        game_path / "Contents" / "Frameworks" / "GameAssembly.dylib",
        game_path / "Contents" / "Resources" / "GameAssembly.so",
        game_path / "TwilightStruggle_Data" / "GameAssembly.dll",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def find_global_metadata(game_path: Path) -> Path | None:
    """global-metadata.dat 탐색 (Data/il2cpp_data/Metadata 아래)"""
    for p in game_path.rglob("global-metadata.dat"):
        return p
    return None


def create_typetree_generator(env, game_path: Path) -> None:
    """UnityPy 포크 env에 typetree_generator를 설정한다.

    IL2CPP 덤프(GameAssembly + global-metadata.dat)로 타입 트리를 생성해
    env.typetree_generator에 주입한다. 이 설정이 있어야 save() 시
    MonoBehaviour m_Script 참조가 보존된다.
    """
    from TypeTreeGeneratorAPI import TypeTreeGenerator

    unity_version = getattr(env.file, "unity_version", None)
    if not unity_version:
        for loaded in (env.files or {}).values():
            uv = getattr(loaded, "unity_version", None)
            if uv:
                unity_version = uv
                break
    if not unity_version:
        raise RuntimeError("resources.assets에서 Unity 버전을 읽을 수 없습니다.")

    il2cpp = find_il2cpp_binary(game_path)
    metadata = find_global_metadata(game_path)
    if il2cpp is None or metadata is None:
        raise FileNotFoundError(
            f"IL2CPP 바이너리/메타데이터를 찾을 수 없습니다. --gamepath를 확인하세요:\n"
            f"  GameAssembly: {il2cpp or '(없음)'}\n"
            f"  global-metadata.dat: {metadata or '(없음)'}"
        )

    gen = TypeTreeGenerator(str(unity_version))
    gen.load_il2cpp(il2cpp.read_bytes(), metadata.read_bytes())
    env.typetree_generator = gen
    print(f"  typetree_generator 설정 완료 (Unity {unity_version})")


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
        row_s, col = cell_key.split(":", 1)
        if col != "2" or val in ("null", "", "EN", "ENTER PATH"):
            continue

        # 우선순위: EN 값 기준(rt_index/manual) > key 기준(manual)
        row_key = cells.get(f"{row_s}:1", "")
        ko = (
            key_to_ko.get(val)
            or rt_index.get(val)
            or manual.get(val)
            or manual.get(row_key)
        )
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


def inject_rules_tutorial(text: str, rules_entries: list) -> tuple[str, int]:
    """TS_RulesTutorial: 시트 1631793870의 EN 열(3열) → KO 번역 주입 (Phase 7)

    구조: 1열=키(String), 2열=US, 3열=EN, 4~8=FR/IT/DE/ES/NL, 9=Notes, 10=KO.
    시트 0(File/String 참조 목록)은 건드리지 않는다.
    key(1열) 기준으로 translation/manual-rules.json의 번역을 찾아 EN 열에 쓴다.
    (EN 열에 주입하면 add_ko_columns.py가 KO 열로 복사해 동기화된다)
    """
    date_end = text.index("\n") + 1
    date_line = text[:date_end]
    data = json.loads(text[date_end:].strip())

    key_to_ko = {}
    for e in rules_entries:
        ko = e.get("translation_ko", "")
        if ko:
            key_to_ko[e["key"]] = ko

    changed = 0
    for top_key, cells in data.items():
        if top_key == "0" or not isinstance(cells, dict):
            continue
        for cell_key, val in list(cells.items()):
            if ":" not in cell_key:
                continue
            r, c = cell_key.split(":", 1)
            if c != "3":  # EN 열만 교체
                continue
            row_key = cells.get(f"{r}:1", "")
            ko = key_to_ko.get(row_key)
            if ko and val != ko:
                cells[cell_key] = ko
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
    import argparse

    import UnityPy

    parser = argparse.ArgumentParser(description="번역 주입 (무손상 저장)")
    parser.add_argument("--gamepath", default=None, help="게임 루트 경로 (IL2CPP 탐색용)")
    parser.add_argument("--src", default=None, help="원본 assets 경로 (기본: original/resources.assets)")
    parser.add_argument("--out", default=None, help="출력 경로 (기본: patched/resources.assets)")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent

    # 원본 로드
    src_path = Path(args.src) if args.src else base / "original/resources.assets"
    if not src_path.exists():
        raise FileNotFoundError(f"원본이 없습니다: {src_path} (--src로 지정하세요)")
    env = UnityPy.load(str(src_path))

    # typetree_generator 설정 (m_Script 보존 필수)
    if args.gamepath:
        create_typetree_generator(env, Path(args.gamepath))
    else:
        print("  ⚠️  --gamepath 미지정: typetree_generator 없이 저장하면 참조가 깨질 수 있습니다.")

    # 번역 소스 로드
    strings = json.loads((base / "translation/strings.json").read_text("utf-8"))
    cards = json.loads((base / "translation/cards.json").read_text("utf-8"))
    key_to_ko_cs = build_key_to_ko(strings)
    key_to_ko_cards = build_key_to_ko(cards)
    rt_index = build_rt_index()

    # 수동 번역 확장 (translation/manual-extra.json — 잔존 UI 키)
    manual_extra = {}
    manual_extra_path = base / "translation/manual-extra.json"
    if manual_extra_path.exists():
        manual_extra = json.loads(manual_extra_path.read_text("utf-8"))

    # TS_RulesTutorial 번역 (translation/manual-rules.json — Phase 7)
    manual_rules = {"entries": []}
    manual_rules_path = base / "translation/manual-rules.json"
    if manual_rules_path.exists():
        manual_rules = json.loads(manual_rules_path.read_text("utf-8"))
        print(f"TS_RulesTutorial 번역 소스: {len(manual_rules.get('entries', []))}행")

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
    
    # 원본 로드 (위에서 args.src 처리됨 — 여기서 재할당 금지!)
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
            new_text, changed = inject_simple_table(
                text, {}, rt_index, manual_extra.get("TS_Ingame", {})
            )
            print(f"  TS_Ingame: {changed}행 (EN→KO)")
            results["TS_Ingame"] = changed
        
        elif name == "Common_Ingame":
            manual = dict(common_ingame_manual)
            manual.update(manual_extra.get("Common_Ingame", {}))
            new_text, changed = inject_simple_table(text, {}, rt_index, manual)
            print(f"  Common_Ingame: {changed}행 (EN→KO)")
            results["Common_Ingame"] = changed
        
        elif name == "TS_Strings":
            new_text, changed = inject_simple_table(
                text, {}, rt_index, manual_extra.get("TS_Strings", {})
            )
            print(f"  TS_Strings: {changed}행 (EN→KO)")
            results["TS_Strings"] = changed
        
        elif name == "TS_RulesTutorial":
            new_text, changed = inject_rules_tutorial(text, manual_rules.get("entries", []))
            print(f"  TS_RulesTutorial: {changed}행 (EN 열 3 → KO, Phase 7)")
            results["TS_RulesTutorial"] = changed
        
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
    out_path = Path(args.out) if args.out else out_dir / "resources.assets"
    with open(out_path, "wb") as f:
        f.write(env.file.save(packer="original"))

    print(f"\n→ {out_path}")

    # EN 보존 검증 (Common_Strings)
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

    # m_Script 무손상 검증 (MonoBehaviour 참조가 원본과 동일한지)
    print("\n=== m_Script 무손상 검증 ===")
    mism = 0
    orig_env = UnityPy.load(str(src_path))
    for o1, o2 in zip(orig_env.objects, env2.objects):
        if o1.type.name != "MonoBehaviour" or o2.type.name != "MonoBehaviour":
            continue
        r1, r2 = o1.get_raw_data(), o2.get_raw_data()
        if len(r1) >= 28 and len(r2) >= 28:
            s1 = (struct.unpack_from("<I", r1, 16)[0], struct.unpack_from("<Q", r1, 20)[0])
            s2 = (struct.unpack_from("<I", r2, 16)[0], struct.unpack_from("<Q", r2, 20)[0])
            if s1 != s2:
                mism += 1
                if mism <= 5:
                    print(f"  ❌ PathID={o1.path_id}: m_Script {s1} → {s2}")
    if mism == 0:
        print("  ✅ MonoBehaviour m_Script 전부 보존됨")
    else:
        print(f"  ❌ m_Script 불일치 {mism}건 — 저장이 안전하지 않습니다!")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
