# Phase 3 — 한글 SDF 폰트 아틀라스 생성

## 상태

- 상태: ⬜ 대기
- 선행 Phase: Phase 2 완료

## 목표

번역문에 실제로 사용되는 한글 글자를 포함한 TMP 호환 SDF 폰트 아틀라스를 생성하고 기존 `resources.assets`의 폰트 에셋에 주입한다. **핵심 도구: [Unity_Font_Replacer](https://github.com/snowyegret23/Unity_Font_Replacer) v1.2.8** (Python, macOS 호환).

## 배경

게임은 TextMeshPro(TMP)로 텍스트를 렌더링한다. TMP는 TTF를 직접 쓰지 않고 SDF(Signed Distance Field) 폰트 아틀라스라는 특수 텍스처를 사용한다. 현재 게임의 SDF 아틀라스는 라틴 문자만 포함하고 있어, 한글을 출력하면 빈 네모(`□`)가 표시된다. (Phase 1에서 확인)

Unity_Font_Replacer는 UnityPy + Pillow 기반으로 TMP SDF 폰트의 생성·추출·교체를 자동화한다. TMP FontAsset의 복잡한 내부 구조(CharacterTable, GlyphTable, Atlas Texture, Material)를 직접 파싱할 필요 없이 도구가 처리한다.

## 도구

| 구성 요소 | 다운로드 | 크기 | 용도 |
|---|---|---|---|
| `Unity_Font_Replacer_v1.2.8.zip` | [Release](https://github.com/snowyegret23/Unity_Font_Replacer/releases/tag/v1.2.8) | 142 MB | `unity_font_replacer_ko.py` — 폰트 교체 |
| `make_sdf_v1.2.8.zip` | [Release](https://github.com/snowyegret23/Unity_Font_Replacer/releases/tag/v1.2.8) | 80 MB | `make_sdf.py` — TTF → SDF 생성 |

요구사항: `pip install UnityPy Pillow numpy scipy fonttools`

## 체크리스트

- [ ] 도구 다운로드 및 설치 (`tools/unity-font-replacer/`에 배치)
- [ ] 번역문에서 사용 글자 문자셋 산출 → `fonts/chars.txt`
- [ ] 폰트 TTF 다운로드 및 라이선스 확인 (Noto Serif KR, Black Han Sans 등) → `fonts/`
- [ ] `make_sdf.py`로 TTF → SDF JSON + Atlas PNG + Material JSON 생성
- [ ] 기존 게임 폰트 parse → `fontmap.json` 확인
- [ ] `unity_font_replacer_ko.py`로 폰트 교체 (원본 백업 → `original/`)
- [ ] macOS 재서명 (`codesign --force --sign -`)
- [ ] 게임 내 한글 출력 확인 (메뉴·카드·툴팁)
- [ ] 잔존 `□`/`ㅁ` 글자 확인 및 누락 문자 추가

## 작업 순서

### 1. 도구 설치

```bash
# tools/unity-font-replacer/ 디렉토리에 압축 해제
cd tools/unity-font-replacer/
unzip Unity_Font_Replacer_v1.2.8.zip
unzip make_sdf_v1.2.8.zip
pip install UnityPy Pillow numpy scipy fonttools
```

### 2. 문자셋 추출

```bash
# translation/strings.json + translation/cards.json의 모든 ko 값에서
# 고유 문자를 추출해 fonts/chars.txt로 저장
python scripts/extract_charset.py
```

### 3. 폰트 준비

| 폰트 | 용도 | 라이선스 | TTF 위치 |
|---|---|---|---|
| Noto Serif KR | 본문 (카드 설명, UI) | OFL | `fonts/NotoSerifKR-Regular.ttf` |
| Black Han Sans | 제목 (카드명) | OFL | `fonts/BlackHanSans-Regular.ttf` |

### 4. SDF 생성

```bash
python tools/unity-font-replacer/make_sdf.py \
  --ttf fonts/NotoSerifKR-Regular.ttf \
  --charset fonts/chars.txt \
  --size 4096 \
  --output fonts/

# → fonts/NotoSerifKR-Regular SDF.json
# → fonts/NotoSerifKR-Regular SDF Atlas.png
# → fonts/NotoSerifKR-Regular SDF Material.json
```

### 5. 게임 폰트 parse

```bash
python tools/unity-font-replacer/unity_font_replacer_ko.py \
  --gamepath "original/" \
  --parse
# → fontmap.json (게임 내 모든 폰트 목록)
```

### 6. 폰트 교체 (injection)

```bash
# 방법 A: oneshot — 단일 폰트로 전체 교체
python tools/unity-font-replacer/unity_font_replacer_ko.py \
  --gamepath "patched/" \
  --font "fonts/NotoSerifKR-Regular.ttf"

# 방법 B: list — JSON 기반 개별 폰트 지정 교체
# fontmap.json의 Replace_to 필드에 교체할 SDF JSON 파일명 지정 후
python tools/unity-font-replacer/unity_font_replacer_ko.py \
  --gamepath "patched/" \
  --list fontmap.json
```

### 7. macOS 재서명

```bash
# IL2CPP 바이너리 및 수정된 모든 파일 재서명
cd patched/
codesign --force --sign - "TwilightStruggle.app"
```

### 8. 게임 테스트

Steam에서 실행하거나 `patched/`를 직접 실행해 한글 출력 확인.

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 문자셋 | 번역 소스에서 실제 사용 글자를 재현 가능하게 추출함 |
| SDF 생성 | `make_sdf.py`가 오류 없이 JSON + Atlas PNG 생성 |
| parse | 게임 폰트 목록이 누락 없이 JSON으로 출력됨 |
| 주입 | 도구가 에셋을 수정하고 게임이 정상 실행됨 |
| 렌더링 | 메뉴·카드·툴팁 등 주요 텍스트에서 한글이 `□` 없이 정상 표시됨 |
| 재서명 | macOS에서 `codesign` 후 실행 가능 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| — | — | ⬜ 대기 |

## 리스크

| 리스크 | 대응 |
|---|---|
| `make_sdf.py`의 4096² 아틀라스에 문자셋 초과 | 사용 글자 수 먼저 확인. 초과 시 분할 또는 필수 글자만 선별 |
| `unity_font_replacer.py`가 Unity 6 IL2CPP 타입트리 미지원 | Unity_Font_Replacer_AT(C#)로 대체하거나 raw 바이트 수동 교체 |
| 아틀라스 용량 증가로 `resources.assets` 전체 재배치 필요 | UnityPy가 파일 크기 변경을 자동 처리하므로 괜찮을 가능성 높음 |
| 게임이 여러 폰트/여러 아틀라스 사용 | parse 결과로 실제 폰트 구성 확인 후 대응 |

## 다음 Phase로 핸드오프

Phase 완료 시 다음 항목을 기록한다.

- 생성된 SDF 아틀라스 크기 및 문자셋 수
- 게임 내 폰트 구성 (`fontmap.json` 요약)
- 교체 방식 (oneshot / list) 및 사용 폰트
- Material 보정값 (필요 시)
- 잔존 `□` 글자 및 누락 문자 목록
- macOS 코드사인 필요 여부
- Phase 4 주입 작업에 필요한 주의사항 (에셋 구조 변경 발생 시)
