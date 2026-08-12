# Twilight Struggle 한글 패치

Steam판 **Twilight Struggle**(App ID `406290`)용 한글 패치 프로젝트입니다.

> **현재 개발 중 (Phase 5).** Windows 실게임에서 **카드/메뉴/인게임 UI 대부분 한글화 확인** (2026-08-12).
> 미번역 잔존 확인·macOS 적용·멀티플레이 검증이 남아 있습니다.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 대상 게임 | Steam Twilight Struggle (Unity 6 `6000.0.58f2`, IL2CPP) |
| 번역 주입 (TextAsset) | ✅ 666행 + 잔존 키 53개 — `Common_Strings`(KO 열), `TS_Cards`, `TS_Ingame`, `TS_Strings`, `Common_Ingame` |
| 언어 테이블 KO 열 | ✅ 5개 테이블에 KO 열 추가 (언어=KO에서 카드/PANEL/HELP 키 해석) |
| 씬 하드코딩 문자열 | ✅ 2,548개 — level1(메인 메뉴)·level2(인게임)·level3(보드) |
| 한글 SDF 폰트 | ✅ 2048² SDF 2종(Noto Serif KR, Black Han Sans, 739자) → 24개 TMP 폰트 주입 |
| 게임 언어 설정 | ✅ KO 전환 (레지스트리 PlayerPrefs) |
| Windows 실게임 테스트 | ✅ 4차 완료 — **카드·메뉴·인게임 UI 대부분 한글화 확인** |
| 미번역 텍스트 전체 확인 | ⬜ 영어 잔존 수집 중 |
| macOS 적용 | ⬜ `patched/` 전송 + `scripts/install.sh` |
| 멀티플레이 | ⬜ 미검증 |

상세 진행 상황은 [`docs/PROGRESS.md`](docs/PROGRESS.md)를 참조하세요.

## 패치 범위

**한글화 완료**
- 카드 이름·본문·사건, 국가명 (TS_Cards)
- 메인 메뉴, 설정, 로비/친구/계정 UI (Common_Strings + 씬 패치)
- 인게임 HUD — 턴 트랙, 데프콘, 우주 경쟁, 득점, 입찰, 쿠데타/재편성 배너 등 (TS_Ingame + 씬 패치)

**한글화 제외 (알려진 한계)**
- 턴 히스토리 로그(게임 하단) — IL2CPP 코드 문자열이라 파일 패치 불가 (BepInEx 런타임 훅 필요)
- 보드맵에 텍스처로 구워진 국가명
- 규칙북/튜토리얼 본문 중 씬에 하드코딩된 긴 문단 (일부)

## 설치 방법

