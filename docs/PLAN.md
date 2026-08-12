# 황혼의 투쟁 (Twilight Struggle) 한글 패치 프로젝트 계획서

> Steam App ID: 406290 · 제작사: Playdek · 엔진: **Unity 6 (6000.0.58f2)**, IL2CPP
> 작성일: 2026-02 · 목표: 기존 (방치된) 한글 패치를 최신 게임 버전에서 다시 동작하게 만드는 것

---

## 1. 현황 요약 (탐색 결과)

### 게임 구조

| 항목 | 내용 |
| --- | --- |
| 설치 위치 (macOS) | `~/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data/` |
| 설치 위치 (Windows) | `steamapps/common/Twilight Struggle/TwilightStruggle_Data/` ✅ 실측 (2026-08-11, 공백 없음) |
| 엔진 | Unity **6000.0.58f2** (IL2CPP, `GameAssembly.dll` 35MB / dylib) |
| 텍스트 렌더링 | TextMeshPro SDF (TIMES, Anton, Bangers, atwriter 등 24개 폰트 → 한글 2종으로 교체 완료) |
| 전체 크기 | 약 416MB (패치 대상: resources.assets 108MB + level1~3 ~8.5MB) |

### 텍스트 소재별 난이도

> Phase 1·2·4·5 검증 결과 반영. Lua는 죽은 잔재 파일로 확인(작업 대상 아님).

| 소재 | 위치 | 상태 |
| --- | --- | --- |
| 다국어 문자열 테이블 | `resources.assets` 내 **Common_Strings** (키값 방식 `Key_XXX`, EN+11개 언어 열) | ✅ 실게임 반영 확인 + KO 열 주입 완료 (Phase 1·4) |
| 카드/국가 텍스트 | `resources.assets` 내 `TS_Cards` 등 TextAsset (`"행:열":"값"` JSON) | ✅ 실게임 반영 확인 + 주입 완료 (Phase 1·4) |
| 인게임/도움말 키 | `TS_Ingame`·`TS_Strings`·`Common_Ingame` | ✅ 실게임 반영 확인 + 주입 완료 (잔존 52키 수동 번역 포함) |
| **씬 하드코딩 문자열** | level1(메인 메뉴)·level2(인게임)·level3(보드) MonoBehaviour | ✅ 2,548개 한글화 (Phase 5 — `patch_scenes.py`) |
| 기존 번역 재사용 소스 | 블루칩 v1.0.1 `resources.assets` 내 **MonoBehaviour** string 필드 (432개 고유 한글 문자열) | ✅ 추출 가능 확인 (Phase 2) |
| **IL2CPP 코드 문자열** | `global-metadata.dat` (턴 히스토리 로그 템플릿: 'to attempt a Coup in' 등) | 🔴 파일 패치 불가 — BepInEx 런타임 훅 필요 (보류) |
| 카드/국가 Lua | `StreamingAssets/Lua/*.lua` | ❌ 죽은 잔재 (Phase 1 확인). 블루칩 Lua에는 번역 없음 |
| SDF 폰트 아틀라스 | `resources.assets` (CJK 글리프 없음 → 한글 네모 현상의 원인) | ✅ 해결 — 24개 폰트 한글 SDF로 교체 (Phase 3~4) |
| 텍스처에 구워진 텍스트 | 보드맵 국가명 등 | 🔴 어려움 (범위 제외) |

---

## 2. 기존 한글 패치 역사 (재사용 가능한 자산!)

