# Phase 5 — 플랫폼 적용 & 테스트

## 상태

- 상태: 🚧 진행 중 (Windows 테스트 1차 완료, 씬 패치 적용 완료)
- 선행 Phase: Phase 4 완료

## Windows 실게임 테스트 (2026-08-11) — 결과 기록

### ✅ 확인된 것

- 한글 폰트 주입 정상 — 카드/인게임 대부분 한글 출력 확인
- `Common_Strings` KO 열 + `AvailableCultures` ko 등록 정상

### ❌ 발견된 문제와 진단

| 문제 | 원인 | 해결 |
|---|---|---|
| 메인 메뉴/설정이 영어 | **게임 언어 설정이 EN** — PlayerPrefs `localization_h2525087814 = 'EN'` (Player.log: `Load Language Header: EN`) | 레지스트리에서 KO로 변경 완료 |
| 메뉴 일부 하드코딩 영어 | level1/level2의 TextMeshProUGUI.m_text / Text.m_Text — MonoBehaviour 직렬화 문자열 | **씬 패치 완료** (아래) |
| 인게임 잔존 영어 (Current Turn 등) | TS_Ingame/TS_Strings 미번역 키 53개 | **수동 번역 + 재주입 완료** (Phase 4 갱신) |
| 턴 히스토리(하단) 영어 | IL2CPP 코드 문자열 템플릿 (global-metadata.dat) — 'to attempt a Coup in' 등. 기존 런타임 패치도 미커버 | 🔴 별도 프로젝트 (BepInEx 런타임 훅) 필요 — 보류 |

### 게임 텍스트 3계층 구조 (확정)

1. **Common_Strings/TS_Ingame 등 TextAsset** — `${Key_XXX}` 키 참조. 언어=ko일 때 KO 열 사용 → **번역 주입 + 언어 설정으로 해결**
2. **씬 하드코딩 문자열** — level1(메인 메뉴)·level2(인게임)·level3(보드)의 MonoBehaviour 직렬화. 언어와 무관하게 영어 고정 → **씬 패치로 해결**
3. **IL2CPP 코드 문자열** — global-metadata.dat의 C# 리터럴. 턴 히스토리 로그 템플릿 등 → 메타데이터 패치는 길이 제약, **BepInEx 런타임 훅이 현실적**

## 씬 패치 (2026-08-11 완료)

### 방법

- Unity 6 MonoBehaviour 헤드 레이아웃 실측: `m_GameObject(12B) + m_Enabled(1B)+pad(3B) + m_Script(12B) + m_Name(string)`
- TextMeshProUGUI: `m_text` @ head_end+56 / Text: `m_Text` @ head_end+112 (고정 오프셋 확인)
- raw blob 재구성: `head + 새 m_text + 나머지` — m_Script 참조 무변경
- 번역 소스: 런타임 TSV(정확 + 개행/공백 정규화 매칭) + `translation/manual-scenes.json`(수동 206개)
- `${...}` 키 참조 문자열·이미 한글·더미/숫자·규칙본문은 제외

### 검증 결과

| 항목 | 결과 |
|---|---|
| level1(메인 메뉴) | ✅ 883개 객체 변경 (raw 변경 874, 전부 텍스트 객체) |
| level2(인게임) | ✅ 1,391개 객체 변경 |
| level3(보드) | ✅ 274개 객체 변경 |
| m_Script 무손상 | ✅ 0건 불일치 (3개 레벨 전부) |
| 비텍스트 raw 변경 | ✅ 0건 |
| 샘플 확인 | ✅ '오프라인 플레이'/'설정'/'현재 턴:'/'우주 경쟁' 등 전부 확인 |

### ⚠️ 저장 트러블슈팅 (재현 시 참고)

- 같은 파일 경로에 `env.file.save()` 하면 지연 스트리밍(Replacer)이 깨져 `EOFError: Unexpected EOF while streaming source slice`
- **로드 파일 ≠ 저장 파일**이어야 함 (`.work` 복사본 로드 → 별도 출력 파일 저장)

