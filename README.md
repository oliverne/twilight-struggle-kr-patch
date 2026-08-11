# Twilight Struggle 한글 패치

Steam판 **Twilight Struggle**(App ID `406290`)용 한글 패치 프로젝트입니다.

> **현재 개발 중 (Phase 5).** Windows 실게임에서 카드/인게임/메뉴 한글화를 확인했으며,
> macOS 적용·멀티플레이 검증이 남아 있습니다. 배포 전까지는 직접 적용 후 테스트해 주세요.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 대상 게임 | Steam Twilight Struggle (Unity 6 `6000.0.58f2`, IL2CPP) |
| 번역 주입 (TextAsset) | ✅ 666행 + 잔존 키 53개 — `Common_Strings`(KO 열), `TS_Cards`, `TS_Ingame`, `TS_Strings`, `Common_Ingame` |
| 씬 하드코딩 문자열 | ✅ 2,548개 — level1(메인 메뉴)·level2(인게임)·level3(보드) |
| 한글 SDF 폰트 | ✅ 2048² SDF 2종(Noto Serif KR, Black Han Sans) → 24개 TMP 폰트 주입 |
| 게임 언어 설정 | ✅ KO 전환 (레지스트리 PlayerPrefs) |
| Windows 실게임 테스트 | ✅ 1차 완료 — 카드/인게임 한글 출력 확인 |
| 메뉴 한글화 재확인 | ⬜ 게임 재실행 대기 |
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

### Windows

1. 게임 종료 상태에서 `TwilightStruggle_Data/` 폴더의 다음 파일을 백업:
   `resources.assets`, `sharedassets0.assets`, `level1`, `level2`, `level3`
2. `patched/` 폴더의 같은 이름 파일 5개를 `TwilightStruggle_Data/`에 복사
3. 게임 실행 → 설정 → Languages에서 **한국어** 선택
   (또는 레지스트리 `HKCU\Software\Playdek\TwilightStruggle`의 `localization_h2525087814`를 `KO`로 변경)

### macOS

1. `patched/`의 파일 5개를 `TwilightStruggle.app/Contents/Resources/Data/`에 복사
2. `scripts/install.sh` 실행 (백업 → 복사 → `codesign --force --sign -` 자동 처리)

### 복구

- 백업해둔 파일을 되돌리거나 Steam "파일 무결성 확인" 실행

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
    --src <원본 resources.assets> --out <중간본>

# 2. 폰트 주입 — Windows에서 Unity_Font_Replacer (Runbook 참조)

# 3. 씬 패치 (level1-3)
python scripts/patch_scenes.py --gamepath <게임루트>

# 4. 검증
python scripts/verify_assets.py --orig <원본> --patched <패치본>
```

## 번역 소스

| 파일 | 내용 |
|---|---|
| `translation/runtime-20260315.json` | 런타임 패치 TSV 2,253쌍 (기존 한글화 재사용) |
| `translation/strings.json`, `cards.json` | Common_Strings·TS_Cards 키 매핑 |
| `translation/manual-extra.json` | TS_Ingame/TS_Strings 잔존 키 수동 번역 53개 |
| `translation/manual-scenes.json` | 씬 하드코딩 문자열 수동 번역 206개 |

새 문자열 추가 시 해당 JSON에 키-값을 추가한 뒤 1·3단계 재실행.

## 라이선스

- 폰트: Noto Serif KR, Black Han Sans (SIL OFL 1.1) — `fonts/`에 라이선스 동봉
- 번역문: 기존 한글 패치(블루칩 등)의 번역을 참고·재사용 — 배포 전 크레딧 정리 필요 (Phase 6)