배포 zip을 압축 해제한 뒤 운영체제별 설치 스크립트를 실행합니다 (백업 → 복사 → 언어 KO 설정 자동 처리).

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
```

### macOS

```bash
./scripts/install.sh
```

수동으로 하면 아래와 같습니다 (스크립트가 이 과정을 자동 수행):

1. 게임 종료 상태에서 `TwilightStruggle_Data/` 폴더의 다음 파일을 백업:
   `resources.assets`, `sharedassets0.assets`, `level1`, `level2`, `level3`
2. `patched/` 폴더의 같은 이름 파일을 게임 Data 폴더에 복사
3. 게임 언어를 KO로 설정 (Windows: 레지스트리 `HKCU\Software\Playdek\TwilightStruggle`의 `localization_h2525087814` / macOS: `~/Library/Preferences/unity.Playdek.TwilightStruggle.plist`의 `localization`)
4. macOS는 추가로 `codesign --force --sign -` 재서명 필요

### 제거 (영문/원래 언어 복귀)

설치 스크립트가 적용한 것을 모두 원상 복구합니다.

- Windows: `powershell -ExecutionPolicy Bypass -File scripts\uninstall-windows.ps1`
- macOS: `./scripts/uninstall.sh`

원본 파일을 `.bak`에서 복원하고, 게임 언어를 **설치 전 값**으로 되돌립니다 (설치 시 `krpatch-install-info.txt`에 기록).

⚠️ **패치 파일만 지우면 안 됩니다.** Steam 무결성 확인만 하면 파일은 원복되지만 언어가 KO로 남아 메뉴·카드가 `${Key}`로 표시됩니다. `.bak`이 없을 때(Steam 업데이트 등)는 Steam 무결성 확인을 먼저 실행한 뒤 위 스크립트를 다시 실행하세요.

⚠️ **게임 삭제·재설치를 해도 언어 설정은 남습니다.** macOS plist(`~/Library/Preferences/`)와 Windows 레지스트리는 게임 폴더 밖에 있어 Steam이 지우지 않습니다. 재설치 후 언어가 KO로 남아 있으면 `${Key}`가 표시되므로 아래를 실행하세요 (이 게임에는 언어 선택 UI가 없어 PlayerPrefs 값 변경으로만 바뀝니다):

```bash
# macOS
defaults write ~/Library/Preferences/unity.Playdek.TwilightStruggle.plist localization -string "EN"
defaults write ~/Library/Preferences/unity.Playdek.TwilightStruggle.plist localization_h2525087814 -string "EN"
```

```powershell
# Windows
Set-ItemProperty -Path "HKCU:\Software\Playdek\TwilightStruggle" -Name "localization_h2525087814" -Value "EN"
```

## 안전 원칙

- Steam 설치 폴더에서 직접 개발하지 않습니다.
- 원본은 `original/`에 백업하고, 수정 결과는 `patched/`에 둡니다.
- 모든 실제 패치 적용은 멱등적인 설치 스크립트로 수행합니다.
- macOS에서 게임 파일을 수정하면 애드혹 코드 서명이 필요합니다.
- 원본 백업과 레거시 패치 파일은 용량 및 저작권 문제로 Git에 포함하지 않습니다.

## 재현 (패치 파일 재생성)

패치 파일은 아래 순서로 언제든 재생성할 수 있습니다 (상세: [`docs/phases/phase-4-injection-layout.md`](docs/phases/phase-4-injection-layout.md), [`docs/phases/phase-5-platform-test.md`](docs/phases/phase-5-platform-test.md))

```bash
# 1. 번역 주입 (TextAsset) — 포크 UnityPy + typetree_generator 필수
python scripts/inject_translations.py --gamepath <게임루트> \
    --src <원본 resources.assets> --out <중간본1>

# 2. 언어 테이블 KO 열 추가 (TS_Cards 9열 / 그 외 8·10열 — 멱등)
python scripts/add_ko_columns.py --gamepath <게임루트> \
    --src <중간본1> --out <중간본2>

# 3. 폰트 주입 — Windows에서 Unity_Font_Replacer (Runbook 참조)
#    가상 폴더의 resources.assets를 <중간본2>로 교체 후 --parse → 매핑 → --list

# 4. 씬 패치 (level1-3)
python scripts/patch_scenes.py --gamepath <게임루트>

# 5. 검증
python scripts/verify_assets.py --orig <원본> --patched <패치본>
```

## 번역 소스

| 파일 | 내용 |
|---|---|
| `translation/runtime-20260315.json` | 런타임 패치 TSV 2,253쌍 (기존 한글화 재사용) |
| `translation/strings.json`, `cards.json` | Common_Strings·TS_Cards 키 매핑 |
| `translation/manual-extra.json` | TS_Ingame/TS_Strings 잔존 키 수동 번역 52개 |
| `translation/manual-scenes.json` | 씬 하드코딩 문자열 수동 번역 206개 |

새 문자열 추가 시 해당 JSON에 키-값을 추가한 뒤 1·2·4단계 재실행. 상세: [translation/README.md](translation/README.md)

## 폴더별 인벤토리

| 폴더 | 설명 |
|---|---|
| [scripts/](scripts/README.md) | 주입·검증 스크립트 (핵심 5종 + 보조 + archive 보관) |
| [tools/](tools/README.md) | 폰트 주입 도구·에셋 탐색 (Unity_Font_Replacer 등) |
| [translation/](translation/README.md) | 번역 소스 (활성 5종 + 참고 산출물) |
| [docs/](docs/PROGRESS.md) | 진행 현황·Phase 문서·Runbook |

## 라이선스

- 폰트: Noto Serif KR, Black Han Sans (SIL OFL 1.1) — `fonts/`에 라이선스 동봉
- 번역문: 기존 한글 패치(블루칩 등)의 번역을 참고·재사용 — 배포 전 크레딧 정리 필요 (Phase 6)
