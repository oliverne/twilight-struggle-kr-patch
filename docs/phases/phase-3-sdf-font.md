# Phase 3 — 한글 SDF 폰트 아틀라스 생성

## 상태

- 상태: ✅ 완료 (폰트 주입 완료 — Windows exe + macOS 소스 실행, 2026-08-12)
- 선행 Phase: Phase 2 완료
- **절차**: 스킬 [twilight-struggle-font-injection](../../.agents/skills/twilight-struggle-font-injection/SKILL.md)

## 목표

번역문에 실제로 사용되는 한글 글자를 포함한 TMP 호환 SDF 폰트 아틀라스를 생성하고 기존 `resources.assets`의 폰트 에셋에 주입한다.

## 배경

게임은 TextMeshPro(TMP)로 텍스트를 렌더링한다. TMP는 TTF를 직접 쓰지 않고 SDF(Signed Distance Field) 폰트 아틀라스라는 특수 텍스처를 사용한다. 현재 게임의 SDF 아틀라스는 라틴 문자만 포함하고 있어, 한글을 출력하면 빈 네모(`□`)가 표시된다. (Phase 1에서 확인)

**macOS 직접 실행 (2026-08-12 검증)**: 원래 Windows 전용으로 기록됐으나, Python 소스 실행 + Windows 빌드 `GameAssembly.dll`/`global-metadata.dat` 준비로 **macOS에서 전체 주입 파이프라인 재현 가능** — 스킬 [twilight-struggle-font-injection](../../.agents/skills/twilight-struggle-font-injection/SKILL.md) "macOS 소스 실행 시 유의점" 참조 (venv 패치 2건 필수)

## 체크리스트

- [x] 도구 다운로드 및 설치 (`tools/unity-font-replacer/`에 배치)
- [x] 번역문에서 사용 글자 문자셋 산출 → `fonts/chars.txt` (596자, 한글 508자 → **739자로 확장, Phase 5**)
- [x] 폰트 TTF 다운로드 및 라이선스 확인 (Noto Serif KR, Black Han Sans) → `fonts/`
      (⚠️ 이후 2026-08-12 폰트 교체: 본문 D2Coding, 제목 Paperlogy 5 Medium — `fonts/README-fonts.md` 참조)
- [x] `make_sdf.py`로 TTF → SDF JSON + Atlas PNG + Material JSON 생성
      - ~~4096² (point-size 162/192)~~ → **2048² (point-size 74/87, auto)로 최적화** — 24개 폰트 주입 시 397MB → 103MB
- [x] 게임 폰트 목록 파악 (24개 TMP FontAsset: resources.assets 23 + sharedassets0 atwriter SDF)
- [x] Windows에서 폰트 교체 → [스킬: 폰트 주입](../../.agents/skills/twilight-struggle-font-injection/SKILL.md)
- [x] 수정된 `resources.assets` macOS 전송 준비 (patched/ 반영)
- [x] macOS 재서명 (`codesign --force --sign -`) — install.sh가 처리 (2026-08-12 macOS 적용으로 검증)
- [x] 게임 내 한글 출력 확인 (메뉴·카드·툴팁) — 2026-08-12 macOS 실게임 확인 (Phase 5)
- [x] 잔존 `□`/`ㅁ` 글자 확인 및 누락 문자 추가 — 2026-08-12 문자셋 739자 확장·재주입 완료 (Phase 5)

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 문자셋 | 번역 소스에서 실제 사용 글자를 재현 가능하게 추출함 |
| SDF 생성 | `make_sdf.py`가 오류 없이 JSON + Atlas PNG 생성 |
| 주입 | Windows 도구가 에셋을 수정하고 게임이 정상 실행됨 |
| 렌더링 | 메뉴·카드·툴팁 등 주요 텍스트에서 한글이 `□` 없이 정상 표시됨 |
| 재서명 | macOS에서 `codesign` 후 실행 가능 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| 문자셋 추출 | `scripts/extract_charset.py` | ✅ 성공 — 596자 (한글 508자 + 기타 88자) |
| SDF 생성 | `make_sdf.py` — NotoSerifKR (point-size 74), BlackHanSans (point-size 87), 2048² | ✅ 성공 — 595 glyphs, SDF JSON/Material 정상 |
| 게임 폰트 파악 | UnityPy raw 바이트 파싱 | ✅ 성공 — 24개 TMP FontAsset 확인 |
| 폰트 주입 | Windows `unity_font_replacer_ko.exe --list` | ✅ 성공 — 24개 폰트 교체 (NotoSerifKR 13 + BlackHanSans 11), Sprite Asset 3개 제외 |
| 무손상 검증 | `scripts/verify_assets.py` | ✅ 성공 — m_Script 0건/예상외 raw 0건 |
| 게임 테스트 | macOS 실게임 (Phase 5, 2026-08-12) | ✅ 성공 — 메뉴·카드·인게임 UI 한글 + 폰트 정상 (D2Coding/Paperlogy) |

