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

### 폰트 매핑 (2026-08-11 확정)

| 교체 폰트 | 대상 (24개) |
|---|---|
| **NotoSerifKR SDF** | TIMES, TIMESI, LiberationSans(+Fallback), FRAMD 계열, GOTHIC 계열, Unity (13개) |
| **BlackHanSans SDF** | Anton, Bangers, Electronic Highway Sign, Oswald, Roboto-Bold, Gunplay, IMPACT 계열, atwriter(+outline) (11개) |

---

## Step 3: 검증

```bash
# m_Script/raw 무손상 검증 (번역 주입본 vs 폰트 주입 결과)
python scripts/verify_assets.py --orig <번역주입본 resources.assets> --patched <font-output/resources.assets>
```

- 성공 기준: `m_Script 불일치 0건`, `예상외 raw 변경 0건`
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
