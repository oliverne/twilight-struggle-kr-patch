# Phase 3 Runbook — Windows에서 Unity_Font_Replacer로 SDF 폰트 주입

> **상태**: macOS에서 `make_sdf.py`로 SDF 생성 완료, Windows에서 `Unity_Font_Replacer_KO.exe`로 주입

## 사전 준비물

- **Windows PC** (또는 Parallels/VM) + **Windows용 Twilight Struggle 설치** (Steam)
- macOS 프로젝트 폴더의 생성 완료된 SDF 파일:
  - `fonts/NotoSerifKR SDF.json` + `NotoSerifKR SDF Atlas.png` + `NotoSerifKR SDF Material.json`
  - `fonts/BlackHanSans-Regular SDF.json` + `BlackHanSans-Regular SDF Atlas.png` + `BlackHanSans-Regular SDF Material.json`
  - `fonts/chars.txt`

### 파일 플랫폼 호환성

| 파일 | 플랫폼 호환 | 설명 |
|---|---|---|
| `resources.assets` | ✅ **공용** | Unity 에셋은 플랫폼 무관 동일 바이너리. macOS→Windows 복사 가능 |
| `sharedassets*.assets` | ✅ **공용** | 마찬가지로 플랫폼 무관 |
| `global-metadata.dat` | ✅ **공용** | IL2CPP 메타데이터, 플랫폼 무관 |
| `GameAssembly.dll` | ❌ **Windows 전용** | IL2CPP 바이너리. macOS의 Mach-O와 다름. **Windows Steam 설치본 필요** |

> **핵심**: `resources.assets`는 그대로 써도 된다. 하지만 `Unity_Font_Replacer`가 Il2CppDumper를 실행할 때 `GameAssembly.dll`(Windows 바이너리)를 읽어야 하므로, **Windows Steam에 Twilight Struggle이 설치되어 있어야** 한다.

---

## Step 1: Windows로 파일 이동

### 1-1. macOS에서 Windows로 보낼 파일 준비

```bash
cd ~/Projects/twilight-struggle-kr-patch

# 임시 전송 폴더 (macOS)
mkdir -p ~/ts-windows-transfer

# SDF 폰트 결과물 → Windows로
cp fonts/NotoSerifKR\ SDF* ~/ts-windows-transfer/
cp fonts/BlackHanSans-Regular\ SDF* ~/ts-windows-transfer/
cp fonts/chars.txt ~/ts-windows-transfer/

# Unity_Font_Replacer 도구 (exe 포함 zip) → Windows로
cp tools/unity-font-replacer/Unity_Font_Replacer_v1.2.8.zip ~/ts-windows-transfer/
```

### 1-2. Windows에서 압축 해제 및 게임 파일 경로 확인

```
Windows 탐색기에서 ts-windows-transfer 폴더 열기:
  Unity_Font_Replacer_v1.2.8.zip → 압축 해제 → Unity_Font_Replacer 폴더 생성

Windows Steam Twilight Struggle 설치 경로 확인:
  기본값: C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle\
  └── TwilightStruggle_Data\
        ├── resources.assets       ← 이 파일을 수정할 것
        ├── il2cpp_data\Metadata\global-metadata.dat
        └── ...
  └── GameAssembly.dll             ← Il2CppDumper가 필요로 함
```

### 1-3. 작업 폴더 구성

```bat
cd C:\Users\<사용자명>\Downloads\ts-windows-transfer

:: SDF 파일들을 Unity_Font_Replacer\ASSETS\로 복사
copy NotoSerifKR*.json Unity_Font_Replacer\ASSETS\
copy NotoSerifKR*.png Unity_Font_Replacer\ASSETS\
copy BlackHanSans-Regular*.json Unity_Font_Replacer\ASSETS\
copy BlackHanSans-Regular*.png Unity_Font_Replacer\ASSETS\
copy chars.txt Unity_Font_Replacer\

:: 게임 원본 백업 (Windows Steam 설치본에서)
mkdir BACKUP
copy "C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle\TwilightStruggle_Data\resources.assets" BACKUP\
copy "C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle\TwilightStruggle_Data\sharedassets*.assets" BACKUP\
```
  Unity_Font_Replacer_v1.2.8.zip → 압축 해제 → Unity_Font_Replacer 폴더 생성됨
```

---

## Step 2: Windows에서 폰트 주입

### 2-1. 명령 프롬프트(CMD) 열기

```
Win+R → cmd 입력 → Enter
```

### 2-2. 게임 폰트 parse (기존 폰트 목록 확인)

```bat
cd C:\Users\<사용자명>\Downloads\ts-windows-transfer\Unity_Font_Replacer