| 패치 | 대상 버전 | 특징 | 상태 |
| --- | --- | --- | --- |
| 우드킹 (최초) | v1.1.3 | 첫 한글화 | 방치 |
| **블루칩** v1.0.1 | v1.4.2 → **v1.1.3 다운그레이드** | 100% 한글화, 멀티 불가 | [블로그](https://bluechip2022.tistory.com/2) |
| **블루칩** v2.0.1 | v1.4.2 | 멀티 가능, 그러나 메인화면·전적 UI·**오리지널 카드 미번역** (SDF 아틀라스가 CJK 미지원이라 TTF 폰트 쓰는 부분만 번역 가능했음) | 방치 |
| 한패(hanpe.net) 백업 | — | 제작자: 짜짜 | [hanpe.net/hanguls/t](https://hanpe.net/hanguls/t) |
| 일본어 패치 | 블루칩 v1.0 기반 | 이미지 문자는 번역 불가였음 | note.com/suraimuman1 |

### 방치된 원인 (Steam 토론에서 원 패치 제작자 본인이 설명)

1. **v1.4.x**: SDF 아틀라스 기반 폰트는 CJK 출력 불가 → TTF 폰트 부분만 번역 가능했음
2. **v1.4.6.154** (당시 최신): 모든 텍스트가 SDF 아틀라스로 전환되어 한글 출력 자체가 불가
3. v1.4.6부터는 텍스트가 **번역 키 방식**으로 바뀜: `resources.assets`의 `Common_Strings` 파일에 `Key_XXX` 항목이 언어별로 존재. 그러나 게임에 언어 선택 기능이 없고 한글 폰트가 없어서 영어만 출력
4. 그 이후 게임이 **Unity 6로 재빌드(rebuild)**됨 (현재 우리 설치본) → 기존 패치 완전 무력화

### 💡 핵심 기회 (달성됨)

- 블루칩 v1.0.1(100% 한글화)의 번역은 `resources.assets` 내 **MonoBehaviour**의 string 필드에 직접 주입돼 있음. UnityPy 고수준 `read()`는 IL2CPP 타입트리 불완전으로 실패하나, `get_raw_data()`에서 raw 바이트를 받아 Unity string 표준 레이아웃(`int32 len + bytes + pad4`)을 수동 파싱하면 **432개 고유 한글 문자열을 깨끗하게 추출 가능** (Phase 2 확인)
- 번역 재사용 전략: 런타임 패치(2026-03-15)의 `runtime_exact.tsv` 2,253쌍 + 수동 번역으로 TextAsset 666행·씬 2,548개 문자열 커버 (Phase 2·4·5). 블루칩 432개는 구버전 소스라 직접 매칭 불가 → 참고용
- `Common_Strings`의 한국어 슬롯은 **원본에 없음** (열 구조: `Key/EN/FR/DE/ES/PL/PT/JP/IT/RU/NL/CH`). 번역 주입 시 **EN 열 보존, RU(10열)을 한국어로 교체** (AGENTS.md 원칙 #8). 게임 언어 선택기 인식은 `AvailableCultures`에 ko 등록으로 해결 (Phase 4 검증)
- **언어=KO에서 카드/스코어링까지 한글이 되려면 모든 언어 테이블에 KO 열 추가 필수** — SmartLocalization이 언어별 열 헤더로 해석하며 KO 열이 없으면 `${Key}` 노출 (2차 테스트 확인). `scripts/add_ko_columns.py`로 TS_Cards·TS_Ingame·TS_Strings·Common_Ingame·TS_RulesTutorial에 KO 열 추가 (Common_Strings는 이미 10열)
- **게임 언어 설정은 별도 PlayerPrefs**(레지스트리 `localization_h2525087814`, macOS plist)로 관리됨 — KO로 설정해야 KO 열 로드 (Phase 5 확인). **설치 스크립트(`install-windows.ps1`/`install.sh`)가 자동으로 KO 설정**
- ~~"진짜 난제는 CJK 포함 SDF 폰트 아틀라스 주입"~~ → ✅ 해결 (Unity_Font_Replacer + 2048² SDF 2종, Phase 3~4)
- **남은 진짜 난제: IL2CPP 코드 문자열(턴 히스토리 로그)** — 모든 패치(블루칩·런타임 포함)가 미커버한 영역. BepInEx 런타임 훅으로만 가능

---

## 3. 작업 구조: 별도 Git 저장소 + 설치 스크립트 방식 (권장)

**Steam 폴더에서 직접 작업하지 않는다.** 이유:

- Steam "파일 무결성 확인" 시 수정 파일이 원본으로 복원됨
- 게임 자동 업데이트로 수정분이 날아감
- 원본 백업 없이는 되돌릴 수 없음
- 배포 가능한 패치 형태(파일 복사 + 스크립트)로 만들려면 처음부터 분리된 구조가 유리

### 저장소 구조 (제안)

```
~/Projects/twilight-struggle-kr-patch/
├── docs/
│   ├── PLAN.md                # 전체 계획
│   ├── PROGRESS.md            # 전체 진행 현황
│   └── phases/                # Phase별 상세 계획·검증·핸드오프
├── README.md                  # 사용자용 설치 안내
├── original/                  # 원본 파일 백업 (패치 대상 파일만 복사, .gitignore + 별도 보관)
├── patched/                   # 수정된 파일 (git 관리 대상)
│   ├── resources.assets       # 번역+폰트 주입본 (108MB, gitignore)
│   ├── sharedassets0.assets   # atwriter SDF 주입본 (gitignore)
│   ├── level1~3               # 씬 패치본 (git 관리)
│   └── hashes.txt             # SHA-256 기록
├── translation/               # 번역 소스 (JSON/CSV) — 실제 "소스코드"
│   ├── strings.json           # 키 → 한글 매핑
│   ├── cards.json
│   ├── runtime-20260315.json  # 런타임 패치 TSV (2,253쌍)
│   ├── manual-extra.json      # TextAsset 잔존 키 수동 번역
│   ├── manual-scenes.json     # 씬 하드코딩 문자열 수동 번역
│   └── schema.md              # 용어 통일표
├── fonts/                     # TTF 원본 + 생성된 SDF json/atlas
├── scripts/
│   ├── install.sh             # macOS 설치 (백업 → 복사 → codesign)
│   ├── inject_translations.py # TextAsset 번역 주입
│   ├── patch_scenes.py        # level1-3 씬 문자열 패치
│   ├── verify_assets.py       # m_Script/raw 무결성 검증
│   └── ...
└── tools/                     # UABEA 등 보조 도구 링크/메모
```

- `original/`은 부피가 크므로 git에 넣지 않고 로컬에만 보관 (`.gitignore`), 또는 Git LFS
- `patched/*.assets`도 108MB로 GitHub 100MB 제한을 초과하므로 gitignore — **배포는 `scripts/package-release.sh`의 dist/ zip으로** (압축 시 ~8MB, Releases 첨부 가능). `patched/level1~3`은 git 관리
- 설치 스크립트는 **멱등성** 있게: 재실행해도 안전, 업데이트 후 재적용 한 줄로 해결

---

## 4. Phase 개요

각 Phase의 세부 체크리스트, 검증 기준·결과, 결정 사항, 산출물 및 핸드오프는 해당 문서에서 관리한다. 이 문서에는 Phase 간 순서와 목표만 유지한다.

| Phase | 목표 | 예상 기간 | 상세 문서 |
| --- | --- | --- | --- |
| Phase 0 — 준비 | 저장소·도구·원본 백업·기존 패치 준비 | 0.5일 | [Phase 0](phases/phase-0-preparation.md) |
| Phase 1 — 텍스트 위치 검증 | 실게임에 반영되는 텍스트 소스 확정 | 1~2일 | [Phase 1](phases/phase-1-source-validation.md) |
| Phase 2 — 문자열 추출 & 번역 소스 구축 | 영문 추출 및 기존 번역을 키 기반 소스로 정리 | 2~3일 | [Phase 2](phases/phase-2-translation-source.md) |
| Phase 3 — 한글 SDF 폰트 아틀라스 생성 | CJK 글리프를 포함한 TMP 폰트 생성·주입 | 3~5일 | [Phase 3](phases/phase-3-sdf-font.md) |
| Phase 4 — 텍스트 주입 & 레이아웃 조정 | 재현 가능한 번역 주입과 UI 검증 | 1~2주 | [Phase 4](phases/phase-4-injection-layout.md) |
| Phase 5 — 플랫폼 적용 & 테스트 | macOS·Windows·멀티플레이 및 복구 검증 | 2~3일 | [Phase 5](phases/phase-5-platform-test.md) |
| Phase 6 — 배포 | 설치 안내·라이선스·배포물 정리 (zip 2종 패키징 스크립트 완료) | — | [Phase 6](phases/phase-6-release.md) |
| Phase 7 — 도움말/규칙 번역 (후순위) | TS_RulesTutorial 313행(6.4만 자) + 씬 규칙 문단 167개. **배포 후 맨 마지막에 수행** | 1~2일 | [Phase 7](phases/phase-7-help-translation.md) |

---

## 5. 플랫폼별 가이드

### macOS

| 작업 | 방법 |
| --- | --- |
| 데이터 경로 | `TwilightStruggle.app/Contents/Resources/Data/` |
| 코드 서명 | 애드혹 서명 가능 (개발자 계정 불필요): `codesign --force --sign - <앱 경로>`. 프레임워크/플러그인 손상 시 내부→외부 순서로 개별 서명 |
| Gatekeeper | Steam 설치 앱은 격리 속성이 보통 없음. 문제 시 `xattr -cr TwilightStruggle.app` |
| 도구 | UABEA(.NET 크로스플랫폼)·Python 스크립트 모두 macOS에서 실행 가능. 단 Unity_Font_Replacer의 **exe는 Windows 전용** → `make_sdf.py`(Python 원본) 사용 또는 Wine |

### Windows

| 작업 | 방법 |
| --- | --- |
| 데이터 경로 | `steamapps/common/Twilight Struggle/TwilightStruggle_Data/` ✅ 실측 (2026-08-11, 공백 없음) |
| 코드 서명 | 불필요 |
| 도구 | 모든 Windows exe 그대로 사용 가능 |

### 공통

- 에셋 파일(`resources.assets` 등)은 데스크톱 양 플랫폼에서 보통 동일 빌드 산출물 → **맥에서 만든 수정 파일을 윈도우에도 그대로 복사 가능** (게임 버전만 일치하면)
- `GameAssembly.dylib`(mac)과 `.dll`(win)은 호환 불가 — 다만 이 패치는 바이너리를 안 건드리는 것이 목표

---

## 6. Edge Cases & 리스크

| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| Steam 무결성 확인/자동 업데이트로 파일 원복 | 패치 소멸 | 설치 스크립트로 즉시 재적용. `boot.config`의 build-guid 또는 파일 해시로 버전 감지, 불일치 시 경고 |
| Lua 파일이 실제로 안 쓰임 (잔재 파일) | 작업 무효 | Phase 1에서 반드시 실게임 반영 테스트 후 착수 |
| Unity 6 직렬화 포맷 변경으로 도구 파싱 실패 | 에셋 편집 불가 | UABEANext / AssetRipper 대안. 최후 수단: Unity Editor로 프로젝트 재구성 후 AssetBundle 주입 (XUnity.AutoTranslator 방식) |
| SDF 아틀라스 용량 부족 | 글자 누락(□) | 사용 글자 기반 문자셋(739자) + **2048²** (실측: 596→739자 기준 충분, 4096² 시 397MB), 필요 시 아틀라스 2개로 분할. 폰트 에셋의 fallback 체인 활용 |
| 폰트 교체 후 아웃라인/그림자 스타일 깨짐 | 시각 품질 | Material 파라미터(`_OutlineWidth`, `_GradientScale`)를 원본 padding 기준으로 보정 (Unity_Font_Replacer가 자동 보정 기능 보유) |
| OFL Reserved Font Name | 라이선스 위반 가능성 | 폰트 파일 자체를 수정·개명 재배포 시 Reserved Name 회피. 단순 번들·사용은 문제없음. 라이선스 전문 동봉 |
| 멀티플레이 버전 체크 | 온라인 불가 | v1.4.2 시절 v2.0 패치가 멀티를 유지한 전례 있음. 에셋만 교체 시 유지될 가능성 높으나 반드시 테스트 |
| 텍스처 구워진 영문 | 일부 영문 잔존 | 기존 패치들도 미해결. 1차 범위 제외, 이미지 리터칭은 후속 과제로 |
| IL2CPP 내 하드코딩 문자열 (턴 히스토리 등) | 일부 UI 영어 잔존 — **현실화됨** | 파일 패치는 길이 제약으로 불가. BepInEx 런타임 훅이 현실적 (기존 런타임 패치도 미커버 확인, 보류) |
| **UnityPy 저장 시 같은 경로 금지** | 저장 파일 손상 (EOFError) | 로드 파일과 저장 파일 분리 (`.work` → 별도 출력) — `patch_scenes.py` 참조 |
| 게임 언어가 EN으로 고정됨 | 메뉴 영어 표시 | 설치 스크립트가 자동 설정 (레지스트리/plist `localization_*` = KO). ⚠️ **게임 내 언어 선택 UI는 없음** (2026-08-12 실측) — PlayerPrefs 값 변경으로만 설정 가능. 제거 시 uninstall 스크립트가 이전 언어로 복원 |

---

## 7. 도구 총정리

| 도구 | 용도 | 링크/비고 |
| --- | --- | --- |
| **UABEA** | 에셋 추출/수정/재삽입 (크로스플랫폼) | github.com/nesrak1/UABEA |
| UABEANext | UABEA 대안 (IL2CPP 게임에 유리하다는 보고) | nesrak1 레포 참고 |
| AssetRipper / AssetStudio | 읽기 전용 에셋 분석 | github.com/AssetRipper/AssetRipper |
| **Unity_Font_Replacer** | 한글 SDF 아틀라스 포함, 폰트 교체/추출, `make_sdf.py`(Unity 없이 SDF 생성) | github.com/snowyegret23/Unity_Font_Replacer |
| XUnity.AutoTranslator | 폰트 번들 주입 가이드(참고), 런타임 텍스트 후킹 대안 | 위키에 Font Asset 패키징 가이드 |
| Cpp2IL / Il2CppDumper | IL2CPP 바이너리 분석 (필요 시에만) | |
| Unity Editor 6000.0.58f2 | Font Asset Creator (선택지 B) | Unity Hub |

### 폰트 (모두 재배포 허용 라이선스 — 2026-08-12 확정)

- **D2Coding Regular** (SIL OFL 1.1) — 본문/TIMES 계열 대체 (기존: Noto Serif KR)
- **Paperlogy 5 Medium** (SIL OFL 1.1) — 제목/Anton 계열 대체 (기존: Black Han Sans)
- SDF 생성·크기 조절: `make_sdf.py` + m_PointSize 수정 (폰트 교체/크기 조절은 스킬 참조)

---

## 8. 참고 자료

- 블루칩 한글 패치 v1.0.1/v2.0.1: <https://bluechip2022.tistory.com/2>
- 한패 백업 목록: <https://hanpe.net/hanguls/t> (Twilight Struggle 항목)
- 일본어화 패치(블루칩 기반): <https://note.com/suraimuman1/n/n49419b1f24f3>
- Steam 토론 (패치 제작자의 기술 설명, v1.4.6 구조): steamcommunity.com/app/406290 토론 "Spanish translation?" 스레드
- XUnity.AutoTranslator 폰트 번들 가이드: github.com/bbepis/XUnity.AutoTranslator/wiki

---

## 실행 기준

현재 상태와 다음 작업은 [`docs/PROGRESS.md`](PROGRESS.md)를 기준으로 확인한다. 작업을 재개할 때는 다음 순서를 따른다.

1. `docs/PROGRESS.md`에서 현재 Phase와 핸드오프를 확인한다.
2. 해당 Phase 문서의 체크리스트와 검증 기준을 먼저 읽는다.
3. 작업 결과와 근거를 Phase 문서에 기록한 뒤 다음 Phase로 진행한다.
