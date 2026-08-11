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

## 체크리스트

- [x] Windows 실게임 테스트 (1차) — 한글 출력 확인, 문제 진단
- [x] 게임 언어 설정 KO 전환 (레지스트리)
- [x] TS_Ingame/TS_Strings 잔존 키 수동 번역 + 재주입 (53키)
- [x] 씬 패치 (level1-3) — 하드코딩 문자열 2,548개 한글화
- [ ] **게임 재실행 테스트** — 메뉴 한글화 확인, 잔존 `□`/영어 확인
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
| 게임 재실행 | — | ⬜ 대기 |

## 다음 Phase로 핸드오프

- **테스트 대기**: 게임 재실행 → 메뉴 한글화 + 잔존 이슈 확인 (Player.log의 `Load Language Header` 값도 확인)
- **알려진 잔존 영어**: 턴 히스토리(IL2CPP 코드 문자열) — BepInEx 런타임 훅으로만 해결 가능, 별도 판단
- **Windows 설치 스크립트 미작성**: `scripts/install-windows.ps1` 필요 (backup → 복사 → 검증)
- **배포 포함 파일**: `patched/resources.assets`, `patched/sharedassets0.assets`, `patched/level1~3`, `fonts/`, 설치 스크립트
