---
name: twilight-struggle-update
description: Twilight Struggle 한글 패치가 Steam 게임 업데이트로 무효화/원복됐거나, 새 버전 에셋에 패치를 재적용할 때의 전체 절차. 버전·해시 감지, 원본 백업, 번역 주입→KO 열→씬 패치→폰트 주입 파이프라인 재실행, 구조 변경 검증 포인트, 설치·복구까지.
---

# Twilight Struggle 한글 패치 — 게임 업데이트 대응 절차

## 배경

- 패치는 `translation/`(번역 소스) + `scripts/`(주입 도구) + `patched/`(산출물) 3계층 구조
- 게임 업데이트 시 Steam이 `TwilightStruggle_Data/` 파일을 원본으로 되돌림 → **스크립트 재실행으로 재적용**
- 번역 소스는 그대로 재사용 가능 (새 텍스트만 수동 번역)

## 절차

### 1. 업데이트 감지 (패치 무효화 확인)

```bash
# Steam 설치본 vs patched 해시 비교
sha256sum "D:/Games/steamapps/common/Twilight Struggle/TwilightStruggle_Data/resources.assets"
cat patched/hashes.txt
# 불일치 → 업데이트로 원복됨 → 아래 진행
```

- Player.log 확인: `%LOCALAPPDATA%\..\LocalLow\Playdek\Twilight Struggle\Player.log`
- 언어 설정(레지스트리 `localization_h2525087814`=KO)도 초기화됐는지 확인 (`reg query HKCU\Software\Playdek\TwilightStruggle`)

### 2. 새 원본 백업

```bash
mkdir -p <게임>/TwilightStruggle_Data/backup-<date>
cp <게임>/TwilightStruggle_Data/resources.assets backup-<date>/
cp <게임>/TwilightStruggle_Data/sharedassets0.assets backup-<date>/
cp <게임>/TwilightStruggle_Data/level1 level2 level3 backup-<date>/
```

### 3. 파이프라인 재실행 (순서 고정)

```bash
# 3-1. 번역 주입 (TextAsset — Common_Strings KO 열, EN 열 한글 교체, AvailableCultures ko)
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/inject_translations.py \
  --gamepath "<게임루트>" --src <원본 resources.assets> --out <중간본1>

# 3-2. 언어 테이블 KO 열 추가 (TS_Cards 9열 / TS_Ingame·TS_Strings·Common_Ingame 8열 / TS_RulesTutorial 10열)
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/add_ko_columns.py \
  --gamepath "<게임루트>" --src <중간본1> --out <중간본2>

# 3-3. 씬 패치 (level1-3 하드코딩 문자열)
#      씬 구조가 바뀌었으면 먼저 analyze_scene_texts.py로 재매칭 확인
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/patch_scenes.py \
  --gamepath "<게임루트>"   # patched/level1-3 생성 (--src 인자 없음)

# 3-4. 폰트 주입 — 스킬 twilight-struggle-font-swap 4~6단계와 동일
#      (가상 폴더의 resources.assets를 <중간본2>로 교체 후 --parse → 매핑 → --list)

# 3-5. 검증
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/verify_assets.py \
  --orig <중간본2> --patched <font-output/resources.assets>
```

### 4. 구조 변경 시 검증 포인트 (업데이트가 에셋 구조를 바꿨다면)

| 포인트 | 확인 방법 | 실패 시 |
|---|---|---|
| 씬 MonoBehaviour 헤드 오프셋 (m_text @ head+56 TMP / +112 Text) | `patch_scenes.py` 실행 로그 — 변경 객체 수 0이면 의심 | 헤드 레이아웃 재실측 |
| KO 열 파서 (원본 존재 열 범위 내 배치, 27열 이상 금지) | `add_ko_columns.py` 검증 자동 실패 | 빈 열 번호 확인 후 재배치 |
| TextAsset 시트 구조 (행:열 JSON) | `scripts/extract_textassets.py <assets> --list` | 시트 키/열 구조 재파악 |
| 폰트 매핑 (24개 TMP → SDF 2종) | `--parse` 결과 JSON | `apply_font_mapping.py` 재실행 |
| 새 텍스트 키 | 미번역 `${Key}` UI 확인 | `translation/manual-*.json` 추가 → 3-1~3-2 재실행 |

### 5. 설치

```bash
# 백업 → 복사 → 해시 갱신 (macOS는 scripts/install.sh가 codesign 포함 처리)
sha256sum patched/*.assets patched/level1 patched/level2 patched/level3 > patched/hashes.txt
```

## 복구 (업데이트 전으로)

- Steam "파일 무결성 확인" → 원복 → 위 절차 재적용
- 또는 `backup-<date>/`에서 파일 복사

## 주의사항

- ⚠️ **Unity 버전 변경** 시 씬 직렬화 레이아웃이 바뀔 수 있음 — patch_scenes의 객체 변경 수(level1 883/level2 1391/level3 274)와 크게 다르면 중단하고 조사
- ⚠️ **새 문자열 추가 시**: EN 열 교체 → KO 열은 add_ko_columns가 EN 값 복사로 동기화 (순서: inject → add_ko 고정)
- ⚠️ 폰트 주입은 Windows에서만 가능 (exe) — macOS는 SDF 생성만
- ⚠️ 작업 전 `tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/Managed` 폴더 제거/이름변경 (Mono 오판 방지)
- 관련 문서: `docs/PROGRESS.md` (현재 상태/핸드오프), `docs/PLAN.md`, `docs/phases/phase-5-platform-test.md`
