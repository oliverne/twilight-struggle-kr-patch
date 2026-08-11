#!/usr/bin/env python3
"""모든 언어 테이블에 KO 열 추가 — 언어=KO에서 ${Key} 노출 문제 해결 (2026-08-12)

원인:
  게임 언어가 KO일 때 SmartLocalization은 각 TextAsset 테이블의 'KO' 헤더
  열을 찾아 값을 해석한다. Common_Strings만 KO 열(10열)이 있어 메뉴가
  한글화됐고, TS_Cards·TS_Ingame·TS_Strings·Common_Ingame·
  TS_RulesTutorial에는 KO 열이 없어 ${Card_*}/${Panel_*} 키가 그대로
  화면에 노출됐다 (카드 전체 키 표시, Scoring UI 키 표시).

해결:
  각 시트 헤더의 빈 열에 'KO' 라벨을 추가하고, EN 열(이미 한글 주입됨)
  값을 KO 열에 복사한다. 언어가 EN이든 KO든 한글이 표시된다.
  - EN 열 위치: 헤더 행(1행)에서 'EN' 라벨로 탐색
  - KO 열 위치: **헤더 행에 이미 존재하는 열 중 값이 null인 최소 번호**
    (⚠️ 2026-08-12 3차 테스트: 원본에 없던 열 번호(27열 등)에 셀을 추가하면
    게임 파서가 무시함 — 원본이 26열까지 셀을 보유하므로 8/9/10열에 배치)
  - Common_Strings: 이미 KO 열 있음 → 스킵 (검증만)
  - 시트 0(스프레드시트 설명)은 언어 열이 없어 스킵

기존에 잘못 추가된 KO 열(원본 범위 밖)이 있으면 제거 후 재배치한다.

사용법:
  python scripts/add_ko_columns.py --gamepath <게임루트> --src <assets> --out <출력>

저장: UnityPy 포크 + typetree_generator (m_Script 보존 — inject_translations.py와 동일)
"""
import json
import struct
import sys
from pathlib import Path

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
    return name, raw[off + 4 : off + 4 + script_len]


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


def add_ko_column(text: str) -> tuple[str, dict]:
    """시트별 EN 열 값 → KO 열 복사. (변경된 시트 통계 반환)

    KO 열 위치: 헤더 행에 이미 존재하는 열 중 값이 null/''인 최소 번호.
    기존에 잘못 배치된 KO 열(원본 범위 밖)은 제거 후 재배치.
    """
    date_end = text.index("\n") + 1
    date_line = text[:date_end]
    data = json.loads(text[date_end:].strip())
    stats = {}

    for top_key, cells in data.items():
        if not isinstance(cells, dict):
            continue

        # 헤더 행(1행)에서 EN 열 위치와 사용 중 열 파악
        header_cols = {}
        row_ids = set()
        for cell_key, val in cells.items():
            if ":" not in cell_key:
                continue
            r, c = cell_key.split(":", 1)
            if r == "1":
                header_cols[int(c)] = val
            else:
                row_ids.add(int(r))

        en_col = next((c for c, v in sorted(header_cols.items()) if v == "EN"), None)
        if en_col is None:
            continue  # 언어 열 없는 시트 (설명 시트 등)

        # 기존 KO 열 제거 (잘못된 위치 포함) 후 null로 복원
        old_ko = next((c for c, v in header_cols.items() if v == "KO"), None)
        if old_ko is not None:
            for cell_key in [k for k in cells if k.endswith(f":{old_ko}")]:
                cells[cell_key] = "null"
            stats[top_key] = {"removed_old_ko": old_ko}

        # KO 열 위치: 헤더 행에 이미 존재하는 열 중 값이 null/''인 최소 번호
        # (⚠️ 원본에 없는 열 번호를 추가하면 게임 파서가 무시함)
        # (⚠️ 1열은 키 열이므로 제외)
        ko_col = next(
            (c for c, v in sorted(header_cols.items()) if c != 1 and v in ("null", "", None)),
            None,
        )
        if ko_col is None:
            stats[top_key]["skipped"] = "no free column" if top_key in stats else ""
            if top_key not in stats:
                stats[top_key] = {"skipped": "no free column"}
            continue

        cells[f"1:{ko_col}"] = "KO"
        added = 0
        for r in sorted(row_ids):
            en_val = cells.get(f"{r}:{en_col}", "null")
            if en_val not in ("null", ""):
                cells[f"{r}:{ko_col}"] = en_val
                added += 1
        st = stats.setdefault(top_key, {})
        st.update({"en_col": en_col, "ko_col": ko_col, "rows": added})

    return date_line + json.dumps(data, ensure_ascii=False, separators=(",", ":")), stats


