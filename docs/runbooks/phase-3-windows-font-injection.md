# Phase 3 Runbook — Windows에서 Unity_Font_Replacer로 SDF 폰트 주입

> **상태**: ✅ 실행 완료 (2026-08-11). 아래는 실제 검증된 절차다.

## 사전 준비물

- **Windows PC** + **Windows용 Twilight Struggle 설치** (Steam)
  - `GameAssembly.dll` + `il2cpp_data/Metadata/global-metadata.dat` 필요 (Il2CppDumper가 읽음)
- macOS 프로젝트 폴더의 SDF 파일:
  - `fonts/NotoSerifKR SDF.json` + `NotoSerifKR SDF Atlas.png` + `NotoSerifKR SDF Material.json`
  - `fonts/BlackHanSans-Regular SDF.json` + `BlackHanSans-Regular SDF Atlas.png` + `BlackHanSans-Regular SDF Material.json`
  - `fonts/chars.txt`
- 도구: [Unity_Font_Replacer](https://github.com/snowyegret23/Unity_Font_Replacer) v1.2.8 릴리즈 ZIP
  - `Unity_Font_Replacer_v1.2.8.zip` (unity_font_replacer_ko.exe 포함, ~149MB)
  - `.NET 8.0 Runtime` 필요 (Il2CppDumper용)

### 파일 플랫폼 호환성

| 파일 | 플랫폼 호환 | 설명 |
|---|---|---|
| `resources.assets` | ✅ **공용** | Unity 에셋은 플랫폼 무관 동일 바이너리 |
| `sharedassets*.assets` | ✅ **공용** | 마찬가지로 플랫폼 무관 |
| `global-metadata.dat` | ✅ **공용** | IL2CPP 메타데이터, 플랫폼 무관 |
| `GameAssembly.dll` | ❌ **Windows 전용** | IL2CPP 바이너리. **Windows Steam 설치본 필요** |

> **핵심**: `resources.assets`는 그대로 써도 된다. 하지만 도구가 Il2CppDumper를 실행할 때
> `GameAssembly.dll`(Windows 바이너리)을 읽어야 하므로 Windows Steam에 게임이 설치되어 있어야 한다.

---

## ⚠️ 사전 지식 (중요)

1. **`Managed` 폴더 존재 시 Mono로 오판**: 도구의 `get_compile_method()`는 `_Data/Managed` 폴더
   존재 여부로 Mono/Il2cpp를 판별한다. 이 게임은 IL2CPP지만 `Managed` 폴더가 있어 Mono로 오판되어
   **SDF 폰트를 하나도 못 찾는다** (TTF 20개만 인식). → 가상 작업 폴더에서 `Managed`를 제거해야 한다.
2. **`oneshot` 서브커맨드는 없다**: v1.2.8 CLI는 `--parse` → JSON 수정 → `--list` 순서로 동작.
3. **공식 UnityPy로 저장한 assets는 m_Script가 파괴**되어 폰트 인식이 안 될 수 있다.
   반드시 [Phase 4 문서](../phases/phase-4-injection-layout.md)의 무손상 번역 주입본을 입력으로 쓸 것.
4. **Steam 폴더를 직접 수정하지 않는다** (불변 원칙). 가상 작업 폴더 + `--output-only` 사용.

---

## Step 1: 파일 준비

### 1-1. SDF 파일 배치

```
tools/unity-font-replacer/KR_ASSETS/
├── NotoSerifKR SDF.json
├── NotoSerifKR SDF Atlas.png
├── NotoSerifKR SDF Material.json
├── BlackHanSans-Regular SDF.json
├── BlackHanSans-Regular SDF Atlas.png
├── BlackHanSans-Regular SDF Material.json
└── (도구 기본 폰트: Mulmaru, NanumGothic)
```

### 1-2. 가상 게임 폴더 구성 (Steam 폴더 직접 수정 금지)

```
tools/font-inject-work/Twilight Struggle/
├── GameAssembly.dll                          ← Steam 설치본에서 복사
└── TwilightStruggle_Data/
    ├── resources.assets                      ← ★ 번역 주입 완료본(patched)을 복사
    ├── sharedassets*.assets (+ .resS)        ← Steam 설치본에서 복사
    ├── globalgamemanagers.assets (+ .resS)
    ├── il2cpp_data/Metadata/global-metadata.dat
    └── ⚠️ Managed 폴더는 복사하지 않는다 (Mono 오판 방지)
```

### 1-3. Steam 게임 경로 확인

기본값: `C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle\`
다른 위치일 수 있으니 Steam 라이브러리에서 확인 (예: `D:\Games\steamapps\common\Twilight Struggle\`)

---

## Step 2: 폰트 주입

```bat
cd tools\unity-font-replacer

:: 1) 폰트 목록 파싱 (가상 폴더 기준)
unity_font_replacer_ko.exe --gamepath "…\font-inject-work\Twilight Struggle" --parse

