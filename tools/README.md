# tools/

보조 도구 및 기존 패치 보관소. `asset-tool/` 소스는 git 관리, 나머지는 로컬 전용(`.gitignore`).

| 경로 | 용도 | 설치 방법 |
|---|---|---|
| `asset-tool/` | 에셋 탐색·덤프 (.NET, AssetsTools.NET 기반) | `dotnet build tools/asset-tool` (단, `tools/uabea/AssetsTools.NET.dll` 참조용이므로 `setup-uabea-mac.sh` 먼저 실행 필요). 명령: `probe`\|`types`\|`list`\|`dump <assets> [이름] [출력파일]` |
| `uabea/` | 에셋 추출/수정 (GUI) | `scripts/setup-uabea-mac.sh` 실행 (v8 ubuntu 빌드 + macOS 네이티브 보강). 실행: `DOTNET_ROLL_FORWARD=LatestMajor dotnet tools/uabea/UABEAvalonia.dll` |
| `legacy-patches/` | 기존 한글 패치 (번역 추출용) | [블루칩](https://bluechip2022.tistory.com/2), [한패](https://hanpe.net/hanguls/t) |
| `asset-ripper/` | (선택) UABEA 파싱 실패 시 대안 | [AssetRipper Releases](https://github.com/AssetRipper/AssetRipper/releases) |
| `dump/` | UnityPy/asset-tool 추출 텍스트 덤프 | 스크립트로 재생성 (git 제외, 게임 파생물) |

## asset-tool 비고

- Phase 1 실험 B 준비용으로 작성한 읽기 전용 탐색 도구. `AssetsTools.NET.dll`을 `../uabea/`의 파일로 HintPath 참조하므로 **`tools/uabea/` 없이는 빌드 불가**.
- 역할은 에셋 구조 파악·TextAsset 덤프이며, 실제 텍스트 주입은 UnityPy 기반 `scripts/patch_textasset.py`를 사용한다 (Phase 1 결론).
- NuGet 패키지 참조로 전환하면 `tools/uabea/` 의존을 제거할 수 있으나 현재는 로컬 DLL 참조 유지.
