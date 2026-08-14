---
name: twilight-struggle-font-injection
description: Twilight Struggle 한글 패치 프로젝트에서 한글 SDF 폰트를 게임 에셋에 주입하는 전체 절차 (Unity_Font_Replacer v1.2.8). 가상 작업 폴더 구성 → --parse → 매핑 재설정 → --list 주입 → verify_assets 검증 → patched/<플랫폼>/ 반영 → 설치까지. Windows(exe)와 macOS(소스 실행) 모두 지원. 폰트 주입/재주입 요청 시 사용. (폰트 자체 교체는 twilight-struggle-font-swap, 크기 조절은 twilight-struggle-font-size 참조)
---

# Twilight Struggle 한글 패치 — SDF 폰트 주입 절차

## 배경

- 게임의 24개 TMP 폰트에 한글 SDF 2종이 매핑돼 있음
  - 본문: `NotoSerifKR SDF` (= D2Coding Regular, 16개: TIMES/FRAMD/GOTHIC/LiberationSans/Unity + IMPACT 3종)
  - 제목: `BlackHanSans-Regular SDF` (= Paperlogy 5 Medium, 8개: Anton/Bangers/Oswald/Roboto/Gunplay/atwriter)
  - Sprite 3개(Default Sprite Asset·DropCap Numbers·EmojiOne)는 교체 제외 (빈 값)
- ⚠️ **2026-08-13 실측**: IMPACT 3종은 트랙 첫 칸 H 넘침 문제로 제목(Paperlogy)이 아닌 **본문(D2Coding 모노스페이스)**으로 매핑
- 원본 문서: `docs/runbooks/phase-3-windows-font-injection.md` (최초 검증 기록)

## 사전 준비

- **Windows 빌드 `GameAssembly.dll` + `global-metadata.dat`** 필요 (Il2CppDumper가 읽음)
  - Windows: Steam 설치본에서 직접
  - macOS: `original/GameAssembly.dll`·`original/global-metadata.dat` 보관본 사용 (PE dll + Windows metadata 조합만 동작 — macOS metadata로는 실패)
- venv python: `.venv/Scripts/python.exe` (Windows) / `.venv/bin/python` (macOS)
- 주입 대상: **번역+KO 열 주입 완료본** (inject_translations.py --platform 실행 결과 — m_Script 무손상 필수)
- KR_ASSETS: `tools/unity-font-replacer/KR_ASSETS/` (Windows exe) 또는 `tools/unity-font-replacer/src/KR_ASSETS/` (macOS 소스 실행 — script_dir 기준)

## 절차

### 1. 가상 작업 폴더 구성 (Steam 폴더 직접 수정 금지)

```
tools/font-inject-work/Twilight Struggle/          # macOS는 font-inject-work-mac/
├── GameAssembly.dll                               # Windows 빌드 (PE)
└── TwilightStruggle_Data/
    ├── resources.assets                           # ★ 번역+KO 주입 완료본 (patched/<플랫폼>/) 복사
    ├── sharedassets*.assets (+ .resS)             # Steam 설치본에서 복사
    ├── globalgamemanagers.assets (+ .resS)        # Steam 설치본에서 복사
    └── il2cpp_data/Metadata/global-metadata.dat   # Windows 빌드 metadata
    # ⚠️ Managed 폴더는 복사하지 않는다 (있으면 Mono로 오판 → SDF 0개)
```

```bash
# Windows 예시
GAME="/d/Games/steamapps/common/Twilight Struggle"
WORK="tools/font-inject-work"
rm -rf "$WORK" && mkdir -p "$WORK/Twilight Struggle/TwilightStruggle_Data/il2cpp_data/Metadata"
cp "$GAME/GameAssembly.dll" "$WORK/Twilight Struggle/"
cp patched/windows/resources.assets "$WORK/Twilight Struggle/TwilightStruggle_Data/"
cp "$GAME/TwilightStruggle_Data/"{globalgamemanagers.assets,globalgamemanagers.assets.resS,sharedassets0.assets,sharedassets0.assets.resS,sharedassets1.assets,sharedassets2.assets,sharedassets3.assets} \
   "$WORK/Twilight Struggle/TwilightStruggle_Data/"
cp "$GAME/TwilightStruggle_Data/il2cpp_data/Metadata/global-metadata.dat" \
   "$WORK/Twilight Struggle/TwilightStruggle_Data/il2cpp_data/Metadata/"
```

### 2. 폰트 파싱 (stdin 리다이렉트 필수 — 없으면 EOFError)

```bash
cd tools/unity-font-replacer
echo "" | ./unity_font_replacer_ko.exe \
  --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" --parse
# macOS 소스 실행: .venv/bin/python tools/unity-font-replacer/src/unity_font_replacer_ko.py --gamepath "tools/font-inject-work-mac/Twilight Struggle" --parse
```

- 성공 기준: `SDF 폰트: 27개` (TTF 20 + SDF 27). SDF 0개면 venv 패치 누락 (아래 macOS 유의점)
- parse가 `Twilight Struggle.json`을 초기화 → **매핑은 다음 단계에서 반드시 재설정**

### 3. 매핑 재설정

```bash
.venv/Scripts/python.exe scripts/apply_font_mapping.py
# → Replace_to 설정: 24개 (NotoSerifKR 16 + BlackHanSans 8)
# JSON 경로: tools/unity-font-replacer/Twilight Struggle.json (macOS 소스: src/Twilight Struggle.json)
```

