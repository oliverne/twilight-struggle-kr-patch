# 보류 이슈 목록

> 2026-08-05 코드 리뷰에서 발견된 이슈 중 즉시 처리하지 않은 항목.
> 우선순위가 낮거나, 해당 Phase 진행 중 자연스럽게 해결될 수 있는 항목들이다.
> 완료 시 항목에 ✅ 표시 후 처리 내용을 간단히 기록한다.

---

## 🟡 Warning

### #6 `setup-uabea-mac.sh` — 다운로드 체크섬·서명 검증 없음
- **위치**: `scripts/setup-uabea-mac.sh` (UABEA zip 다운로드 ~15–19행, `fetch_nuget_native` ~30–40행)
- **문제**: `curl -sL`로 GitHub Release zip과 NuGet 패키지를 받아 unzip만 하고 **SHA-256 비교 없음**. MITM 또는 레포 침해 시 악성 네이티브 라이브러리(`libSkiaSharp.dylib` 등)가 `tools/uabea/`에 주입될 수 있음. .NET 네이티브 라이브러리는 에셋 처리 과정에서 로드되므로 공격 표면 실재.
- **제안 수정**: 알려진 SHA-256 상수와 비교하는 검증 단계 추가. NuGet은 `nuget verify` 또는 패키지 해시 비교. 최소한 공식 릴리스 해시는 UABEA 릴리스 노트에서 가져와 assert.
- **상태**: ⬜ 보류
- **관련 Phase**: Phase 5(배포 전 최종 검증 시 점검 권장)

### #7 `restore-original.sh` — `while read` 마지막 줄 누락·공백 파일명 위험
- **위치**: `scripts/restore-original.sh` (복원 루프 ~17–21행)
- **문제**: `while read -r hash f; do ... done < hashes.txt` 패턴은 마지막 줄에 개행이 없으면 읽지 않음. 또한 IFS 기본 분할이라 파일명에 공백이 있으면 `f`가 잘림. 현재 `original/StreamingAssets/` 파일명엔 공백 없어 즉시 위험은 없으나, 향후 산출물 추가 시 잠재적 손상.
- **제안 수정**: `while IFS= read -r line || [ -n "$line" ]; do hash=${line%% *}; f=${line#*  }; ...` 형태로 개행 누락·공백 파일명 모두 대응.
- **상태**: ⬜ 보류
- **관련 Phase**: Phase 5(설치 스크립트 검증 시 점검 권장) 또는 `backup-original.sh` 포맷 변경 시

---

## 🔵 Info

### #9 `asset-tool.csproj` HintPath 의존으로 clone 후 빌드 불가
- **위치**: `tools/asset-tool/asset-tool.csproj` (`<HintPath>../uabea/AssetsTools.NET.dll</HintPath>`)
- **문제**: `tools/uabea/`는 gitignored이므로, 신규 clone 환경에서 `dotnet build` 시 DLL 부재로 실패. 소스만 가지고는 재현 불가.
- **제안 수정**: uabea가 없을 때 빌드를 건너뛰거나, NuGet으로 `AssetsTools.NET` 패키지 참조로 전환해 HintPath 의존 제거.
- **상태**: ⬜ 보류
- **관련 Phase**: Phase 5(재현성 검증 시) 또는 `asset-tool` 재사용 필요할 때
- **비고**: Phase 4 주입 도구는 `patch_textasset.py`(UnityPy)가 주 도구이므로, asset-tool 빌드가 안 되어도 패치 진행에 차질 없음. dump는 `tools/dump/` 산출물이 이미 있고 UnityPy로도 재생성 가능.

### #10 `README.md` "Windows 경로 예상" 미검증 표기가 Phase 5까지 방치 위험
- **위치**: `PLAN.md` §1 (Windows 경로 "예상 — 설치 후 확인 필요")
- **문제**: Phase 5 "Windows 테스트 ⬜"로 아직 미검증. Windows 경로 마지막 컴포넌트가 `Twilight Struggle_Data`인지 `Data`인지 Phase 5 착수 전까지 검증 필요.
- **상태**: ✅ 해결 — 실측 완료: `steamapps/common/Twilight Struggle/TwilightStruggle_Data/` (2026-08-11 Windows 게임 설치본 확인)
- **관련 Phase**: Phase 5

---

## 🟢 처리된 이슈 추가 (2026-08-11)

- ✅ #10 Windows 데이터 경로 실측 — `TwilightStruggle_Data` (공백 없음)

---

## 🔴 Blocked / 🟡 Warning (2026-08-11 추가)

### #11 턴 히스토리(게임 하단 로그) 한글화 불가 — IL2CPP 코드 문자열
- **위치**: `il2cpp_data/Metadata/global-metadata.dat` — 'to attempt a Coup in', 'gets a Coup Strength of' 등 C# 리터럴
- **문제**: 턴 히스토리 메시지가 씬/TextAsset이 아닌 코드 문자열 템플릿 + 카드명 조합으로 생성됨. IL2CPP 메타데이터 문자열 패치는 길이 제약(한글 3바이트)으로 사실상 불가. 기존 런타임 패치(2026-03-15) TSV에도 format string 없음 → 모든 기존 패치가 미커버한 영역
- **제안**: BepInEx 플러그인 런타임 훅 (문자열 포맷 후킹) — 별도 프로젝트로 판단
- **상태**: ⬜ 보류 (Phase 5 핸드오프에 기록)