### 재실행 방법

```bash
python scripts/patch_scenes.py --gamepath <게임루트>            # patched/level1-3 생성
python scripts/patch_scenes.py --gamepath <게임루트> --apply    # 백업 후 Steam에 적용
```

## 언어 설정 (Step 1 — 레지스트리로 해결)

- Unity PlayerPrefs 위치: `HKCU\Software\Playdek\TwilightStruggle`
- 키: `localization_h2525087814` — `EN` → `KO`로 변경 완료 (2026-08-11)
- 게임 설정 → Languages 에서도 선택 가능 (AvailableCultures에 ko 등록됨)
- **검증**: 게임 실행 후 Player.log에 `Load Language Header: KO`가 찍히는지 확인

## 게임 재실행 테스트 (2차, 2026-08-12) — 문제 3건 발견·해결

사용자 테스트 결과 (언어=KO):
- ✅ 메인 메뉴/설정 한글화 확인 (Common_Strings KO 열 정상)
- ✅ 인게임 UI(플레이어패/버리기/제거됨/다음 프로젝트) 한글화
- ✅ 게임판 국가명 대부분 한글

| 문제 | 원인 | 해결 | 상태 |
|---|---|---|---|
| 1. 국가명 일부 □ (튀니지→ㅁ니지, 케냐→케ㅁ, 콜롬비아→ㅁㅁ비아 등) | SDF chars.txt에 누락 한글 104자 (튀/콰/콜/롬/냐/룬 등) | chars.txt 확장 (596→739자) + SDF 재생성 | ✅ 재주입 완료 |
| 2. Scoring UI에 ${Panel:ScoringB/...} 키 노출 | 언어=KO에서 SmartLocalization이 각 테이블의 **KO 헤더 열**을 찾는데 TS_Ingame 등에 KO 열 없음 | **모든 언어 테이블에 KO 열 추가** (아래) | ✅ 재주입 완료 |
| 3. **카드 텍스트 전부 ${XXXXX} 키 노출** | 동일 — 카드 키(Card_*)는 TS_Cards(EN=2열)에만 있고 KO 열 없음. EN 상태에서는 EN 열(한글 교체분)을 읽어 한글이었음 | TS_Cards에 KO 열 추가 | ✅ 재주입 완료 |

### 근본 원인 (조사 확정)

- 씬의 UI 텍스트는 `${Card_*}`, `${Panel_*}`, `${Help_*}`, `${Key_*}` 키 문자열로 저장되고 **런타임에 SmartLocalization이 해석**
- `Common_Strings`만 KO 열(10열) 주입 → 메뉴 한글화 성공. 나머지 테이블은 EN 열(2~3열)에 한글을 넣었을 뿐 KO 열이 없어 **KO 언어에서 키가 그대로 노출**
- 2차 시도: 26/27열(원본 범위 밖)에 KO 열 추가 → **게임 파서가 무시** (3차 테스트에서 키 노출 지속 확인)
- 3차 시도(최종): **원본 존재 열 범위 내 빈 열에 배치** — TS_Cards 9열, TS_Ingame/TS_Strings/Common_Ingame 8열, TS_RulesTutorial 10열 → 재주입 완료 (2026-08-12)
- 해결 도구: `scripts/add_ko_columns.py` (기존 잘못된 KO 열 자동 제거 후 재배치, 1열 키 열 제외)

| 테이블 | 시트 | KO 열 | 복사 행 |
|---|---|---|---|
| TS_Cards | 1631793870 | **9** (처음 26 → 무시됨) | 344 |
| TS_Ingame | 0 | **8** (처음 27 → 무시됨) | 157 |
| TS_Strings | 0 | **8** (처음 27 → 무시됨) | 50 |
| Common_Ingame | 0 | **8** (처음 27 → 무시됨) | 22 |
| TS_RulesTutorial | 1631793870 / 1022388242 | **10** (처음 27 → 무시됨) | 313 / 0 |

