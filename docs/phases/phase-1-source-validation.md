# Phase 1 — 텍스트 위치 검증

## 상태

- 상태: ✅ 완료
- 완료일: 2026-08-05
- 관련 커밋: `d135d1b`

## 목표

Unity 6로 변경된 현재 게임에서 실제로 화면에 반영되는 텍스트 소스를 실게임 실험으로 확정한다. 죽은 잔재 파일에 번역을 주입하는 일을 방지하는 것이 핵심이다.

## 체크리스트

- [x] 실험 A: Lua 카드 이름 변경
- [x] 실험 C: Lua 로드 경로 및 바이너리 참조 확인
- [x] 실험 B: `Common_Strings` 및 `TS_Cards` 수정
- [x] 실게임 반영 여부 확인
- [x] 주 작업 대상 확정

## 검증 기준

| 검증 항목 | 성공 기준 |
|---|---|
| Lua 소스 | 카드 이름 변경이 게임 화면에 표시됨 |
| `Common_Strings` | 메뉴 문자열 변경이 게임 화면에 표시됨 |
| `TS_Cards` | 카드 이름 변경이 게임 화면에 표시됨 |
| 한글 주입 | 인코딩이 깨지지 않고 폰트 렌더링 문제와 구분됨 |

## 실행 결과

| 항목 | 방법 | 결과 | 근거 |
|---|---|---|---|
| 실험 A | `twilight_cards.lua`의 `Asia Scoring`을 테스트 문자열로 변경 후 실행 | ❌ 실패 | 게임에 `Asia Scoring` 그대로 표시 |
| 실험 C | `LoadLuaFile`/`twilight/database`를 GameAssembly.dylib·에셋·global-metadata에서 검색 | ❌ 실패 | 관련 참조 0건. Lua는 죽은 잔재 파일로 판단 |
| UnityPy 파싱 | `resources.assets` TextAsset 추출 | ✅ 성공 | 오브젝트 42,653개 파싱 |
| `Common_Strings` | `Key_PlayOffline` EN 값 변경 후 실행 | ✅ 성공 | 메뉴 문구 변경 확인 |
| `TS_Cards` | `Asia Scoring` 카드 이름 변경 후 실행 | ✅ 성공 | 카드 이름 변경 확인 |
| 한글 렌더링 | 테스트 문자열을 한글로 주입 후 실행 | ⚠️ 부분 성공 | 주입·인코딩은 정상이나 SDF CJK 글리프 부재로 `ㅁ` 표시 |

## 발견된 에셋 구조

`resources.assets`에서 TextAsset 18개를 확인했다.

- `Common_Strings`: 약 200KB, 323행. 열은 `Key/EN/FR/DE/ES/PL/PT/JP/IT/RU/NL/CH`
- `TS_Cards`: 약 162KB
- `TS_Strings`
- `TS_Ingame`
- `TS_RulesTutorial`: 약 195KB

문자열은 스프레드시트형 JSON이며, `행:열` 키 구조를 사용한다. 첫 줄에는 날짜 헤더가 있을 수 있으므로 치환 시 JSON 본문만 다룬다.

## 검증된 파이프라인

- 탐색·덤프(읽기 전용): `tools/asset-tool` (.NET, AssetsTools.NET) — 에셋 구조 파악·TextAsset 본문 추출
- 주입(수정): UnityPy + `scripts/patch_textasset.py` (2026-08-12 정리로 삭제됨 — 현재는 `scripts/inject_translations.py` 사용)
- 적용: `scripts/install-asset-test.sh` 패턴 — 해시 검증 후 복사, 멱등 실행 (2026-08-12 삭제됨 — 현재는 `scripts/install.sh`·`install-windows.ps1` 사용)
- 복원: `scripts/restore-original.sh`

⚠️ UnityPy가 저장한 파일을 다시 읽어 재저장하면 데이터가 유실될 수 있다. 항상 원본에서 한 번에 모든 치환을 적용한다.

## 산출물

- 텍스트 덤프: `tools/dump/*.txt` (git 제외, 재생성 가능)
- 에셋 탐색·덤프 도구: `tools/asset-tool/` (.NET, AssetsTools.NET 기반 — 읽기 전용. `tools/README.md` 참고)
- TextAsset 수정 도구: ~~`scripts/patch_textasset.py`~~ → 삭제됨 (2026-08-12, `inject_translations.py`로 대체)
- 테스트 적용 스크립트: ~~`scripts/install-asset-test.sh`~~ → 삭제됨 (2026-08-12)
- 원본 백업: `original/`
- 기존 패치: `tools/legacy-patches/v1.0.1/`, `tools/legacy-patches/v2.0.1/`

## 다음 Phase로 핸드오프

### 수신 Phase

- Phase 2 — 문자열 추출 & 번역 소스 구축

### 반드시 알아야 할 사실

- 실제 텍스트 소스는 `resources.assets` 내 TextAsset다.
- `Common_Strings`와 `TS_Cards`는 실게임 반영이 확인됐다.
- `StreamingAssets/Lua`는 죽은 코드이므로 번역 주입 대상이 아니다.
- 한글 주입과 UTF-8 인코딩은 정상이다. 현재 `ㅁ` 현상은 SDF 폰트에 CJK 글리프가 없기 때문이다.

### 즉시 실행할 작업

1. `scripts/restore-original.sh`로 게임 테스트 상태를 복원한다.
2. `Common_Strings`, `TS_Cards`의 영문 문자열 전체를 추출해 `translation/` JSON으로 정리한다.
3. 기존 블루칩 패치에서 한글 번역을 추출하고 현재 문자열과 자동 매칭한다.
4. `TS_Ingame`, `TS_Strings`, `TS_RulesTutorial`, `Common_Ingame`의 실제 사용 여부를 함께 확인한다.

### 사용해야 하는 도구와 주의점

- UnityPy와 `scripts/patch_textasset.py`를 사용한다. (2026-08-12 삭제됨 — 현재는 `scripts/inject_translations.py` + `scripts/add_ko_columns.py`)
- 테스트용 `patched/resources.assets`는 원본에서 재생성하거나 폐기한다.
- `tools/dump/*.txt`는 git 제외 산출물이므로 필요하면 UnityPy로 재생성한다.

### 미해결 이슈

- 기타 TextAsset의 실제 사용 여부 미검증
- 기존 패치와 현재 버전의 문자열 차이 및 매칭률 미확인
- CJK SDF 아틀라스 생성·주입은 Phase 3에서 처리
