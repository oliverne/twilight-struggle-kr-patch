# Twilight Struggle 한글 패치

Steam판 **Twilight Struggle**(App ID `406290`)용 한글 패치 프로젝트입니다.

> **한글화 완료 (2026-08-13).** 카드/메뉴/인게임 UI/규칙북/도움말/씬 텍스트 **파일 패치 범위 100% 한글화**.
> 배포는 보류 — 남은 영어는 IL2CPP 코드 문자열(턴 히스토리·튜토리얼 안내)로 BepInEx 훅이 필요합니다.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 대상 게임 | Steam Twilight Struggle (Unity 6 `6000.0.58f2`, IL2CPP) |
| 번역 주입 (TextAsset) | ✅ 666행 + 잔존 키 52개 — `Common_Strings`, `TS_Cards`, `TS_Ingame`, `TS_Strings`, `Common_Ingame` — **EN 열에 한글 주입 (EN 로케일 대체)** |
| 언어 테이블 KO 열 | ✅ 5개 테이블 KO 열 추가 — 구형 KO 설정 호환용 (2026-08-14: 설정 무조작 방식 전환) |
| 씬 하드코딩 문자열 | ✅ 2,548개 + 규칙 문단 — level1(메인 메뉴)·level2(인게임)·level3(보드) |
| 규칙북/도움말 (Phase 7) | ✅ TS_RulesTutorial 313행 + 씬 규칙 문단 — 용어표·검수 완료 (2026-08-13) |
| 한글 SDF 폰트 | ✅ 2048² SDF 2종(D2Coding 본문, Paperlogy 제목, 739자) → 24개 TMP 폰트 주입 |
| 게임 언어 설정 | ✅ 불필요 — **EN 로케일을 한글로 대체** (설정 무조작, 2026-08-14) |
| Windows 실게임 테스트 | ✅ 4차 완료 — **카드·메뉴·인게임 UI 대부분 한글화 확인** |
| macOS 실게임 테스트 | ✅ 완료 — macOS 원본 기준 파이프라인 재현 + 설치 확인 (2026-08-12) |
| 미번역 텍스트 확인 | ✅ 화면 단위 확인 (2026-08-12, 전수 조사는 미실시) |
| 멀티플레이 | ⬜ 미검증 |

상세 진행 상황은 [`docs/PROGRESS.md`](docs/PROGRESS.md)를 참조하세요.

## 패치 범위

**한글화 완료**
- 카드 이름·본문·사건, 국가명 (TS_Cards)
- 메인 메뉴, 설정, 로비/친구/계정 UI (Common_Strings + 씬 패치)
- 인게임 HUD — 턴 트랙, 데프콘, 우주 경쟁, 득점, 입찰, 쿠데타/재편성 배너 등 (TS_Ingame + 씬 패치)

**한글화 제외 (알려진 한계 — 파일 패치 불가, BepInEx 런타임 훅 필요)**
- 턴 히스토리 로그(게임 하단) — IL2CPP 코드 문자열 (global-metadata.dat)
- 튜토리얼 단계별 안내 가이드 — IL2CPP 코드 문자열 (2026-08-13 실측, ISSUES #17)
- 보드맵에 텍스처로 구워진 국가명 (이미지 리터칭 필요, 범위 제외)

## 지원 플랫폼

| 플랫폼 | 지원 | 비고 |
|---|---|---|
| Windows 10/11 | ✅ 공식 지원 | 설치: `install-windows.ps1` |
| macOS 10.13+ | ✅ 공식 지원 | 설치: `install.sh` (애드혹 재서명 자동) |
| 스팀덱 | ✅ 지원 (Proton) | Windows 배포본 파일 사용 — Linux 네이티브 빌드 없음 |
| Linux (일반) | ✅ 지원 (Proton) | Steam에서 Proton 강제 설정 후 Windows 배포본 적용 |
| Android / iOS | ❌ 지원 불가 | Playdek의 **별도 모바일 앱**(별도 빌드·구매) — 데스크톱 에셋 적용 불가. Steam Link 스트리밍으로 한글화 화면 감상만 가능 |

> 스팀덱/리눅스는 게임 실행 방식이 Proton(Windows 빌드)이므로 **Windows 배포본 파일을 그대로 복사**하면 됩니다.
> 언어 설정은 건드리지 않으므로 Wine prefix 조작이 필요 없습니다 (2026-08-14 개정).

## 설치 방법

배포 zip을 압축 해제한 뒤 운영체제별 설치 스크립트를 실행합니다 (백업 → 복사만 — 언어 설정은 건드리지 않습니다).

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
2. `patched/<플랫폼>/` 폴더 (windows 또는 macos)의 같은 이름 파일을 게임 Data 폴더에 복사
3. macOS는 추가로 `codesign --force --sign -` 재서명 필요

### 제거 (영문/원래 언어 복귀)

설치 스크립트가 적용한 것을 모두 원상 복구합니다.

- Windows: `powershell -ExecutionPolicy Bypass -File scripts\uninstall-windows.ps1`
- macOS: `./scripts/uninstall.sh`

원본 파일을 `.bak`에서 복원합니다. 게임 언어 설정은 건드리지 않습니다 (EN 로케일 대체 방식 — 복원만 하면 영어로 돌아감).

⚠️ **패치 파일만 지우면 안 됩니다.** Steam 무결성 확인만 하면 파일이 원복되어 영어로 돌아갑니다. `.bak`이 없을 때(Steam 업데이트 등)는 Steam 무결성 확인을 먼저 실행한 뒤 위 스크립트를 다시 실행하세요.

## 안전 원칙

- Steam 설치 폴더에서 직접 개발하지 않습니다.
- 원본은 `original/`에 백업하고, 수정 결과는 `patched/windows/`(Windows)·`patched/macos/`(macOS)에 플랫폼별로 둡니다.
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

# 3. 폰트 주입 — Unity_Font_Replacer (Windows exe 또는 macOS 소스 실행, Runbook 참조)
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

- 폰트: D2Coding, Paperlogy 5 Medium (SIL OFL 1.1) — `fonts/`에 라이선스 동봉
- 번역문: 기존 한글 패치(블루칩 등)의 번역을 참고·재사용 — 배포 전 크레딧 정리 필요 (Phase 6)
