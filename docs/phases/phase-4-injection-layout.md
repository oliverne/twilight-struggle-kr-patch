# Phase 4 — 텍스트 주입 & 레이아웃 조정

## 상태

- 상태: ✅ 완료 (무손상 주입 재구축 완료)
- 선행 Phase: Phase 2·3 완료

## ⚠️ 재구축 기록 (2026-08-11) — UnityPy save가 폰트를 파괴

기존 `patched/resources.assets`는 공식 UnityPy 1.25.3의 `env.file.save()`로 생성됐는데,
이 게임(IL2CPP)에서 저장 시 **MonoBehaviour 11,890개의 m_Script 참조가 재매핑**되고
**Shader/AnimationClip/AudioClip 등 11,949개 객체의 raw 데이터가 변경**됐다.

- TMP_FontAsset 23개: m_Script (1,672)=`TMP_FontAsset` → (1,670)=`TutorialSteps1`로 변조
- 결과: Unity_Font_Replacer가 폰트를 인식하지 못함 (SDF 0개 스캔) + 게임 실행 위험

**해결**: 포크 UnityPy(snowyegret23) + TypeTreeGeneratorAPI 기반 typetree_generator를
`env.typetree_generator`에 설정한 뒤 저장 → m_Script 0건/raw 0건 불일치.

### 재현 방법 (macOS/Windows 공용)

```bash
pip install TypeTreeGeneratorAPI numpy scipy Pillow
pip install --upgrade "git+https://github.com/snowyegret23/UnityPy.git"

python scripts/inject_translations.py --gamepath <게임루트> \
    --src <원본 resources.assets> --out patched/resources.assets
# 검증
python scripts/verify_assets.py --orig <원본> --patched patched/resources.assets
```

- `--gamepath`는 IL2CPP 바이너리(GameAssembly.dll/.dylib)와 `global-metadata.dat` 탐색에 필요
- macOS에서는 `GameAssembly.dylib`을 자동 탐색한다
- **공식 UnityPy로 저장 금지** (위 손상 재발)

## 목표

번역 소스를 게임 에셋에 반복 적용할 수 있는 파이프라인을 만들고, 한글 길이·개행·TMP 태그 차이로 발생하는 UI 레이아웃 문제를 조정한다.

## 주입 방식 결정 (Phase 2에서 확정)

- **EN 열(열 2)은 보존하고, 다른 언어 열을 한국어로 교체한다.** 원문(EN)을 덮어쓰지 않는다.
- 이유: 영문 폴백·원문 대조·번역 검수 유지, EN열 치환 시 짧은 토큰 측면 치환 위험 회피.
- 현재 `Common_Strings` 열 구조: `Key(1) EN(2) FR(3) DE(4) ES(5) PL(6) PT(7) JP(8) IT(9) RU(10) NL(11) CH(12) null(13~)`
- 현재 `AvailableCultures` 등록 언어: `de, en, es, fr, ru` (SmartLocalization)
- Phase 2 번역 소스는 **EN 원문**(열 2)과 **번역값**(한글)을 분리 저장했으므로, 교체 열 선택과 무관하게 재사용 가능.

## 체크리스트

- [x] 번역 JSON → TextAsset 주입 스크립트 작성 (`scripts/inject_translations.py`) — **무손상 저장 방식으로 재구축**
- [x] **Common_Strings 주입** — RU(10열) → KO, 322행 한글 주입, EN(2열) 보존
- [x] **TS_Cards 주입** — 344행 EN→한글 교체
- [x] **AvailableCultures 수정** — ru → ko (한국어 선택 가능)
- [x] EN 열 보존 검증 (Common_Strings: col 2 EN 무결함)
- [x] `TS_Ingame`(117행)·`TS_Strings`(38행)·`Common_Ingame`(22행) 주입 — 런타임 TSV 커버
- [x] **잔존 영어 키 수동 번역 재주입 (2026-08-11)** — `translation/manual-extra.json` 53키 (TS_Ingame 41 + TS_Strings 12)
      - TS_Ingame: 'Current Turn'→'현재 턴', 'Bid For Sides'→'진영 입찰', 'No Presence'→'진출 없음', 'Defcon Level'→'데프콘 단계', 'Game Results'→'게임 결과' 등
      - TS_Strings: 'Flavor_Castro', 'Key_USSR'→'소련', 'Key_MapTypeClassic' 등
      - `inject_simple_table`이 key 기준 manual도 지원하도록 확장 (값 기준 우선)
