# 황혼의 투쟁 (Twilight Struggle) 한글 패치 프로젝트 계획서

> Steam App ID: 406290 · 제작사: Playdek · 엔진: **Unity 6 (6000.0.58f2)**, IL2CPP
> 작성일: 2026-02 · 목표: 기존 (방치된) 한글 패치를 최신 게임 버전에서 다시 동작하게 만드는 것

---

## 1. 현황 요약 (탐색 결과)

### 게임 구조
| 항목 | 내용 |
|---|---|
| 설치 위치 (macOS) | `~/Library/Application Support/Steam/steamapps/common/Twilight Struggle/TwilightStruggle.app/Contents/Resources/Data/` |
| 설치 위치 (Windows) | `steamapps/common/Twilight Struggle/Twilight Struggle_Data/` (예상 — 설치 후 확인 필요) |
| 엔진 | Unity **6000.0.58f2** (IL2CPP, `GameAssembly.dylib` 82MB) |
| 텍스트 렌더링 | TextMeshPro SDF (`TIMESI SDF`=Times New Roman, Anton, Bangers, atwriter 등) |
| 전체 크기 | 약 416MB (패치 대상 에셋만 추출하면 수십 MB 수준) |

### 텍스트 소재별 난이도
| 소재 | 위치 | 난이도 |
|---|---|---|
| 카드/국가 텍스트 (Lua) | `StreamingAssets/Lua/*.lua` (평문, 약 6,500줄) | 🟢 쉬움 |
| 카드 텍스트 (TextAsset) | `resources.assets` 내 `TS_Cards` 등 (구버전 방식, 잔존 여부 확인 필요) | 🟡 |
| UI/튜토리얼/규칙 텍스트 | `resources.assets`, `level0~3` 씬 파일 (TMP 리치텍스트) | 🟡 중간 |
| **다국어 문자열 테이블** | `resources.assets` 내 **Common_Strings** (번호 약 739, 키값 방식: `Key_PlayOffline` 등. 다국어 번역 포함돼 있으나 영어로만 출력된다는 제보 있음) | 🟢 **최우선 확인 대상** |
| SDF 폰트 아틀라스 | `resources.assets` (CJK 글리프 없음 → 한글 네모 현상의 원인) | 🔴 핵심 장벽 |
| 텍스처에 구워진 텍스트 | 보드맵 국가명 등 | 🔴 어려움 (기존 패치도 미번역) |

---

## 2. 기존 한글 패치 역사 (재사용 가능한 자산!)