:: 2) "Twilight Struggle.json"에서 SDF 항목의 Replace_to 지정
::    - "NotoSerifKR SDF.json"  (본문/세리프 계열)
::    - "BlackHanSans-Regular SDF.json" (제목/디스플레이 계열)
::    - Sprite Asset(Default Sprite Asset, DropCap Numbers, EmojiOne)은 빈 값으로 제외

:: 3) 교체 실행 (원본 유지 + 수정 파일만 출력)
unity_font_replacer_ko.exe --gamepath "…\font-inject-work\Twilight Struggle" ^
    --list "Twilight Struggle.json" ^
    --output-only "…\font-inject-work\font-output"
```

- `--output-only`로 Steam 폴더가 아닌 별도 폴더에 결과물을 받는다.
- `--list`는 `Replace_to`가 빈 항목은 건너뛴다.
- 출력: `font-output/resources.assets`, `font-output/sharedassets0.assets` 등

### 폰트 매핑 (2026-08-12 갱신)

| 교체 폰트 | 대상 (24개) |
|---|---|
| **NotoSerifKR SDF** → D2Coding Regular | TIMES, TIMESI, LiberationSans(+Fallback), FRAMD 계열, GOTHIC 계열, Unity (13개) |
| **BlackHanSans SDF** → Paperlogy 5 Medium | Anton, Bangers, Electronic Highway Sign, Oswald, Roboto-Bold, Gunplay, IMPACT 계열, atwriter(+outline) (11개) |

> 파일명(KR_ASSETS의 `NotoSerifKR SDF` / `BlackHanSans-Regular SDF`)은 유지한 채
> SDF JSON 내용만 교체한다. 매핑 JSON 재설정 불필요.

---

## Step 2.5: 폰트 크기 조절 (SDF 재생성 불필요)

> 상세 절차: `.pi/skills/twilight-struggle-font-size/SKILL.md`

- **m_Scale은 도구가 게임 원본 값으로 강제 덮어씀** (`_NEW_LINE_METRIC_KEYS`) — JSON 수정 무의미
- **m_PointSize는 보존됨** — TMP `fontScale = fontSize / pointSize × scale` 공식에 따라
  pointSize를 키우면 글자가 작아진다 (반비례)
- 수식: 새 PointSize = 현재 PointSize ÷ (1 − 축소율). 도구가 int 정수화 → 70→77 ≈ 9% 축소
- line metrics가 pointSize 비율로 자동 보정되어 **글자만 축소, 줄 간격은 유지**
- 적용: `fonts/*.json` m_PointSize 수정 → KR_ASSETS 복사 → parse → apply_font_mapping → 주입 → 검증

---

## Step 3: 검증

```bash
# m_Script/raw 무손상 검증 (번역 주입본 vs 폰트 주입 결과)
python scripts/verify_assets.py --orig <번역주입본 resources.assets> --patched <font-output/resources.assets>
```

- 성공 기준: `m_Script 불일치 0건`, `예상외 raw 변경 0건`
- 크기 조절 주입 시 폰트/텍스처 변경이 **0건이면 m_PointSize가 반영되지 않은 것** (20여 건 잡혀야 정상)
- `font-output/resources.assets` → `patched/`, `font-output/sharedassets0.assets` → `patched/` 복사
- `sha256sum patched/*.assets > patched/hashes.txt`

---

## Step 4: macOS로 전송 및 적용

```
patched/resources.assets      (108MB, 번역+폰트 주입 완료)
patched/sharedassets0.assets  (4.6MB)
fonts/                        (2048² SDF — 재생성 시 필요)
```

macOS에서:

```bash
./scripts/install.sh   # 백업 → 복사 → codesign 자동 처리
```

Steam 실행 → 게임 언어 설정에서 한국어 선택 → 한글 확인.

---

## 문제 해결

| 증상 | 원인 가능성 | 대응 |
|---|---|---|
| `unity_font_replacer_ko.exe` 실행 안 됨 | .NET Runtime 없음 | [.NET 8.0 Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) 설치 |
| SDF 폰트 0개 (TTF만 인식) | `Managed` 폴더로 Mono 오판 | 가상 폴더에서 `Managed` 제거 후 재parse |
| parse 결과가 1개뿐 (atwriter SDF) | 입력 assets가 UnityPy로 손상된 파일 (m_Script 변조) | 무손상 번역 주입본을 입력으로 사용 |
| `resources.assets` 용량 급증 (397MB) | 4096² 아틀라스 × 24개 | `make_sdf.py --atlas-size 2048,2048 --point-size auto`로 재생성 (→103MB) |
| `classdata.tpk` 오류 | TPK 자동 다운로드 실패 | 인터넷 연결 확인 |
| 한글 `□` 여전히 표시 | SDF 아틀라스에 글리프 없음 | `chars.txt`에 누락 글자 추가 후 SDF 재생성 → 재주입 |

---

## 소스 기반 디버깅 (선택)

exe가 아닌 소스로 실행/디버깅하려면 GitHub 소스 + 의존성 설치:

```bash
pip install TypeTreeGeneratorAPI Pillow numpy scipy
pip install --upgrade "git+https://github.com/snowyegret23/UnityPy.git"
```

- `unity_font_replacer_core.py`의 `scan_fonts(game_path, lang='en', isolate_files=False)`로 스캔 재현
- `_create_generator()` → `TypeTreeGeneratorAPI.TypeTreeGenerator` — `get_nodes()`로 클래스별 타입 트리 생성 확인

---

## Step 5: macOS에서 전체 파이프라인 직접 실행 (2026-08-12 검증)

> Windows 전송 없이 macOS에서 번역 주입 → KO 열 → 폰트 주입 → 설치까지 전부 가능.
> 필요한 것은 Windows 빌드의 `GameAssembly.dll`(PE) + `global-metadata.dat` 2개뿐 (original/에 보관).

### ⚠️ global-metadata.dat는 플랫폼별이다 (Runbook 초기 기록 정정)

- macOS metadata(`3665f553…`) ≠ Windows metadata(`e18d1b04…`) — 해시 다름 (2026-08-12 실측)
- **Windows dll + Windows metadata 조합이어야 타입 트리 생성 성공**
  (macOS metadata로는 `Type "TMP_FontAsset" was not found in the IL2CPP metadata` 발생)
- macOS dylib(슬라이스) + macOS metadata 조합도 실패 → **PE dll + Windows metadata만 사용**

### 사전 준비 (original/에 보관)

```
original/GameAssembly.dll      # Windows Steam 설치본 (PE32+, ~34MB)
original/global-metadata.dat   # Windows Steam 설치본 (TwilightStruggle_Data/il2cpp_data/Metadata/, ~7.9MB)
```

### venv 패치 (필수 2건 — 로컬 수정, 재설치 시 재적용)

1. **UnityPy `get_nodes_up`의 `.dll` 붙임 제거** (공식 UnityPy 1.25.2 기준):
   `UnityPy/helpers/TypeTreeGenerator.py`에서 아래 2줄 삭제
   ```python
   if not assembly.endswith(".dll"):
       assembly = f"{assembly}.dll"
   ```
   (C++ 라이브러리가 `.dll` 없는 이름만 인식 — 안 지우면 모든 타입 검색 실패 → SDF 0개)

2. **Il2CppDumper 분기 스킵** (`unity_font_replacer_core.py` ~8281행):
   `if not os.path.exists(dumper_path):` → `if sys.platform != "win32" or not os.path.exists(dumper_path):`
   (소스 실행 시 get_script_dir()=src/에 Il2CppDumper.exe가 있어도 macOS에서 실행 불가 — 비Windows는 무조건 스킵)

### 가상 작업 폴더 구성

```
tools/font-inject-work-mac/Twilight Struggle/
├── GameAssembly.dll                          ← original/GameAssembly.dll (PE!)
└── TwilightStruggle_Data/
    ├── resources.assets                      ← 번역+KO 주입본 (patched)
    ├── sharedassets0~3.assets (+ .resS)
    ├── globalgamemanagers (+ .assets, .resS)
    └── il2cpp_data/Metadata/global-metadata.dat  ← original/global-metadata.dat (Windows!)
```

### 실행 순서

```bash
# 1) 번역 주입 (macOS: --gamepath는 GameAssembly.dll 있는 임시 폴더 + metadata 복사본)
cp original/GameAssembly.dll /tmp/ts-ga/ && cp original/global-metadata.dat /tmp/ts-ga/
.venv/bin/python scripts/inject_translations.py --gamepath /tmp/ts-ga \
    --src original/resources.assets --out patched/resources.assets
.venv/bin/python scripts/add_ko_columns.py --gamepath /tmp/ts-ga \
    --src patched/resources.assets --out patched/resources.assets.ko && mv patched/resources.assets.ko patched/resources.assets

# 2) SDF 재생성 (2048², m_PointSize 77 유지 — 4096²면 결과가 397MB가 됨)
cd fonts
.venv/bin/python ../tools/unity-font-replacer/src/make_sdf.py --ttf "D2Coding-Ver1.3.3-20260725.ttf" \
    --atlas-size 2048,2048 --point-size 77 --padding 4 --charset chars.txt
.venv/bin/python ../tools/unity-font-replacer/src/make_sdf.py --ttf "Paperlogy-5Medium.ttf" \
    --atlas-size 2048,2048 --point-size 77 --padding 4 --charset chars.txt
# ※ make_sdf가 73으로 자동 보정 → JSON m_FaceInfo.m_PointSize를 77로 재수정 후 주입

# 3) KR_ASSETS 배치 (script_dir=src/KR_ASSETS 기준! 루트 KR_ASSETS에도 동일 복사)
cp "fonts/D2Coding-Ver1.3.3-20260725 SDF.json"        src/KR_ASSETS/NotoSerifKR SDF.json
cp "fonts/D2Coding-Ver1.3.3-20260725 SDF Atlas.png"   src/KR_ASSETS/NotoSerifKR SDF Atlas.png
cp "fonts/Paperlogy-5Medium SDF.json"                 src/KR_ASSETS/BlackHanSans-Regular SDF.json
cp "fonts/Paperlogy-5Medium SDF Atlas.png"            src/KR_ASSETS/BlackHanSans-Regular SDF Atlas.png

# 4) 폰트 주입 (SDF 27개 인식 확인 후)
.venv/bin/python tools/unity-font-replacer/src/unity_font_replacer_ko.py \
    --gamepath "tools/font-inject-work-mac/Twilight Struggle" --parse
# → "Twilight Struggle.json"의 SDF 항목에 Replace_to 지정
#   (본문 13개: NotoSerifKR SDF / 제목 11개: BlackHanSans-Regular SDF / Sprite 3개: 빈 값)
.venv/bin/python tools/unity-font-replacer/src/unity_font_replacer_ko.py \
    --gamepath "tools/font-inject-work-mac/Twilight Struggle" \
    --list "tools/unity-font-replacer/src/Twilight Struggle.json" \
    --output-only "tools/font-inject-work-mac/font-output"

# 5) 검증 + 설치 (verify는 "입력(번역+KO 주입본) vs 출력(폰트 주입본)" 비교!)
.venv/bin/python scripts/verify_assets.py \
    --orig "tools/font-inject-work-mac/Twilight Struggle/TwilightStruggle_Data/resources.assets" \
    --patched tools/font-inject-work-mac/font-output/resources.assets
cp tools/font-inject-work-mac/font-output/resources.assets tools/font-inject-work-mac/font-output/sharedassets0.assets patched/
./scripts/install.sh   # 백업 → 복사(resources/sharedassets0/level1~3) → 재서명 → 언어 KO
```

### macOS 실행 시 유의점

- `--parse`에서 "SDF 0개 / TTF 20개"면 venv 패치(1번) 누락 — 타입 트리 생성 실패
- `--list`에서 "Il2CppDumper 실행 중 예외"면 venv 패치(2번) 누락
- `resources.assets` 397MB면 SDF Atlas가 4096² — 2048²로 재생성 필요
- font-output의 `globalgamemanagers` 등 다른 파일은 복사 불필요 (resources/sharedassets0/level1~3만 patched/)
- install.sh는 level1~3도 복사한다 (2026-08-12 버그 수정: 원래 level1~3 누락)
