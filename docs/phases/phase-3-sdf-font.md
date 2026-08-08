# Phase 3 — 한글 SDF 폰트 아틀라스 생성

## 상태

- 상태: 🚧 진행 중 (macOS에서 SDF 생성 완료, Windows에서 주입 대기)
- 선행 Phase: Phase 2 완료
- **Runbook**: [docs/runbooks/phase-3-windows-font-injection.md](runbooks/phase-3-windows-font-injection.md)

## 목표

번역문에 실제로 사용되는 한글 글자를 포함한 TMP 호환 SDF 폰트 아틀라스를 생성하고 기존 `resources.assets`의 폰트 에셋에 주입한다.

## 배경

게임은 TextMeshPro(TMP)로 텍스트를 렌더링한다. TMP는 TTF를 직접 쓰지 않고 SDF(Signed Distance Field) 폰트 아틀라스라는 특수 텍스처를 사용한다. 현재 게임의 SDF 아틀라스는 라틴 문자만 포함하고 있어, 한글을 출력하면 빈 네모(`□`)가 표시된다. (Phase 1에서 확인)

**macOS 한계**: [Unity_Font_Replacer](https://github.com/snowyegret23/Unity_Font_Replacer)의 `make_sdf.py`(SDF 생성)는 macOS에서 정상 작동하나, `unity_font_replacer_ko.py`(에셋 주입)는 Il2CppDumper.exe + Managed 폴더 생성에 Windows 전용 API(subprocess.STARTUPINFO, psutil.io_counters)를 사용해 macOS에서 실행 불가. **→ SDF 생성은 macOS, 주입은 Windows에서 실행.**

## 체크리스트

- [x] 도구 다운로드 및 설치 (`tools/unity-font-replacer/`에 배치)
- [x] 번역문에서 사용 글자 문자셋 산출 → `fonts/chars.txt` (596자, 한글 508자)
- [x] 폰트 TTF 다운로드 및 라이선스 확인 (Noto Serif KR, Black Han Sans) → `fonts/`
- [x] `make_sdf.py`로 TTF → SDF JSON + Atlas PNG + Material JSON 생성 (2개 폰트, 4096²)
- [x] 게임 폰트 목록 수동 파악 (23개 TMP FontAsset PathID 목록 확보)
- [ ] **Windows에서 `Unity_Font_Replacer_KO.exe`로 폰트 교체** → [Runbook](runbooks/phase-3-windows-font-injection.md)
- [ ] 수정된 `resources.assets` macOS로 복사
- [ ] macOS 재서명 (`codesign --force --sign -`)
- [ ] 게임 내 한글 출력 확인 (메뉴·카드·툴팁)
- [ ] 잔존 `□`/`ㅁ` 글자 확인 및 누락 문자 추가

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
| SDF 생성 | `make_sdf.py` — NotoSerifKR (point-size 162), BlackHanSans (point-size 192) | ✅ 성공 — 4096² Atlas, 595 glyphs, SDF JSON/Material 정상 |
| 게임 폰트 파악 | UnityPy raw 바이트 파싱 | ✅ 성공 — 23개 TMP FontAsset 확인 |
| 폰트 주입 | Windows `Unity_Font_Replacer_KO.exe` | ⬜ 대기 — [Runbook](runbooks/phase-3-windows-font-injection.md) |
| 게임 테스트 | — | ⬜ 대기 |

## 리스크 (업데이트)

| 리스크 | 대응 |
|---|---|
| ~~`make_sdf.py` 4096² 초과~~ | ✅ 596자로 충분히 수용 (point-size 162) |
| `Unity_Font_Replacer` macOS 미지원 | Windows에서 `.exe` 실행 — [Runbook](runbooks/phase-3-windows-font-injection.md) |
| `Il2CppDumper.exe` 실행 실패 | Windows 환경에 .NET 8.0 Runtime 설치 필요 |
| `resources.assets` 크기 증가 | AssetsTools.NET 기반으로 안전하게 처리 |

## 다음 Phase로 핸드오프

Phase 완료 시 다음 항목을 기록한다.

- Windows 주입 성공 여부 및 사용한 명령어
- 생성된 SDF 아틀라스 크기 및 문자셋 수
- 게임 내 폰트 구성 (교체된 폰트 목록)
- Material 보정값 (필요 시)
- 잔존 `□` 글자 및 누락 문자 목록
- macOS 코드사인 필요 여부