| 패치 | 대상 버전 | 특징 | 상태 |
|---|---|---|---|
| 우드킹 (최초) | v1.1.3 | 첫 한글화 | 방치 |
| **블루칩** v1.0.1 | v1.4.2 → **v1.1.3 다운그레이드** | 100% 한글화, 멀티 불가 | [블로그](https://bluechip2022.tistory.com/2) |
| **블루칩** v2.0.1 | v1.4.2 | 멀티 가능, 그러나 메인화면·전적 UI·**오리지널 카드 미번역** (SDF 아틀라스가 CJK 미지원이라 TTF 폰트 쓰는 부분만 번역 가능했음) | 방치 |
| 한패(hanpe.net) 백업 | — | 제작자: 짜짜 | [hanpe.net/hanguls/t](https://hanpe.net/hanguls/t) |
| 일본어 패치 | 블루칩 v1.0 기반 | 이미지 문자는 번역 불가였음 | note.com/suraimuman1 |

### 방치된 원인 (Steam 토론에서 원 패치 제작자 본인이 설명)
1. **v1.4.x**: SDF 아틀라스 기반 폰트는 CJK 출력 불가 → TTF 폰트 부분만 번역 가능했음
2. **v1.4.6.154** (당시 최신): 모든 텍스트가 SDF 아틀라스로 전환되어 한글 출력 자체가 불가
3. v1.4.6부터는 텍스트가 **번역 키 방식**으로 바뀜: `resources.assets`의 `Common_Strings` 파일에 `Key_XXX` 항목이 언어별로 존재. 그러나 게임에 언어 선택 기능이 없고 한글 폰트가 없어서 영어만 출력
4. 그 이후 게임이 **Unity 6로 리빌드**됨 (현재 우리 설치본) → 기존 패치 완전 무력화

### 💡 핵심 기회
- 기존 패치에 **95% 완성된 번역문**이 이미 있음 → 처음부터 번역할 필요 없음. 옛 패치 파일에서 번역 텍스트를 추출해 재사용
- v1.4.6+의 `Common_Strings` 다국어 테이블에 한국어 슬롯이 이미 존재할 가능성 → 게임 코드(언어 설정)만 건드리면 되는 구조일 수 있음
- 우리가 풀어야 할 **진짜 난제는 "CJK 포함 SDF 폰트 아틀라스 주입"** 한 가지로 수렴

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
├── PLAN.md                    # 이 문서
├── README.md                  # 사용자용 설치 안내
├── original/                  # 원본 파일 백업 (패치 대상 파일만 복사, .gitignore + 별도 보관)
├── patched/                   # 수정된 파일 (git 관리 대상)
│   ├── StreamingAssets/Lua/*.lua
│   ├── resources.assets
│   └── ...
├── translation/               # 번역 소스 (JSON/CSV) — 실제 "소스코드"
│   ├── strings.json           # 키 → 한글 매핑
│   ├── cards.json
│   └── glossary.md            # 용어 통일표
├── fonts/                     # TTF 원본 + 생성된 SDF json/atlas
├── scripts/
│   ├── install-mac.sh         # 백업 → 복사 → codesign 재서명
│   ├── install-windows.ps1
│   ├── uninstall-mac.sh
│   ├── uninstall-windows.ps1
│   └── verify.sh              # 게임 버전/파일 해시 확인 (버전 불일치 시 경고)
└── tools/                     # UABEA 등 보조 도구 링크/메모
```

- `original/`은 부피가 크므로 git에 넣지 않고 로컬에만 보관 (`.gitignore`), 또는 Git LFS
- `patched/resources.assets`도 크므로(14MB) git에 넣되, `.resS`(74MB) 파일은 수정 불필요할 가능성이 높음 — 건드릴 경우에만 LFS
- 설치 스크립트는 **멱등성** 있게: 재실행해도 안전, 업데이트 후 재적용 한 줄로 해결

---

## 4. 단계별 실행 계획

### Phase 0 — 준비 (0.5일)
- [ ] Git 저장소 초기화 (`~/Projects/twilight-struggle-kr-patch`)
- [ ] 기존 패치 파일 확보: 블루칩 블로그 v1.0.1/v2.0.1 + 한패 백업 다운로드
- [ ] 도구 설치:
  - **UABEA** (nesrak1/UABEA) — 크로스플랫폼(.NET) 에셋 에디터. ⚠️ Unity **6000.3 이상**에서 MonoBehaviour 파싱 버그가 보고됐으나 우리 게임은 6000.0이라 영향 없을 가능성 높음. 문제 시 **UABEANext** 또는 **AssetRipper**(읽기 전용 분석) 병행
  - Python 3 + numpy + scipy + Pillow (`make_sdf.py`용)
  - (선택) 동일 버전 Unity Editor 6000.0.58f2 — Unity 공식 Font Asset Creator 사용 시
- [ ] 원본 백업: 패치 대상 후보 파일(`resources.assets`, `level*`, `StreamingAssets/Lua`)을 `original/`에 복사

### Phase 1 — 텍스트 위치 검증 (가장 중요, 1~2일)
게임 버전이 Unity 6로 바뀌며 구조가 또 바뀌었을 수 있음. **어디를 고쳐야 화면에 반영되는지** 실험:
1. **Lua 테스트**: `twilight_cards.lua`의 카드 이름 하나를 눈에 띄게 변경 → 게임 실행 → 반영 여부 확인
   - ⚠️ 주의: Lua 로더는 `"twilight/database/twilight_cards.lua"` 경로를 참조하나 파일은 플랫하게 존재 → 경로 매핑 방식 확인 필요. 반영 안 되면 Lua는 잔재 파일일 수 있음
2. **에셋 테스트**: UABEA로 `resources.assets` 열기 → `TS_Cards`(TextAsset), `Common_Strings` 검색 → 문자열 수정 → 게임에서 확인
3. 어느 경로가 "살아있는지" 판명 후 그곳을 주 작업 대상으로 확정

### Phase 2 — 문자열 추출 & 번역 소스 구축 (2~3일)
- [ ] 살아있는 텍스트 소스에서 영문 문자열 전체 추출 → JSON으로 정리
- [ ] **기존 패치에서 한글 번역 추출** (옛 패치 파일 diff 또는 에셋 덤프)
- [ ] 자동 매칭: 기존 번역 ↔ 현재 문자열 대조. 버전업으로 바뀐 문장은 수동 번역
- [ ] 용어 통일표 작성 (Influence=영향력, Coup=쿠데타, DEFCON 등 — 보드게임 한국어판 공식 용어 참고)
- [ ] TMP 리치텍스트 태그(`<color>`, `<font="TIMESI SDF">`, `<br>`, `<indent>`) 보존 규칙 수립

### Phase 3 — 한글 SDF 폰트 아틀라스 생성 (핵심, 3~5일)
1. **문자셋 산출**: 번역 완료된 문자열에서 실제 사용 글자만 추출 (통상 1,500~2,500자 → 아틀라스 4096² 하나에 충분)
2. **폰트 선택** (모두 OFL/재배포 허용):
   | 원본 | 대체 | 비고 |
   |---|---|---|
   | TIMESI SDF (Times 세리프, 본문) | **Noto Serif KR** | 7웨이트 |
   | Anton SDF (제목 고딕) | **Black Han Sans** | 라틴 미포함 → 원본 Anton과 병용 |
   | Bangers SDF | **Gugi** | |
   | atwriter SDF (손글씨) | **나눔손글씨/나눔바른펜** | |
3. **생성 방법** (택 1, A 우선 시도):
   - **A. Unity_Font_Replacer의 `make_sdf.py`** — Unity 에디터 없이 TTF → TMP 호환 JSON+아틀라스 생성 (스탠드얼론 Python이라 macOS에서 바로 실행 가능)
   - B. Unity Editor 6000.0.58f2의 Font Asset Creator (Custom Characters + SDFAA_HINTED + 4096²)
4. **주입 방법** (택 1):
   - A. UABEA로 기존 폰트 에셋의 아틀라스 텍스처 + 문자/글리프 테이블 교체
   - B. Unity_Font_Replacer의 교체 도구로 자동 주입 (Windows exe → Wine/VM 필요 가능성, 도구가 IL2CPP 게임 지원 여부 확인 필요)
5. 게임 내 모든 텍스트 영역에서 한글 출력 확인 (특히 카드 텍스트, 툴팁, 버튼)

### Phase 4 — 텍스트 주입 & 레이아웃 조정 (1~2주)
- [ ] 번역 JSON → 각 소스(Lua/에셋)에 주입하는 스크립트 작성 (반복 적용 가능하게)
- [ ] 한글은 영문보다 짧은 경우가 많아 박스 잘림 적지만, **줄바꿈/공백 처리 차이**로 레이아웃 깨짐 가능 → 개행(`\n`, `<br>`) 위치 조정
- [ ] TMP 태그의 `<font="TIMESI SDF">` 참조를 한글 폰트 이름으로 치환 필요할 수 있음
- [ ] 튜토리얼·규칙 문서(level 씬) 번역 — 분량 최대 구간
- [ ] 텍스처 구워진 문자(보드 국가명 등)는 이번 범위에서 **제외**하거나, 나중에 이미지 작업 별도 진행

### Phase 5 — 플랫폼 적용 & 테스트 (2~3일)
- [ ] macOS: 설치 스크립트 + `codesign --force --sign -` 재서명, 실행 테스트
- [ ] Windows: 동일 수정 파일 복사 + 설치 스크립트 (서명 불필요), 테스트 (VM/실기)
- [ ] 멀티플레이 영향 테스트 (에셋 수정이 온라인 버전 체크에 걸리는지 — 기존 v2.0 패치는 멀티 유지에 성공한 전례 있음)
- [ ] Steam "무결성 확인" 후 재설치 스크립트 정상 동작 확인

### Phase 6 — 배포
- [ ] README + 설치 스크립트 포함된 zip 또는 GitHub Releases
- [ ] 기존 패치 배포처(블루칩 블로그, 한패, Steam 토론)에 업데이트 안내
- [ ] 기존 패치 제작자(블루칩/우드킹)에게 크레딧 및 연락 시도

---

## 5. 플랫폼별 가이드

### macOS
| 작업 | 방법 |
|---|---|
| 데이터 경로 | `TwilightStruggle.app/Contents/Resources/Data/` |
| 코드 서명 | 애드혹 서명 가능 (개발자 계정 불필요): `codesign --force --sign - <앱 경로>`. 프레임워크/플러그인 손상 시 내부→외부 순서로 개별 서명 |
| Gatekeeper | Steam 설치 앱은 격리 속성이 보통 없음. 문제 시 `xattr -cr TwilightStruggle.app` |
| 도구 | UABEA(.NET 크로스플랫폼)·Python 스크립트 모두 macOS에서 실행 가능. 단 Unity_Font_Replacer의 **exe는 Windows 전용** → `make_sdf.py`(Python 원본) 사용 또는 Wine |

### Windows
| 작업 | 방법 |
|---|---|
| 데이터 경로 | `steamapps/common/Twilight Struggle/Twilight Struggle_Data/` (설치 후 확인) |
| 코드 서명 | 불필요 |
| 도구 | 모든 Windows exe 그대로 사용 가능 |

### 공통
- 에셋 파일(`resources.assets` 등)은 데스크톱 양 플랫폼에서 보통 동일 빌드 산출물 → **맥에서 만든 수정 파일을 윈도우에도 그대로 복사 가능** (게임 버전만 일치하면)
- `GameAssembly.dylib`(mac)과 `.dll`(win)은 호환 불가 — 다만 이 패치는 바이너리를 안 건드리는 것이 목표

---

## 6. Edge Cases & 리스크

| 리스크 | 영향 | 대응 |
|---|---|---|
| Steam 무결성 확인/자동 업데이트로 파일 원복 | 패치 소멸 | 설치 스크립트로 즉시 재적용. `boot.config`의 build-guid 또는 파일 해시로 버전 감지, 불일치 시 경고 |
| Lua 파일이 실제로 안 쓰임 (잔재 파일) | 작업 무효 | Phase 1에서 반드시 실게임 반영 테스트 후 착수 |
| Unity 6 직렬화 포맷 변경으로 도구 파싱 실패 | 에셋 편집 불가 | UABEANext / AssetRipper 대안. 최후 수단: Unity Editor로 프로젝트 재구성 후 AssetBundle 주입 (XUnity.AutoTranslator 방식) |
| SDF 아틀라스 용량 부족 | 글자 누락(□) | 사용 글자 기반 문자셋 + 4096², 필요 시 아틀라스 2개로 분할. 폰트 에셋의 fallback 체인 활용 |
| 폰트 교체 후 아웃라인/그림자 스타일 깨짐 | 시각 품질 | Material 파라미터(`_OutlineWidth`, `_GradientScale`)를 원본 padding 기준으로 보정 (Unity_Font_Replacer가 자동 보정 기능 보유) |
| OFL Reserved Font Name | 라이선스 위반 가능성 | 폰트 파일 자체를 수정·개명 재배포 시 Reserved Name 회피. 단순 번들·사용은 문제없음. 라이선스 전문 동봉 |
| 멀티플레이 버전 체크 | 온라인 불가 | v1.4.2 시절 v2.0 패치가 멀티를 유지한 전례 있음. 에셋만 교체 시 유지될 가능성 높으나 반드시 테스트 |
| 텍스처 구워진 영문 | 일부 영문 잔존 | 기존 패치들도 미해결. 1차 범위 제외, 이미지 리터칭은 후속 과제로 |
| IL2CPP 내 하드코딩 문자열 (언어 기본값 등) | 일부 UI 영어 잔존 | 필요 시 Cpp2IL/Il2CppDumper로 분석 후 바이너리 문자열 패치 — 최후의 수단 |
| 번역 인코딩 | Lua/에셋에서 한글 깨짐 | UTF-8 일관 사용, 게임 로드 확인 테스트 |

---

## 7. 도구 총정리

| 도구 | 용도 | 링크/비고 |
|---|---|---|
| **UABEA** | 에셋 추출/수정/재삽입 (크로스플랫폼) | github.com/nesrak1/UABEA |
| UABEANext | UABEA 대안 (IL2CPP 게임에 유리하다는 보고) | nesrak1 레포 참고 |
| AssetRipper / AssetStudio | 읽기 전용 에셋 분석 | github.com/AssetRipper/AssetRipper |
| **Unity_Font_Replacer** | 한글 SDF 아틀라스 포함, 폰트 교체/추출, `make_sdf.py`(Unity 없이 SDF 생성) | github.com/snowyegret23/Unity_Font_Replacer |
| XUnity.AutoTranslator | 폰트 번들 주입 가이드(참고), 런타임 텍스트 후킹 대안 | 위키에 Font Asset 패키징 가이드 |
| Cpp2IL / Il2CppDumper | IL2CPP 바이너리 분석 (필요 시에만) | |
| Unity Editor 6000.0.58f2 | Font Asset Creator (선택지 B) | Unity Hub |

### 폰트 (모두 재배포 허용 라이선스)
- Noto Serif KR (SIL OFL) — 본문/TIMESI 대체
- Black Han Sans (SIL OFL) — 제목/Anton 대체 (라틴 미포함 주의)
- Gugi (SIL OFL) — Bangers 대체
- 나눔손글씨/나눔바른펜 (네이버, OFL 기반) — atwriter 대체

---

## 8. 참고 자료

- 블루칩 한글 패치 v1.0.1/v2.0.1: https://bluechip2022.tistory.com/2
- 한패 백업 목록: https://hanpe.net/hanguls/t (Twilight Struggle 항목)
- 일본어화 패치(블루칩 기반): https://note.com/suraimuman1/n/n49419b1f24f3
- Steam 토론 (패치 제작자의 기술 설명, v1.4.6 구조): steamcommunity.com/app/406290 토론 "Spanish translation?" 스레드
- XUnity.AutoTranslator 폰트 번들 가이드: github.com/bbepis/XUnity.AutoTranslator/wiki

---

## 다음 액션 (즉시 착수 가능)
1. 이 폴더에서 `git init`
2. 기존 패치 다운로드 (블루칩 블로그 + 한패)
3. **Phase 1 검증 테스트**: Lua 카드 이름 변경 → 게임 실행 → 반영 확인
