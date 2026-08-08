# Phase 3 Runbook — Windows에서 Unity_Font_Replacer로 SDF 폰트 주입

> **상태**: macOS에서 `make_sdf.py`로 SDF 생성 완료, Windows에서 `Unity_Font_Replacer_KO.exe`로 주입

## 사전 준비물

- **Windows PC** (또는 Parallels/VM)
- **macOS 프로젝트 폴더** (`twilight-struggle-kr-patch/`) — 외장 드라이브나 네트워크 공유, 또는 파일 복사
- 생성 완료된 SDF 파일:
  - `fonts/NotoSerifKR SDF.json` + `NotoSerifKR SDF Atlas.png` + `NotoSerifKR SDF Material.json`
  - `fonts/BlackHanSans-Regular SDF.json` + `BlackHanSans-Regular SDF Atlas.png` + `BlackHanSans-Regular SDF Material.json`
  - `fonts/chars.txt`

---

## Step 1: Windows로 파일 이동

### 1-1. 게임 원본 파일 준비 (macOS)

```bash
# Steam 게임 폴더에서 Data 디렉토리 전체를 Windows로 복사할 준비
GAME_DATA="/Users/oliverne/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data"

# 임시 작업 폴더에 복사 (macOS)
mkdir -p ~/ts-windows-transfer/TwilightStruggle_Data
cp -R "$GAME_DATA"/* ~/ts-windows-transfer/TwilightStruggle_Data/
# ※ resources.assets가 14MB, 전체 약 67MB. 외장 드라이브나 SMB/AirDrop으로 Windows에 전달
```

### 1-2. SDF 폰트 파일 + 도구 복사

```bash
# 프로젝트 폴더에서 Windows로 전달할 파일들
cd ~/Projects/twilight-struggle-kr-patch

# SDF 폰트 결과물
cp fonts/NotoSerifKR\ SDF* ~/ts-windows-transfer/
cp fonts/BlackHanSans-Regular\ SDF* ~/ts-windows-transfer/
cp fonts/chars.txt ~/ts-windows-transfer/

# Unity_Font_Replacer 도구 (이미 다운로드 완료)
cp -R tools/unity-font-replacer/src/*.py ~/ts-windows-transfer/   # Python 스크립트
# 또는 미리 빌드된 exe가 있는 tools/unity-font-replacer/ 폴더 그대로
cp tools/unity-font-replacer/Unity_Font_Replacer_v1.2.8.zip ~/ts-windows-transfer/
```

### 1-3. Windows에서 압축 해제

```
Windows 탐색기에서 ts-windows-transfer 폴더를 열고:
  Unity_Font_Replacer_v1.2.8.zip → 압축 해제 → Unity_Font_Replacer 폴더 생성됨
```

---

## Step 2: Windows에서 폰트 주입

### 2-1. 명령 프롬프트(CMD) 열기

```
Win+R → cmd 입력 → Enter
```

### 2-2. SDF 폰트를 도구의 ASSETS 폴더로 복사

```bat
cd C:\Users\<사용자명>\Downloads\ts-windows-transfer\Unity_Font_Replacer

:: SDF 파일들을 ASSETS 폴더로 복사
copy ..\NotoSerifKR*.json ASSETS\
copy ..\NotoSerifKR*.png ASSETS\
copy ..\BlackHanSans-Regular*.json ASSETS\
copy ..\BlackHanSans-Regular*.png ASSETS\
copy ..\chars.txt .
```

### 2-3. 게임 폰트 parse (기존 폰트 목록 확인)

```bat
UnityFontReplacer_KO.exe parse --gamepath "C:\Users\<사용자명>\Downloads\ts-windows-transfer"
```

→ `ts-windows-transfer.json` 파일 생성됨. 열어서 폰트 목록 확인 가능.

### 2-4. 원본 백업

```bat
:: 게임 파일을 먼저 다른 곳에 백업
mkdir C:\Users\<사용자명>\Downloads\ts-windows-transfer\BACKUP
copy TwilightStruggle_Data\resources.assets BACKUP\
copy TwilightStruggle_Data\sharedassets*.assets BACKUP\
```

### 2-5. oneshot으로 전체 폰트 교체

> **주의**: `--oneshot`은 게임의 모든 TTF + SDF 폰트를 한 번에 지정한 TTF로 교체한다.

```bat
:: NotoSerifKR로 모든 폰트 교체 (본문+UI)
UnityFontReplacer_KO.exe oneshot ^
  --gamepath "C:\Users\<사용자명>\Downloads\ts-windows-transfer" ^
  --font "..\NotoSerifKR.ttf" ^
  --charset chars.txt
```

> **참고**: `--font`에는 TTF 원본을 지정한다. 도구가 내부적으로 `make_sdf`를 실행해 SDF를 생성한 뒤 주입한다.

또는 미리 생성한 SDF를 직접 지정:

```bat
:: 방법 B: 미리 생성한 SDF JSON을 직접 지정 (list 방식)
:: 1) parse로 생성된 JSON에서 각 폰트의 Replace_to를 "NotoSerifKR SDF"로 수정
:: 2) list 명령으로 적용

notepad ts-windows-transfer.json
:: 각 폰트 항목의 "Replace_to" 필드를 "NotoSerifKR SDF.json" 으로 수정

UnityFontReplacer_KO.exe list ^
  --gamepath "C:\Users\<사용자명>\Downloads\ts-windows-transfer" ^
  --file ts-windows-transfer.json
```

---

## Step 3: macOS로 결과물 복사

### 3-1. 수정된 파일만 복사

```bash
# Windows → macOS (AirDrop, SMB, 또는 외장 드라이브)
# 수정된 핵심 파일만 복사
#   TwilightStruggle_Data/resources.assets   ← 가장 중요
#   TwilightStruggle_Data/sharedassets*.assets
```

### 3-2. macOS에 적용

```bash
cd ~/Projects/twilight-struggle-kr-patch

# 원본으로 복원 (혹시 이전 테스트 잔재가 있다면)
scripts/restore-original.sh

# 수정된 파일을 patched/로 복사
cp ~/Downloads/ts-windows-transfer/TwilightStruggle_Data/resources.assets patched/
cp ~/Downloads/ts-windows-transfer/TwilightStruggle_Data/sharedassets*.assets patched/ 2>/dev/null

# macOS 코드사인
codesign --force --sign - "patched/TwilightStruggle.app" 2>/dev/null || \
  echo "※ macOS .app 번들이 아니라면 개별 dylib/dll만 서명"
```

### 3-3. 게임에 적용

```bash
# install 스크립트로 patched → Steam 게임 폴더에 복사 (Phase 4에서 구현)
# 또는 수동으로:
GAME_DATA="/Users/oliverne/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data"
cp patched/resources.assets "$GAME_DATA/"
codesign --force --sign - "$GAME_DATA/../.."
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
