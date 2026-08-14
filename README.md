# Twilight Struggle 한글 패치

Steam판 **Twilight Struggle**(App ID `406290`)을 위한 비공식 한글 패치입니다.

최신 릴리스는 [`v0.1.1`](https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1)입니다. 카드와 메뉴부터 인게임 UI, 규칙북, 도움말까지 파일로 수정할 수 있는 텍스트를 한글화했습니다.

> 이 패치는 **Steam 데스크톱판**을 대상으로 합니다. 모바일판은 별도 앱이라 이 패치를 적용할 수 없습니다.

## 대상 버전

- Steam `Twilight Struggle` — App ID `406290`
- Unity 6 `6000.0.58f2`, IL2CPP 빌드
- Windows 10/11, macOS 10.13 이상

## 설치 전에

1. 게임이 설치되어 있는지 확인합니다.
2. 위 릴리스 페이지에서 운영체제에 맞는 zip 파일을 받습니다.
   - Windows: `...-windows.zip`
   - macOS: `...-macos.zip`
3. zip 파일을 통째로 압축 해제합니다. 설치 스크립트는 압축을 푼 폴더 안에서 실행해야 합니다.
4. 설치 전에 게임을 완전히 종료합니다.

패키지 안의 `SHA256SUMS`로 파일 해시를 확인할 수 있습니다. 원본 게임 파일은 설치 스크립트가 처음 실행될 때 `.bak`으로 백업합니다.

## 설치

### Windows

압축을 푼 폴더에서 PowerShell을 열고 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1
```

Steam 라이브러리 위치를 자동으로 찾지 못하면 `TwilightStruggle_Data` 폴더를 직접 지정합니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-windows.ps1 `
  -GameData "D:\SteamLibrary\steamapps\common\Twilight Struggle\TwilightStruggle_Data"
```

스크립트는 원본을 백업한 뒤 패치 파일을 복사하고 SHA-256 해시를 확인합니다. 게임이 실행 중이면 먼저 종료해야 합니다.

### macOS

압축을 푼 폴더에서 터미널을 열고 실행합니다.

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

스크립트가 기본 Steam 경로와 `libraryfolders.vdf`에 등록된 추가 라이브러리에서 게임을 찾습니다. 파일을 복사한 뒤 macOS에서 실행할 수 있도록 임시 코드 서명도 시도합니다.

### 언어 설정

게임의 언어 설정은 건드리지 않습니다. 기본 언어인 **EN 열의 문자열을 한글로 바꾸는 방식**이라 별도로 게임 언어를 KO로 변경할 필요가 없습니다. 설치하면 한글이 표시되고, 원본 파일을 복원하면 영어로 돌아갑니다.

## 제거 및 원상 복구

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall-windows.ps1
```

### macOS

```bash
./scripts/uninstall.sh
```

제거 스크립트는 설치 때 만든 `.bak` 파일을 복원합니다. `.bak` 파일이 없거나 Steam 업데이트로 게임 버전이 바뀐 경우에는 Steam에서 다음 절차를 실행하는 편이 안전합니다.

> Steam 라이브러리 → `Twilight Struggle` 속성 → 설치된 파일 → **파일 무결성 확인**

무결성 확인이나 게임 업데이트를 실행하면 패치 파일이 원본으로 되돌아갈 수 있습니다. 그 경우 게임 버전에 맞는 배포본으로 설치를 다시 실행하세요.

## 패치 범위와 알려진 한계

### 한글화한 부분

| 영역 | 내용 |
|---|---|
| 텍스트 테이블 | 카드 이름·본문·사건, 국가명, 메뉴, 설정, 로비, 인게임 HUD, 규칙북·도움말 |
| 씬 텍스트 | 메인 메뉴와 보드에 포함된 하드코딩 문자열, 규칙 안내 문단 |
| 폰트 | 본문 D2Coding, 제목 Paperlogy 5 Medium 기반 한글 지원 SDF 폰트 |

### 아직 영어로 남는 부분

다음 문자열은 게임 에셋이 아니라 IL2CPP 코드에 들어 있어 파일만 바꿔서는 수정할 수 없습니다.

- 게임 하단의 턴 히스토리 로그
- 튜토리얼의 단계별 안내 문구

이 두 부분은 별도의 BepInEx 런타임 훅이 필요해 현재 보류 중입니다. 보드맵 이미지에 글자로 구워진 국가명도 이 패치의 범위에 포함하지 않았습니다.

또한 싱글플레이 기준으로 확인했으며, **멀티플레이는 아직 검증하지 않았습니다.**

## 지원 플랫폼

| 플랫폼 | 상태 | 적용 방법 |
|---|---|---|
| Windows 10/11 | 설치·실행 확인 | Windows 배포본과 `install-windows.ps1` 사용 |
| macOS 10.13 이상 | 설치·실행 확인 | macOS 배포본과 `install.sh` 사용 |
| Steam Deck | Proton에서 사용 가능하나 별도 실게임 검증은 하지 않음 | Windows 배포본 사용 |
| 일반 Linux | Proton에서 사용 가능하나 별도 실게임 검증은 하지 않음 | Steam에서 Proton을 사용하고 Windows 배포본 적용 |
| Android / iOS | 지원하지 않음 | 데스크톱판과 별도 빌드인 모바일 앱에는 적용할 수 없음 |

