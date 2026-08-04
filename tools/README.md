# tools/

보조 도구 및 기존 패치 보관소 (git 관리 대상 아님, 로컬 전용)

| 경로 | 용도 | 설치 방법 |
|---|---|---|
| `uabea/` | 에셋 추출/수정 | `scripts/setup-uabea-mac.sh` 실행 (v8 ubuntu 빌드 + macOS 네이티브 보강). 실행: `DOTNET_ROLL_FORWARD=LatestMajor dotnet tools/uabea/UABEAvalonia.dll` |
| `legacy-patches/` | 기존 한글 패치 (번역 추출용) | [블루칩](https://bluechip2022.tistory.com/2), [한패](https://hanpe.net/hanguls/t) |
| `asset-ripper/` | (선택) UABEA 파싱 실패 시 대안 | [AssetRipper Releases](https://github.com/AssetRipper/AssetRipper/releases) |