### #12 폰트 크기/줄 간격 불일치 — 원본 24종 → 한글 2종 통일
- **위치**: `resources.assets` TMP_FontAsset 23개 + sharedassets0 atwriter (m_FaceInfo)
- **문제**: 원본 폰트(Anton·Bangers 등 제목용, TIMES 본문용)의 개별 메트릭이 사라지고 NotoSerifKR(lineHeight 108/EM)·BlackHanSans(88/EM)로 통일되어 동일 fontSize 대비 표시 크기·줄 간격 차이 발생 (실게임 확인)
- **제안**: ① Unity_Font_Replacer `--use-game-line-metrics` 재주입 (원본 줄 간격 유지) ② m_FaceInfo 배율 직접 조정 (UnityPy) ③ 원본 폰트 특성별 SDF 변형 세분화 (본문/제목/소형)
- **상태**: ⬜ 보류 (게임 테스트 후 우선순위 결정)

### #13 Windows 설치 스크립트 미작성
- **위치**: `scripts/` — macOS `install.sh`만 존재
- **문제**: 배포를 위해 Windows용 설치/복구 스크립트(`install-windows.ps1`) 필요 (백업 → 복사 → 해시 검증)
- **상태**: ⬜ 보류 (Phase 5 체크리스트 잔여)

### #14 규칙북/튜토리얼 긴 문단 미번역 (씬 하드코딩 167개)
- **위치**: level1·level2 MonoBehaviour — 'Twilight Struggle is a two-player game...' 등
- **문제**: 런타임 TSV·수동 번역으로 커버 안 되는 규칙 본문이 씬에 하드코딩되어 있음 (TS_RulesTutorial 제외 결정과 별개로 씬에도 존재)
- **제안**: 번역량 대비 우선순위 낮음 — 게임 테스트 후 필요 시 `manual-scenes.json`에 추가
- **상태**: ⬜ 보류

### #15 모든 언어 테이블 KO 열 부재 — 언어=KO에서 ${Key} 노출 (2026-08-12 해결)
- **위치**: TS_Cards·TS_Ingame·TS_Strings·Common_Ingame·TS_RulesTutorial (Common_Strings는 KO 열 있음)
- **문제**: 씬 UI 텍스트는 `${Card_*}/${Panel_*}/${Help_*}` 키 문자열이고 SmartLocalization이 언어별 열로 해석. EN 열(2~3열)에 한글을 넣었지만 KO 열이 없어 KO 언어에서 키가 그대로 노출 (카드 전체 + Scoring UI). 이전 테스트에서 카드가 한글이었던 건 언어=EN이었기 때문
- **1차 시도 (실패)**: 26/27열(원본에 없는 열 번호)에 셀 추가 → 게임 파서가 무시 → 키 노출 지속
- **해결**: ✅ `scripts/add_ko_columns.py` — **원본 존재 열 범위 내 빈(null) 열**에 KO 라벨 + EN 열 값(한글) 복사: TS_Cards 9열(344행)/TS_Ingame 8(157)/TS_Strings 8(50)/Common_Ingame 8(22)/TS_RulesTutorial 10(313). 1열은 키 열이라 제외. m_Script 0건 검증 통과
- **관련 Phase**: Phase 5

### #16 SDF 문자셋 누락 104자 — 국가명 □ (2026-08-12 해결)
- **위치**: fonts/chars.txt (596자) — 튀/콰/콜/롬/냐/룬 등
- **문제**: 문자셋이 번역 소스 기준이라 씬 문자열(국가명 등) 글자가 누락 → SDF 아틀라스에 글리프 없음
- **해결**: ✅ chars.txt 596→739자 (패치 후 표시 문자열 전체에서 재추출) + SDF 재생성 + 재주입
- **비고**: point-size가 74→70(NotoSerifKR), 87→83(BlackHanSans)로 축소 (2048² 한계, padding 7→4). 화면 표시 크기는 faceInfo 기반이라 동일
- **관련 Phase**: Phase 5

## 처리된 이슈 (참고용)

> Phase 0·1 완료 시점의 코드 리뷰에서 이미 처리된 항목. 커밋 `fbb70bc`, `50feea1`, `69e71a8` 참조.

- ✅ #1 .NET 빌드 산출물 git 추적 제거 (Critical)
- ✅ #2 asset-tool 문서화 (Critical)
- ✅ #2 Phase 1 산출물·파이프라인에 도구 역할 분리 (Critical)
- ✅ #2 Phase 2 번역 소스 키/셀 구조 설계 (Warning #3, #4 근본 해결)
- ✅ #5 `requirements.txt` UnityPy 버전 pin (Warning)
- ✅ #10 Windows 데이터 경로 실측 — `TwilightStruggle_Data` (공백 없음, 2026-08-11)