# 사용 도구 · 오픈소스 (Tools & Open Source)

> 이 프로젝트에서 사용한 오픈소스·도구·라이브러리와 참고 자료를 정리한다.
> 원저작권자, 번역 출처, 폰트 라이선스 등 **법적 고지는 [`LICENSE`](../LICENSE)를 기준**으로 한다.
> (이 문서는 `REFERENCES.md`를 대체 — 2026-08-14)

## 1. 에셋 조작 도구

| 도구 | 버전 | 용도 | 라이선스 | 링크 |
|---|---|---|---|---|
| UABEA (UABE Avalonia) | — | Unity 에셋 추출·수정 (초기 탐색·검증) | MIT | https://github.com/nesrak1/UABEA |
| UnityPy (**포크**) | 1.25.2 기반 | 번역 주입 `inject_translations.py` — ⚠️ 공식판 `save()`는 m_Script를 재매핑해 파괴, **포크 + TypeTreeGeneratorAPI 필수** | MIT | https://github.com/K0lb3/UnityPy |
| TypeTreeGeneratorAPI | 0.0.10 | IL2CPP 타입트리 생성·보강 (포크 UnityPy와 조합) | MIT | https://pypi.org/project/TypeTreeGeneratorAPI |
| AssetsTools.NET | 2.0.12 | `tools/asset-tool` (.NET 8) — 씬/에셋 문자열 구조 분석 | MIT | https://github.com/nesrak1/AssetsTools.NET |
| Il2CppDumper | — | IL2CPP 메타데이터 분석 (`tools/unity-font-replacer/Il2CppDumper`) | MIT | https://github.com/Perfare/Il2CppDumper |
| Unity_Font_Replacer | v1.2.8 | `make_sdf.py`(TTF→TMP SDF 생성) + `unity_font_replacer_ko.exe --parse/--list`(에셋 폰트 교체) | MIT | https://github.com/snowyegret23/Unity_Font_Replacer |

> ⚠️ `Unity_Font_Replacer_AT`(C#/AssetsTools.NET 포트)는 참고 자료이며, 실제 사용은 **v1.2.8 (Python 기반)** 이다.
> 폰트 주입 절차는 [Runbook — Windows 폰트 주입](runbooks/phase-3-windows-font-injection.md) 참조.

## 2. 파이썬 패키지 (`.venv`)

에셋 주입·SDF 생성 파이프라인의 런타임 의존성.

| 패키지 | 용도 | 라이선스 |
|---|---|---|
| numpy, scipy | SDF 생성·문자셋 통계 (make_sdf.py 보조) | BSD-3-Clause |
| Pillow | SDF 아틀라스 이미지 처리 | MIT-CMU (HPND) |
| fontTools | 폰트 파싱·메트릭 추출 | MIT |
| UnityPy, TypeTreeGeneratorAPI | 1번 표 참조 | MIT |

## 3. 런타임 프레임워크

| 도구 | 용도 | 라이선스 | 상태 |
|---|---|---|---|
| BepInEx | IL2CPP 런타임 훅 — 계층 3(턴 히스토리·튜토리얼) 해결용 | LGPL-2.1 | ⏸️ 보류 (ISSUES #11·#17) |
| Steam / Valve | 게임 유통 플랫폼 (App ID 406290) | Valve 정책 | — |

## 4. 폰트 (번역 주입용 한글 SDF)

| 폰트 | 버전 | 용도 | 라이선스 |
|---|---|---|---|
| D2Coding | 1.3.3 | 본문·IMPACT 계열 (24개 TMP 폰트 주입) | SIL OFL 1.1 |
| Paperlogy 5 Medium | — | 제목 계열 | SIL OFL 1.1 |

라이선스 전문은 `fonts/LICENSE-OFL-1.1.txt`에 동봉. (폰트 교체/크기 조절 절차: [폰트 스킬](../.agents/skills/) 참조)

## 5. 번역 재사용 소스 (커뮤니티 패치 — 오픈소스 아님)

| 소스 | 비고 | 사용 |
|---|---|---|
| 한식구 네이버 카페 런타임 패치 (BepInEx, 2026-03-15) | 런타임 TSV 2,253쌍 | ✅ 1차 번역 소스 (`runtime-20260315.json`) |
| 블루칩 한글패치 v1.0.1 | MonoBehaviour 문자열 432개 | 참고·검증 (구버전) |
| 우드킹 패치 | — | 참고 (입수 안 함) |

## 6. 개발·배포 환경

| 도구 | 용도 | 라이선스 |
|---|---|---|
| Python 3.13 + venv | 주입·패치·검증 스크립트 | PSF |
| .NET SDK 10 / 8 | UABEA·asset-tool (초기) | MIT |
| Git + Git Bash | 저장소 관리·스크립트 실행 | GPL-2.0 (Git) |
| gh CLI 2.97 | GitHub Releases 업로드 | MIT |
| sha256sum / Python zipfile | 패키징·해시 (`package-release.sh`) | 표준 |

## 7. 참고 자료 (REFERENCES.md에서 이관)

- 한패넷 — Twilight Struggle 한글화 정보: <https://hanpe.net/app/46v739/twilight-struggle>
- 유니티 에디터 없이 SDF 폰트 교체하는 법 (네이버 카페): <https://cafe.naver.com/f-e/cafes/16259867/articles/32224?menuid=27&referrerAllArticles=false>
- Unity_Font_Replacer_AT (C# 포트, 미사용): <https://github.com/snowyegret23/Unity_Font_Replacer_AT>
- BepInEx (계층 3 보류 항목): <https://github.com/BepInEx/BepInEx>