⚠️ TS_Ingame 등은 시트 키가 `"0"`이므로 설명 시트로 오판하면 안 됨 (EN 열 유무로 판별)
⚠️ **KO 열은 "헤더 행에 이미 존재하는 열" 중 빈(null) 열에 배치해야 함** — 원본에 없는 열 번호(27열)에 셀을 추가하면 게임 파서가 무시함 (2026-08-12 3차 테스트에서 확인). 모든 테이블은 원본부터 26열까지 셀을 보유.
⚠️ **1열은 키 열 — KO 후보에서 제외 필수** (TS_Cards·TS_Strings는 1행 1열이 null이라 자동 선택되면 키가 파괴됨)

### SDF 재생성 (문자셋 739자)

- `fonts/chars.txt`: 596→739자 (누락 한글 104자 + ASCII/특수 보강)
- 문자셋 출처: 패치 후 표시 문자열 전체 (TextAsset 전 테이블 + level1~3 씬 문자열)
- NotoSerifKR: point-size 74→**70** (atlas 2048² 한계, padding 7→4) — 화면 표시 크기는 faceInfo 기반이라 동일, 아틀라스 해상도만 소폭 감소
- BlackHanSans-Regular: 87→**83** (동일 이유)
- 폰트 재주입: Unity_Font_Replacer 재실행 (47항목 매핑 재설정 — parse가 JSON 초기화하므로 주의)
- 검증: m_Script 0건 불일치, TextAsset 변경 0건 (KO 열 유지), 폰트/텍스처 69건 변경
- Steam 설치 완료 (백업: backup-20260811/resources.assets.20260812-pre-ko)

- [x] Windows 실게임 테스트 (1차) — 한글 출력 확인, 문제 진단
- [x] 게임 언어 설정 KO 전환 (레지스트리)
- [x] TS_Ingame/TS_Strings 잔존 키 수동 번역 + 재주입 (53키)
- [x] 씬 패치 (level1-3) — 하드코딩 문자열 2,548개 한글화
- [ ] **게임 재실행 테스트** — 메뉴 한글화 확인, 잔존 `□`/영어 확인
- [ ] macOS 설치 스크립트 검증 (`scripts/install.sh`)
- [ ] Windows 설치 스크립트 (`scripts/install-windows.ps1`) 작성
- [ ] 멀티플레이 동작 테스트
- [ ] Steam 무결성 확인 후 재설치 테스트

## 체크리스트

- [x] Windows 실게임 테스트 (1차) — 한글 출력 확인, 문제 진단
- [x] 게임 언어 설정 KO 전환 (레지스트리)
- [x] TS_Ingame/TS_Strings 잔존 키 수동 번역 + 재주입 (53키)
- [x] 씬 패치 (level1-3) — 하드코딩 문자열 2,548개 한글화
- [x] 2차 테스트 후속 조치 — KO 열 추가(5테이블) + SDF 문자셋 확장 재주입 (2026-08-12)
- [x] 3차 테스트 후속 — KO 열 원본 범위 내 배치(8/9/10열) 재주입 (2026-08-12)
- [ ] **게임 재실행 테스트 (4차)** — 카드/스코어링/HELP/우주 경쟁/DEFCON 확인
- [ ] macOS 설치 스크립트 검증 (`scripts/install.sh`)
- [ ] Windows 설치 스크립트 (`scripts/install-windows.ps1`) 작성
- [ ] 멀티플레이 동작 테스트
- [ ] Steam 무결성 확인 후 재설치 테스트

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| macOS | 설치 후 재서명된 게임이 실행됨 |
| Windows | 동일 에셋으로 게임이 실행됨 |
| 메뉴 한글화 | 언어=KO에서 메인 메뉴/설정이 한글 표시 |
| 멀티플레이 | 패치 후 온라인 기능이 정상 동작함 |
| 복구 | 원본 복원 또는 Steam 검증 후 패치를 재적용할 수 있음 |
| 멱등성 | 설치 스크립트를 반복 실행해도 손상되지 않음 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| 번역 재주입 (TS_Ingame 등) | `inject_translations.py` + verify | ✅ 성공 — 40+12행, m_Script 0건 불일치 |
| 폰트 재주입 | Unity_Font_Replacer `--list` | ✅ 성공 — TextAsset 2개만 변경 |
| 씬 패치 | `patch_scenes.py` + raw 비교 | ✅ 성공 — m_Script 0건, 비텍스트 변경 0건 |
| 언어 설정 | 레지스트리 `localization_*` | ✅ KO 설정 완료 |
| 게임 재실행 | — | ⬜ 대기 (3차 — KO 열 위치 수정 재주입 완료) |
| 카드/스코어링 키 노출 | KO 열 존재 확인 (add_ko_columns.py 검증) | ⚠️ 27열 추가 실패 → ✅ 8/9/10열 재배치 완료, m_Script 0건 |
| 국가명 □ | chars.txt 확장 + SDF 재생성 | ✅ 성공 — 739자, point-size 70/83 |