## 폰트 매핑 (결정 사항)

| 교체 폰트 | 대상 |
|---|---|
| **NotoSerifKR SDF** (현재 내용: **D2Coding Regular**) | 본문/세리프 계열 13개: TIMES, TIMESI, LiberationSans(+Fallback), FRAMD 계열, GOTHIC 계열, Unity |
| **BlackHanSans SDF** (현재 내용: **Paperlogy 5 Medium**) | 디스플레이/제목 계열 11개: Anton, Bangers, Electronic Highway Sign, Oswald, Roboto-Bold, Gunplay, IMPACT 계열, atwriter(+outline) |
| 교체 제외 | Sprite Asset 3개 (Default Sprite Asset, DropCap Numbers, EmojiOne) |

> KR_ASSETS의 파일명(`NotoSerifKR SDF`·`BlackHanSans-Regular SDF`)은 도구 매핑 유지를 위해 그대로 두고 **SDF JSON 내용만 교체**한다 (2026-08-12 폰트 교체 방식).

매핑은 `tools/unity-font-replacer/Twilight Struggle.json`의 `Replace_to`로 관리 (작업 폴더, git 제외).
게임 테스트 후 폰트별 표시 확인이 필요하면 매핑을 조정한다.

## 리스크 (업데이트)

| 리스크 | 대응 |
|---|---|
| ~~`make_sdf.py` 4096² 초과~~ | ✅ 596자로 충분히 수용 (point-size 74/87 @2048²) |
| `Unity_Font_Replacer` macOS 미지원 | Windows에서 `.exe` 실행 — [스킬: 폰트 주입](../../.agents/skills/twilight-struggle-font-injection/SKILL.md) |
| `Il2CppDumper.exe` 실행 실패 | Windows 환경에 .NET 8.0 Runtime 설치 필요 |
| `resources.assets` 크기 증가 | 2048² 아틀라스로 최적화 — 103MB (4096² 시 397MB) |
| ~~UnityPy save로 m_Script 손상~~ | ✅ 포크 UnityPy + typetree_generator로 재구축 (Phase 4 문서 참조) |
| **게임 폴더의 `Managed` 존재로 Mono 오판** | 가상 작업 폴더에서 `Managed` 제거 → IL2CPP 인식 (스킬 twilight-struggle-font-injection 참조) |

## 다음 Phase로 핸드오프

- Windows 주입 성공: `unity_font_replacer_ko.exe --parse` + `--list` (oneshot 아님) 사용
- 생성된 SDF 아틀라스: 2048² × 2 (NotoSerifKR point-size 74, BlackHanSans 87 → 이후 70/83 → 폰트 교체 후 77 통일, 2026-08-12), 595 glyphs
- 교체된 폰트: 24개 TMP FontAsset (NotoSerifKR 13 + BlackHanSans 11), Sprite Asset 3개 제외
- Material: 도구 기본 보정 사용 (게임 원본 스타일 유지 + atlas/padding 자동 보정)
- 잔존 `□` 글자: ✅ 2026-08-12 문자셋 739자 확장·재주입 완료 (Phase 5)
- macOS 코드사인: `codesign --force --sign -` 필수 (install.sh가 자동 처리)
- **Phase 5: macOS는 Windows 전송 없이 자체 파이프라인 재현으로 해결 (2026-08-12) — 스킬 twilight-struggle-font-injection 참조**