def find_il2cpp_binary(game_path: Path):
    for c in [
        game_path / "GameAssembly.dll",
        game_path / "GameAssembly.dylib",
        game_path / "TwilightStruggle_Data" / "GameAssembly.dll",
    ]:
        if c.exists():
            return c
    return None


def find_global_metadata(game_path: Path):
    for p in game_path.rglob("global-metadata.dat"):
        return p
    return None


def main():
    import argparse

    import UnityPy

    parser = argparse.ArgumentParser(description="언어 테이블 KO 열 추가")
    parser.add_argument("--gamepath", required=True, help="게임 루트 (IL2CPP 탐색용)")
    parser.add_argument("--src", required=True, help="입력 assets")
    parser.add_argument("--out", required=True, help="출력 assets")
    args = parser.parse_args()

    from TypeTreeGeneratorAPI import TypeTreeGenerator

    env = UnityPy.load(args.src)
    unity_version = getattr(env.file, "unity_version", None)
    il2cpp = find_il2cpp_binary(Path(args.gamepath))
    metadata = find_global_metadata(Path(args.gamepath))
    if not (unity_version and il2cpp and metadata):
        raise SystemExit("Unity 버전/IL2CPP를 찾을 수 없습니다.")
    gen = TypeTreeGenerator(str(unity_version))
    gen.load_il2cpp(il2cpp.read_bytes(), metadata.read_bytes())
    env.typetree_generator = gen
    print(f"  typetree_generator 설정 완료 (Unity {unity_version})")

    changed_assets = []
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw_textasset(obj.get_raw_data())
        if name not in (
            "TS_Cards", "TS_Ingame", "TS_Strings", "Common_Ingame", "TS_RulesTutorial",
        ):
            continue
        text = script.decode("utf-8")
        new_text, stats = add_ko_column(text)
        if stats:
            obj.set_raw_data(encode_textasset(name, new_text.encode("utf-8")))
            changed_assets.append((name, stats))
            print(f"  {name}: {stats}")

    if not changed_assets:
        print("변경된 테이블 없음 — 중단")
        return 1

    with open(args.out, "wb") as f:
        f.write(env.file.save(packer="original"))
    print(f"\n→ {args.out}")

    # 검증: KO 열 존재 + 값 확인
    print("\n=== 검증 ===")
    env2 = UnityPy.load(args.out)
    for obj in env2.objects:
        if obj.type.name != "TextAsset":
            continue
        name, script = parse_raw_textasset(obj.get_raw_data())
        if name not in ("TS_Cards", "TS_Ingame", "TS_Strings", "Common_Ingame", "TS_RulesTutorial"):
            continue
        text = script.decode("utf-8")
        date_end = text.index("\n") + 1
        data = json.loads(text[date_end:].strip())
        for top_key, cells in data.items():
            if top_key == "0" or not isinstance(cells, dict):
                continue
            header = {int(c.split(":")[1]): v for c, v in cells.items() if c.startswith("1:")}
            if "KO" in header.values():
                ko_col = next(c for c, v in header.items() if v == "KO")
                en_col = next((c for c, v in header.items() if v == "EN"), None)
                ko_rows = [c for c in cells if c.endswith(f":{ko_col}") and not c.startswith("1:")]
                print(f"  ✅ {name}/시트{top_key}: KO 열={ko_col} (EN={en_col}), {len(ko_rows)}행")
            else:
                print(f"  ❌ {name}/시트{top_key}: KO 열 없음!")

    # m_Script 무손상 검증
    print("\n=== m_Script 무손상 검증 ===")
    orig_env = UnityPy.load(args.src)
    mism = 0
    for o1, o2 in zip(orig_env.objects, env2.objects):
        if o1.type.name != "MonoBehaviour" or o2.type.name != "MonoBehaviour":
            continue
        r1, r2 = o1.get_raw_data(), o2.get_raw_data()
        if len(r1) >= 28 and len(r2) >= 28:
            s1 = (struct.unpack_from("<I", r1, 16)[0], struct.unpack_from("<Q", r1, 20)[0])
            s2 = (struct.unpack_from("<I", r2, 16)[0], struct.unpack_from("<Q", r2, 20)[0])
            if s1 != s2:
                mism += 1
    if mism == 0:
        print("  ✅ MonoBehaviour m_Script 전부 보존됨")
    else:
        print(f"  ❌ m_Script 불일치 {mism}건!")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