## 다음 Phase로 핸드오프

### 즉시 실행할 작업 (순서대로)

1. **게임 재실행 테스트** (Windows) — 메뉴/설정/로비 한글화 확인
   - 언어=KO가 이미 레지스트리에 적용됨 (`localization_h2525087814`)
   - Player.log에 `Load Language Header: KO`가 찍히는지 확인 (LocalLow\Playdek\TwilightStruggle\Player.log)
2. **잔존 이슈 수집** — 영어 잔존 UI / `□` 누락 글자 확인
   - 영어 잔존 → `translation/manual-scenes.json`(씬)·`manual-extra.json`(TextAsset)에 키 추가
   - `□` → `fonts/chars.txt`에 글자 추가 → make_sdf.py 재생성 → 폰트 재주입 (Runbook 참조)
3. **macOS 적용** — `patched/` 전송 (resources.assets 108MB + sharedassets0.assets + level1~3) → `scripts/install.sh`
   - macOS 코드사인은 install.sh가 자동 처리 (`codesign --force --sign -`)
4. **Windows 설치 스크립트 작성** — `scripts/install-windows.ps1` (백업 → 복사 → 해시 검증) — 체크리스트 잔여 항목
5. **멀티플레이 테스트** — 패치 후 온라인 기능 정상 동작 확인 (미실시)
6. **Steam 무결성 확인 후 재설치 테스트** — 복구 절차 검증

### 결정 사항 요약

- 게임 언어는 레지스트리 PlayerPrefs로 관리 — 패치에 언어 설정이 포함되지 않으므로 설치 안내에 명시 필요
- 씬 패치는 `patch_scenes.py`로 재현 가능 (번역 소스만 추가하면 재실행)
- 폰트 재주입은 Windows에서만 가능 (Unity_Font_Replacer exe) — macOS는 SDF 생성만 가능

### 미해결 이슈 (보류)

- **턴 히스토리 로그** — IL2CPP 코드 문자열(global-metadata.dat)로 파일 패치 불가. BepInEx 런타임 훅 프로젝트로만 해결 가능 (블루칩·런타임 패치 포함 모든 기존 패치가 미커버)
- **폰트 크기 불일치** — 24개 원본 폰트 → 한글 2종 통일로 크기/줄 간격 차이. `--use-game-line-metrics` 재주입 또는 m_FaceInfo(m_PointSize/m_Scale/m_LineHeight) 배율 조정으로 보정 가능 (미적용)
- **규칙북/튜토리얼 긴 문단** — 씬 하드코딩 167개 미번역 (번역량 대비 우선순위 낮음, TS_RulesTutorial 제외 결정과 일관)
- **더미 텍스트** — 'PlayerName12345', 'Text goes here' 등 개발용 더미는 번역 제외 (무해)

### 산출물 위치

- `patched/` — resources.assets, sharedassets0.assets, level1~3, hashes.txt
- `translation/manual-extra.json`, `translation/manual-scenes.json` — 수동 번역 소스
- `scripts/patch_scenes.py`, `scripts/analyze_scene_texts.py` — 씬 패치 도구
- Steam 설치본 백업: `TwilightStruggle_Data/backup-20260811/`
