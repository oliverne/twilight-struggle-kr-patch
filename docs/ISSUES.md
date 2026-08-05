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

### #8 `.NET 8` vs `.NET 10` 문서 정합성
- **위치**: `docs/PHASE-0-PLAN.md` Step 2 ("`.NET 8`"), Phase 0 완료 문서 (`.NET 10.0.302`), `asset-tool.csproj` (`net8.0`)
- **문제**: 계획 문서는 .NET 8, 실제 설치는 10.0.302, csproj 타겟은 net8.0. 현재 `DOTNET_ROLL_FORWARD=LatestMajor`로 구동 중으로 보이나, 문서에 정합성·의존성 명시 부재.
- **제안 수정**: `PHASE-0-PLAN.md`의 ".NET 8"을 실제 설치한 버전 기준으로 업데이트, 또는 roll-forward 정책을 setup 스크립트 설명에 명시.
- **상태**: ⬜ 보류
- **관련 Phase**: 언제든 (문서 정합성)

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
- **제안 수정**: Phase 5 체크리스트에 "Windows 데이터 경로 실측"을 1순위로 추가해 검증 기준에 명시.
- **상태**: ⬜ 보류
- **관련 Phase**: Phase 5

---

## 처리된 이슈 (참고용)

> Phase 0·1 완료 시점의 코드 리뷰에서 이미 처리된 항목. 커밋 `fbb70bc`, `50feea1`, `69e71a8` 참조.

- ✅ #1 .NET 빌드 산출물 git 추적 제거 (Critical)
- ✅ #2 asset-tool 문서화 (Critical)
- ✅ #2 Phase 1 산출물·파이프라인에 도구 역할 분리 (Critical)
- ✅ #2 Phase 2 번역 소스 키/셀 구조 설계 (Warning #3, #4 근본 해결)
- ✅ #5 `requirements.txt` UnityPy 버전 pin (Warning)