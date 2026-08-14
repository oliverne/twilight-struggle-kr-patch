---
name: twilight-struggle-font-swap
description: Twilight Struggle 한글 패치 프로젝트에서 TMP SDF 폰트(본문 NotoSerifKR / 제목 BlackHanSans)를 다른 폰트로 교체하는 전체 절차. TTF 확보 → make_sdf.py SDF 생성 → KR_ASSETS 교체 → Unity_Font_Replacer 재주입 → 검증 → Steam 설치까지. 폰트 변경 요청 시 사용.
---

# Twilight Struggle 한글 패치 — 폰트 교체 절차

## 배경

- 게임의 24개 TMP 폰트(TIMES·GOTHIC·Anton·Bangers·atwriter 등)에 한글 SDF 2종이 매핑돼 있음
- 본문: `NotoSerifKR SDF` (TIMES/FRAMD/GOTHIC/LiberationSans/Unity 계열 13개)
- 제목: `BlackHanSans-Regular SDF` (Anton/Bangers/Oswald/IMPACT/atwriter 계열 11개)
- 전체 구조는 `docs/runbooks/phase-3-windows-font-injection.md` 참조

## 사전 준비

- Windows 게임 설치본 (GameAssembly.dll 필요 — 가상 폴더 구성용). macOS에서도 소스 실행으로 가능 (Windows 빌드 `GameAssembly.dll`+`global-metadata.dat` 2개만 있으면 됨 — [Runbook Step 5](../../../docs/runbooks/phase-3-windows-font-injection.md))
- `PYTHONIOENCODING=utf-8` + venv python: `.venv/Scripts/python.exe` (Windows) / `.venv/bin/python` (macOS)
- **라이선스 확인**: 재배포 허용 폰트만 (SIL OFL 등). `fonts/`에 라이선스 동봉 필수

## 절차

### 1. TTF 확보 → `fonts/`에 배치

```bash
cp <새폰트>.ttf fonts/
```

### 2. SDF 생성 (문자셋은 기존 `fonts/chars.txt` 재사용)

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe tools/font-inject-work/ufr-src/make_sdf.py \
  --ttf "fonts/<새폰트>.ttf" \
  --charset "fonts/chars.txt" \
  --atlas-size 2048,2048 \
  --point-size 70 --padding 4
```

- 출력: `fonts/<새폰트> SDF.json` + `SDF Atlas.png` + `SDF Material.json`
- point-size 70이 2048² 아틀라스 한계(739자 기준). overflow 시 자동 축소됨
- 새 글자가 필요하면 `fonts/chars.txt`에 추가 후 재생성 (표시 문자열 전체 문자셋 재추출 권장)
- 기존 SDF는 지우지 말고 백업: `mkdir fonts/backup-<date> && cp fonts/*.json fonts/backup-<date>/`

### 3. KR_ASSETS 교체 (핵심: 파일명 유지)

```bash
cp "fonts/<새폰트> SDF.json" "tools/unity-font-replacer/KR_ASSETS/NotoSerifKR SDF.json"   # 본문 교체 시
cp "fonts/<새폰트> SDF Atlas.png" "tools/unity-font-replacer/KR_ASSETS/NotoSerifKR SDF Atlas.png"
cp "fonts/<새폰트> SDF Material.json" "tools/unity-font-replacer/KR_ASSETS/NotoSerifKR SDF Material.json"
```

- **기존 파일명(NotoSerifKR/BlackHanSans-Regular)으로 복사**하면 매핑 JSON(`Twilight Struggle.json`) 수정 불필요
- 파일명을 바꾸면 `scripts/apply_font_mapping.py`로 Replace_to 47개 항목 재설정 필요 (아래 5단계)

### 4. 가상 폴더 준비

```bash
# Steam 폴더를 직접 수정하지 않는다 (불변 원칙)
# tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/ 아래:
#  - resources.assets = 최신 patched/ 복사본
#  - Managed 폴더는 제거/이름변경 필수 (없으면 도구가 Mono로 오판, SDF 폰트 인식 실패)
mv "Twilight Struggle/TwilightStruggle_Data/Managed" "Twilight Struggle/TwilightStruggle_Data/Managed.off"
```

### 5. 폰트 주입 (Unity_Font_Replacer v1.2.8)

```bash
cd tools/unity-font-replacer

# 5-1. 스캔 (stdin 리다이렉트 필수 — 없으면 EOFError)
echo "" | ./unity_font_replacer_ko.exe --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" --parse

# 5-2. 매핑 재설정 (parse가 JSON을 초기화하므로 반드시 재실행)
PYTHONIOENCODING=utf-8 ../../.venv/Scripts/python.exe ../../scripts/apply_font_mapping.py

# 5-3. 주입 (출력 폴더명은 새로 지정 — 기존 산출물 font-output-new2는 덮어쓰지 말 것)
echo "" | ./unity_font_replacer_ko.exe \
  --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" \
  --list "Twilight Struggle.json" \
  --output-only "C:/.../tools/font-inject-work/font-output-<날짜>"
```

### 6. 검증

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/verify_assets.py \
  --orig <주입 전 resources.assets> --patched <font-output/resources.assets>
```

- 성공 기준: `m_Script 불일치 0건`, TextAsset 변경 0건 (KO 열/번역 유지), 폰트/텍스처 변경만 존재

### 7. 설치

```bash
# ⚠️ patched/는 플랫폼별 분리 (2026-08-14): windows / macos 폴더
# 주입 결과를 해당 플랫폼 폴더에 반영 + 해시 갱신 (폴더 내부 기준 상대경로)
cp font-output/resources.assets font-output/sharedassets0.assets patched/<windows|macos>/
cd patched/<플랫폼> && sha256sum level1 level2 level3 resources.assets sharedassets0.assets > hashes.txt && cd -

# Windows
powershell -ExecutionPolicy Bypass -File scripts/install-windows.ps1
# macOS
./scripts/install.sh
```

- 작업 후 `Managed.off` → `Managed` 복원 (가상 폴더 기준)

## 주의사항

- ⚠️ **face info 차이**: 폰트마다 lineHeight/ascent가 달라 표시 크기·줄 간격이 변할 수 있음. 기존과 비슷한 계열 폰트 선택 권장. 원본 게임 메트릭 유지가 필요하면 `--use-game-line-metrics` 재주입 고려 (이슈 #12)
- ⚠️ **한글 글리프**: 제목용 폰트(BlackHanSans 대체)에도 한글 포함 여부 확인. 한글이 없으면 별도 처리
- ⚠️ **문자셋**: 교체 후 `□` 누락 글자 발생 시 chars.txt 확장 → SDF 재생성 → 재주입
- ⚠️ Steam 무결성 확인/업데이트로 패치 원복 가능 — 스킬 `twilight-struggle-update` 참조
- 주입 파이프라인 상세: 스킬 `twilight-struggle-font-injection` (가상 폴더 구성 → parse → 매핑 → 주입 → 검증 → 반영)
- 관련 문서: `docs/runbooks/phase-3-windows-font-injection.md`, `docs/phases/phase-3-sdf-font.md`, `docs/phases/phase-5-platform-test.md` (SDF 재생성 기록)