Steam Deck이나 Linux에서 사용할 때는 Windows 빌드가 Proton으로 실행되므로 Windows 배포본을 선택합니다. `level1`~`level3` 씬 파일은 플랫폼별로 만들어졌으므로 Windows와 macOS 파일을 서로 섞어 복사하지 마세요.

## 개발자용: 패치 재생성

일반 사용자는 이 절을 건너뛰어도 됩니다. 번역 소스와 파이프라인을 수정하거나 Steam 업데이트에 대응할 때 사용하는 절차입니다.

작업 중에는 Steam 설치 폴더를 직접 수정하지 말고, `original/`과 `patched/<플랫폼>/`을 사용합니다. UnityPy는 공식 버전이 아니라 `snowyegret23` 포크와 `TypeTreeGeneratorAPI`가 필요합니다. 자세한 도구 목록은 [`scripts/README.md`](scripts/README.md)를 참고하세요.

아래 명령의 `<게임 루트>`, `<원본 resources.assets>`, `<중간본>`은 실제 경로로 바꿉니다. `python`은 `TypeTreeGeneratorAPI`가 설치된 프로젝트 가상 환경의 Python을 사용해야 합니다. Windows와 macOS는 각각의 원본으로 씬을 따로 패치해야 합니다.

```bash
# 1. TextAsset에 번역 주입
python scripts/inject_translations.py \
  --gamepath <게임 루트> \
  --src <원본 resources.assets> \
  --platform windows \
  --out <중간본-번역>

# 2. 구형 KO 설정과의 호환을 위해 KO 열 추가
python scripts/add_ko_columns.py \
  --gamepath <게임 루트> \
  --src <중간본-번역> \
  --out patched/windows/resources.assets

# 3. level1~3 씬 패치 — 플랫폼별 원본을 사용
python scripts/patch_scenes.py \
  --gamepath <게임 루트> \
  --platform windows

# 4. Unity_Font_Replacer로 폰트 주입
#    절차: tools/README.md 및 폰트 주입 스킬 참고

# 5. 최종 에셋 검증
python scripts/verify_assets.py \
  --orig <원본 resources.assets> \
  --patched patched/windows/resources.assets
```

폰트 주입은 [Unity_Font_Replacer v1.2.8](https://github.com/snowyegret23/Unity_Font_Replacer)을 사용합니다. macOS에서 재현하거나 게임이 업데이트된 경우의 전체 절차는 [Phase 문서](docs/phases/phase-4-injection-layout.md)와 [`scripts/README.md`](scripts/README.md)에 정리되어 있습니다.

번역을 수정할 때는 [`translation/`](translation/)의 JSON을 변경한 뒤 주입 스크립트를 다시 실행합니다. 번역 소스별 역할은 [`translation/README.md`](translation/README.md)에서 확인할 수 있습니다.

## 저장소 안내

| 경로 | 설명 |
|---|---|
| [`scripts/`](scripts/) | 번역 주입, 씬 패치, 폰트·에셋 검증, 설치·제거 스크립트 |
| [`translation/`](translation/) | 번역 원문과 한국어 매핑, 용어표 |
| [`fonts/`](fonts/) | SDF 폰트와 라이선스 |
| [`tools/`](tools/) | 폰트 주입 도구와 에셋 조사 도구 |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | 전체 진행 상황과 검증 기록 |
| [`docs/phases/`](docs/phases/) | Phase별 작업 기록 |

## 번역 출처와 감사의 말

이 프로젝트의 번역은 처음부터 새로 작성한 것이 아니라 기존 커뮤니티 한글 패치를 바탕으로 구성했습니다.

- [한식구 네이버 카페 런타임 패치](https://cafe.naver.com/hansicgu/32259) — 런타임 TSV 2,253쌍을 1차 번역 소스로 재사용했습니다.
- [블루칩님 한글 패치](https://bluechip2022.tistory.com/2) — 현재 버전에서는 동작하지 않지만 번역 매칭과 검증에 참고했습니다.

기존 패치 제작자와 번역 원저작자께 감사드립니다. 번역문의 권리와 사용 조건은 원저작자의 정책을 따르며, 자세한 내용은 [`LICENSE`](LICENSE)를 확인하세요.

## 라이선스

- 이 저장소에서 직접 작성한 소스 코드와 문서: MIT License
- 기존 커뮤니티 패치에서 가져오거나 참고한 번역문: 각 원저작자의 정책 적용
- 게임 에셋과 원작 관련 저작권: Playdek, Valve/Steam, GMT Games 등 각 권리자에게 있음
- D2Coding과 Paperlogy 폰트: SIL Open Font License 1.1

전체 조건은 [`LICENSE`](LICENSE), 폰트 라이선스는 [`fonts/README-fonts.md`](fonts/README-fonts.md)와 `fonts/LICENSE-OFL-1.1.txt`에서 확인할 수 있습니다.