:: 게임 경로를 Windows Steam 설치본으로 지정
UnityFontReplacer_KO.exe parse --gamepath "C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle"
```

→ `Twilight Struggle.json` 파일 생성됨. 열어서 폰트 목록 확인 가능.

### 2-3. oneshot으로 전체 폰트 교체

> **주의**: `--oneshot`은 게임의 모든 TTF + SDF 폰트를 한 번에 지정한 TTF로 교체한다.

```bat
:: NotoSerifKR로 모든 폰트 교체 (본문+UI)
UnityFontReplacer_KO.exe oneshot ^
  --gamepath "C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle" ^
  --font "..\NotoSerifKR.ttf" ^
  --charset chars.txt
```

> **참고**: `--font`에는 TTF 원본을 지정한다. 도구가 내부적으로 `make_sdf`를 실행해 SDF를 생성한 뒤 주입한다.

또는 미리 생성한 SDF를 직접 지정:

```bat
:: 방법 B: 미리 생성한 SDF JSON을 직접 지정 (list 방식)
:: 1) parse로 생성된 JSON에서 각 폰트의 Replace_to를 "NotoSerifKR SDF"로 수정
:: 2) list 명령으로 적용

notepad "Twilight Struggle.json"
:: 각 폰트 항목의 "Replace_to" 필드를 "NotoSerifKR SDF.json" 으로 수정

UnityFontReplacer_KO.exe list ^
  --gamepath "C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle" ^
  --file "Twilight Struggle.json"
```

---

## Step 3: macOS로 결과물 복사

### 3-1. Windows에서 수정된 파일만 복사

```
Windows Steam 폴더에서 수정된 파일을 macOS로 전송 (AirDrop, SMB, USB 등):

  C:\Program Files (x86)\Steam\steamapps\common\Twilight Struggle\TwilightStruggle_Data\
  ├── resources.assets      ← 폰트 아틀라스 교체됨 (14MB)
  └── sharedassets*.assets  ← TTF 폰트 에셋 교체됨
```

### 3-2. macOS 프로젝트에 반영

```bash
cd ~/Projects/twilight-struggle-kr-patch

# 수정된 파일을 patched/로 복사
cp ~/Downloads/resources.assets patched/
cp ~/Downloads/sharedassets*.assets patched/ 2>/dev/null

# Steam 무결성 검사 대비: 원본 해시 기록
shasum -a 256 patched/resources.assets > patched/hashes.txt
```

### 3-3. 게임에 적용 및 코드사인

```bash
GAME_DATA="$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data"

# 원본 백업 (최초 1회)
cp "$GAME_DATA/resources.assets" "$GAME_DATA/resources.assets.bak" 2>/dev/null

# 수정본 복사
cp patched/resources.assets "$GAME_DATA/"
cp patched/sharedassets*.assets "$GAME_DATA/" 2>/dev/null

# macOS 코드사인 (필수!)
APP="$HOME/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app"
codesign --force --sign - "$APP"
```

---

## Step 4: 테스트

1. Steam에서 Twilight Struggle 실행
2. 게임 언어를 교체 대상 언어(현재는 Phase 4 결정)로 전환
3. 메인 메뉴, 카드 텍스트, 툴팁에서 한글이 `□` 없이 정상 표시되는지 확인
4. `□` 발생 시:
   - 누락 문자 확인 → `chars.txt`에 추가 → Step 2-5 재실행
   - Material 설정 이상 → `--use-game-material` 옵션 추가 테스트

---

## 문제 해결

| 증상 | 원인 가능성 | 대응 |
|---|---|---|
| `UnityFontReplacer_KO.exe` 실행 안 됨 | .NET Runtime 없음 | [.NET 8.0 Runtime](https://dotnet.microsoft.com/download/dotnet/8.0) 설치 |
| `classdata.tpk` 오류 | TPK 자동 다운로드 실패 | 인터넷 연결 확인. 수동 다운로드: `%USERPROFILE%\.unitypy\classdata.tpk` |
| `Il2cpp 게임의 경우 Managed 폴더 필요` | IL2CPP 덤프 필요 | 도구가 `Il2CppDumper/Il2CppDumper.exe`를 자동 실행. 실패 시 `Il2CppDumper` 폴더 확인 |
| `resources.assets` 손상 | 주입 중 오류 | `BACKUP/`에서 원본 복원 후 재시도 |
| 게임 실행 안 됨 | 코드사인 필요 (macOS) | `codesign --force --sign -` 실행 |
| 한글 `□` 여전히 표시 | SDF 아틀라스에 글리프 없음 | `chars.txt`에 누락 글자 추가 후 Step 2-5 재실행 |