- [x] 설치 스크립트 `scripts/install.sh` 작성 (macOS)
- [x] 무결성 검증 스크립트 `scripts/verify_assets.py` (m_Script/raw 비교)
- [ ] 게임에서 한국어로 전환되는지 실게임 테스트 (Phase 5)
- [ ] `TS_RulesTutorial` — File/String 참조만 있고 표시 텍스트 없음 → 제외 (기존 결정 유지)

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 재현성 | 번역 JSON과 원본 에셋만으로 패치 파일을 재생성할 수 있음 |
| 보존성 | TMP 태그와 필요한 개행이 유지됨 |
| 레이아웃 | 주요 화면에서 텍스트 잘림·겹침·빈 박스가 없음 |
| 안전성 | 스크립트가 원본 해시를 확인하고 멱등적으로 실행됨 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| Common_Strings 주입 | `inject_translations.py` — 셀 단위 키 매칭, RU(10)→KO, EN 무결성 검증 | ✅ 성공 — 322행 한글 주입, EN 보존 |
| TS_Cards 주입 | `inject_translations.py` — row-key 기반 EN→KO | ✅ 성공 — 344행 교체, 카드명/설명 한글 확인 |
| AvailableCultures | XML 텍스트 치환 ru→ko | ✅ 성공 — "ko" 문화 등록 |
| 부가 주입 | TS_Ingame 117행, TS_Strings 38행, Common_Ingame 22행 (런타임 TSV) | ✅ 성공 |
| m_Script 무손상 | `verify_assets.py` — 원본 vs patched 전체 비교 | ✅ 성공 — 불일치 0건 |
| raw 무손상 | `verify_assets.py` — TextAsset/폰트 외 raw 바이트 | ✅ 성공 — 예상외 변경 0건 |
| 게임 테스트 | — | ⬜ 대기 (Phase 5, 폰트 주입 완료됨) |
| 잔존 키 재주입 | `inject_translations.py` 재실행 (2026-08-11) | ✅ 성공 — TS_Ingame 40행 + TS_Strings 12행, m_Script 0건 |
| 재주입 후 영어 잔존 | TextAsset 스캔 | ✅ 성공 — TS_Ingame/TS_Strings 0개 |

## 산출물

- `patched/resources.assets` — 번역 주입 + 폰트 주입 완료본 (108MB, gitignore)
- `patched/sharedassets0.assets` — atwriter SDF 폰트 주입본 (4.6MB, gitignore)
- `patched/hashes.txt` — SHA-256 기록 (git 관리)
- `scripts/inject_translations.py` — 무손상 번역 주입 스크립트
- `scripts/verify_assets.py` — 무결성 검증 스크립트

## 다음 Phase로 핸드오프

- 수정 파일: `patched/resources.assets` + `patched/sharedassets0.assets` (2026-08-11 재주입으로 갱신 — 잔존 키 53개 포함)
- 추가 산출물: `translation/manual-extra.json` (수동 번역 53키), `patched/level1~3` (씬 패치는 Phase 5에서 처리)
- 레이아웃 이슈: 미확인 (게임 테스트 후 기록), 폰트 크기 불일치 이슈 #12로 등록
- 제외한 텍스트 영역: `TS_RulesTutorial`(표시 텍스트 없음), 보드맵 국가명(텍스처 구움)
- 플랫폼별 주의사항: macOS 코드사인 필수, `patched/*.assets`는 gitignore(GitHub 100MB 제한)
- 주입 재실행: 위 "재구축 기록"의 재현 방법 참조 — `inject_translations.py`는 번역 소스(manual-extra 포함)만 갱신하면 멱등적으로 재실행 가능