### 4. 주입 (출력 폴더는 새로 지정 — 기존 산출물 덮어쓰지 말 것)

```bash
echo "" | ./unity_font_replacer_ko.exe \
  --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" \
  --list "Twilight Struggle.json" \
  --output-only "C:/.../tools/font-inject-work/font-output-<날짜>"
# macOS: --gamepath "tools/font-inject-work-mac/Twilight Struggle" --list "tools/unity-font-replacer/src/Twilight Struggle.json" --output-only "tools/font-inject-work-mac/font-output"
```

- 출력: `font-output/resources.assets`, `font-output/sharedassets0.assets`
- `resources.assets` 크기: 원본 108.3MB → 주입 후 ~108.8MB (2048² 아틀라스 기준)

### 5. 검증 (verify는 "주입 전 vs 주입 후" 비교)

```bash
.venv/Scripts/python.exe scripts/verify_assets.py \
  --orig <번역+KO 주입본(주입 전)> --patched <font-output/resources.assets>
```

- 성공 기준: `m_Script 불일치 0건`, `TextAsset 0건`(번역/KO 열 유지), 폰트/텍스처 변경만 (69건 예)
- 크기 조절 주입 시 폰트 변경이 0건이면 m_PointSize 미반영 (20여 건 잡혀야 정상)

### 6. patched/<플랫폼>/ 반영 + 해시 갱신

```bash
cp font-output/resources.assets font-output/sharedassets0.assets patched/<windows|macos>/
# ⚠️ hashes.txt는 폴더 내부 기준 상대경로로 생성 (자기 자신 포함 금지)
cd patched/<플랫폼> && sha256sum level1 level2 level3 resources.assets sharedassets0.assets > hashes.txt && cd -
# 검증: cd patched/<플랫폼> && sha256sum -c hashes.txt
```

⚠️ 플랫폼별 분리 (2026-08-14): `patched/windows/`와 `patched/macos/`는 별도 폴더.
level1~3은 플랫폼 원본 기준으로 patch_scenes.py 재실행해야 함 (교차 복사 시 크래시).

### 7. 설치

```bash
# Windows: powershell -ExecutionPolicy Bypass -File scripts/install-windows.ps1  (patched/windows 읽음)
# macOS:   ./scripts/install.sh  (patched/macos 읽음 — 코드사인 자동, 언어 설정 무조작)
```

## macOS 소스 실행 시 유의점 (venv 패치 2건 필수)

> 최초 1회만 적용 (로컬 수정 — 재설치 시 재적용). Windows exe는 불필요.

1. **UnityPy `get_nodes_up`의 `.dll` 붙임 제거**: `UnityPy/helpers/TypeTreeGenerator.py`에서 아래 2줄 삭제
   ```python
   if not assembly.endswith(".dll"):
       assembly = f"{assembly}.dll"
   ```
   (안 지우면 모든 타입 검색 실패 → SDF 0개)
2. **Il2CppDumper 분기 스킵** (`unity_font_replacer_core.py` ~8281행):
   `if not os.path.exists(dumper_path):` → `if sys.platform != "win32" or not os.path.exists(dumper_path):`
   (비Windows는 무조건 스킵 — exe 없이 소스 실행)

- `--parse`에서 "SDF 0개 / TTF 20개" → venv 패치(1번) 누락
- `--list`에서 "Il2CppDumper 실행 중 예외" → venv 패치(2번) 누락

## 문제 해결

| 증상 | 원인 | 대응 |
|---|---|---|
| `unity_font_replacer_ko.exe` 실행 안 됨 | .NET Runtime 없음 | .NET 8.0 Runtime 설치 |
| SDF 0개 (TTF만 인식) | `Managed` 폴더로 Mono 오판 | 가상 폴더에서 Managed 제거 후 재parse |
| parse 결과 1개뿐 (atwriter SDF) | 입력 assets가 UnityPy 손상본 (m_Script 변조) | 무손상 번역 주입본을 입력으로 사용 |
| `resources.assets` 용량 급증 (397MB) | 4096² 아틀라스 × 24개 | 2048²로 SDF 재생성 (`--atlas-size 2048,2048`) |
| 한글 `□` 표시 | SDF 아틀라스에 글리프 없음 | `fonts/chars.txt`에 글자 추가 → SDF 재생성 → 재주입 |
| `classdata.tpk` 오류 | TPK 자동 다운로드 실패 | 인터넷 연결 확인 |

## 주의사항

- ⚠️ **m_Script 무손상**: 공식 UnityPy `env.file.save()`는 m_Script를 재매핑해 폰트를 파괴 — 반드시 포크 UnityPy + typetree_generator 방식 유지
- ⚠️ **face info 차이**: 폰트마다 lineHeight/ascent가 달라 표시 크기·줄 간격 변동 — 기존 계열 폰트 유지 권장. 보정이 필요하면 `twilight-struggle-font-size` 스킬 (m_PointSize 조절)
- ⚠️ **문자셋**: 교체 후 `□` 발견 시 `extract_charset.py`로 표시 문자열 전체 재추출 → chars.txt 갱신 → SDF 재생성 → 재주입
- ⚠️ Steam 무결성/업데이트로 원복 시 `twilight-struggle-update` 스킬 참조
- 관련: `twilight-struggle-font-swap` (폰트 교체) / `twilight-struggle-font-size` (크기 조절) / `docs/runbooks/phase-3-windows-font-injection.md`
