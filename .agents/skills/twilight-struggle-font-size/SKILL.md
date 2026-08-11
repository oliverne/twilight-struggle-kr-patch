---
name: twilight-struggle-font-size
description: Twilight Struggle 한글 패치의 TMP SDF 폰트(본문 D2Coding / 제목 Paperlogy 등) 렌더링 크기를 조절하는 절차. SDF 재생성 없이 JSON의 m_PointSize 수정 + 재주입으로 글자 크기를 축소/확대하고, UnityPy raw 파싱으로 실제 반영을 검증한다. 폰트 크기 변경 요청 시 사용.
---

# Twilight Struggle 한글 패치 — 폰트 크기 조절

## 배경 (핵심 지식)

- 게임의 24개 TMP 폰트에 한글 SDF 2종이 매핑돼 있음
  - 본문: `NotoSerifKR SDF` → D2Coding (KR_ASSETS 파일명 유지)
  - 제목: `BlackHanSans-Regular SDF` → Paperlogy (KR_ASSETS 파일명 유지)
- ⚠️ **m_Scale은 절대 경로가 아니다**: Unity_Font_Replacer core(`unity_font_replacer_core.py`의
  `_NEW_LINE_METRIC_KEYS`)가 주입 시 `m_Scale`과 line metrics(lineHeight/ascent 등)를
  **게임 원본 폰트 값으로 강제 덮어쓴다.** SDF JSON에서 m_Scale을 바꿔도 실제로는 적용되지 않는다
  (verify에서 폰트/텍스처 변경 0건으로 드러남).
- ✅ **m_PointSize는 보존된다**: 덮어쓰기 목록에 없어 우리 값이 그대로 주입된다.
  TMP 렌더링 공식 `fontScale = fontSize / pointSize × scale`에 따라
  **m_PointSize를 키우면 글자가 작아진다** (반비례).
- 도구가 line metrics를 `교체 pointSize / 게임 pointSize` 비율로 자동 보정하므로
  **글자만 축소되고 줄 간격은 유지된다** (비례 축소가 아님).

## 사전 준비

- Windows 게임 설치본 + 가상 폴더(`tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/`)
- `PYTHONIOENCODING=utf-8` + venv python: `.venv/Scripts/python.exe`
- 주입 전 `patched/resources.assets`가 가상 폴더와 동일한지 확인:
  `sha256sum patched/resources.assets "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/resources.assets"`

## 절차

### 1. SDF JSON의 m_PointSize 수정 (SDF 재생성 불필요)

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -c "
import json
for name in ['D2Coding-Ver1.3.3-20260725', 'Paperlogy-5Medium']:
    path = f'fonts/{name} SDF.json'
    data = json.load(open(path, encoding='utf-8'))
    data['m_FaceInfo']['m_PointSize'] = 77  # 아래 계산 참고
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
"
```

- **수식**: 새 PointSize = 현재 PointSize ÷ (1 − 축소율)
  - 10% 축소 = 70 ÷ 0.9 = **77.78** → 도구가 `int()`로 정수화하므로 **77** 사용 (실제 9.1% 축소)
  - 15% 축소 = 70 ÷ 0.85 = 82.35 → **82**
  - 확대 시: 10% 확대 = 70 × 1.1 = **77**
- ⚠️ 정수화 주의: JSON에 소수를 적어도 int로 잘리므로 처음부터 정수로 지정한다
- 제목/본문은 각각 다른 수치 지정 가능

### 2. KR_ASSETS 교체

```bash
cp "fonts/D2Coding-Ver1.3.3-20260725 SDF.json" "tools/unity-font-replacer/KR_ASSETS/NotoSerifKR SDF.json"
cp "fonts/Paperlogy-5Medium SDF.json" "tools/unity-font-replacer/KR_ASSETS/BlackHanSans-Regular SDF.json"
```

### 3. 가상 폴더 준비

```bash
cp patched/resources.assets "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/resources.assets"
mv "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/Managed" \
   "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/Managed.off"
```

### 4. 주입 (font-output-<날짜>는 매번 새로)

```bash
cd tools/unity-font-replacer
echo "" | ./unity_font_replacer_ko.exe --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" --parse
PYTHONIOENCODING=utf-8 ../../.venv/Scripts/python.exe ../../scripts/apply_font_mapping.py
echo "" | ./unity_font_replacer_ko.exe \
  --gamepath "C:/.../tools/font-inject-work/Twilight Struggle" \
  --list "Twilight Struggle.json" \
  --output-only "C:/.../tools/font-inject-work/font-output-<날짜>"
```

### 5. 검증

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/verify_assets.py \
  --orig patched/resources.assets --patched "tools/font-inject-work/font-output-<날짜>/resources.assets"
```

- 성공 기준: m_Script 0건, TextAsset 0건, 폰트/텍스처 변경은 **0이 아닌 값**이어야 함
  (m_PointSize가 반영되면 폰트 20여 건이 잡힘. 변경 0건이면 m_PointSize가 실제로 안 들어간 것)

### 6. 에셋 raw로 실제 반영 확인 (UnityPy raw 파싱)

verify만으로는 m_FaceInfo 값이 안 잡힐 수 있으므로 반드시 아래 스크립트로 확인:

```python
# m_FaceInfo float 변경 위치 출력 (70.0 -> 77.0 확인)
import struct, UnityPy
def f32(d, o): return struct.unpack_from('<f', d, o)[0]
env = UnityPy.load('tools/font-inject-work/font-output-<날짜>/resources.assets')
for obj in env.objects:
    if obj.path_id in (30683, 30688):  # 제목/본문 대표 폰트
        raw = obj.get_raw_data()
        for off in range(0, len(raw) - 4, 4):
            v = f32(raw, off)
            if abs(v - 77.0) < 0.001:
                print(f'PathID {obj.path_id} +{off}: m_PointSize=77.0 확인')
```

### 7. 설치

```bash
GAME="D:/Games/steamapps/common/Twilight Struggle/TwilightStruggle_Data"
cp "$GAME/resources.assets" "$GAME/backup-20260812/resources.assets.pre-scale90"   # 이전본 백업
cp tools/font-inject-work/font-output-<날짜>/resources.assets "$GAME/resources.assets"
cp tools/font-inject-work/font-output-<날짜>/sharedassets0.assets "$GAME/sharedassets0.assets"
cp tools/font-inject-work/font-output-<날짜>/resources.assets patched/resources.assets
cp tools/font-inject-work/font-output-<날짜>/sharedassets0.assets patched/sharedassets0.assets
sha256sum patched/*.assets patched/level1 patched/level2 patched/level3 > patched/hashes.txt
mv "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/Managed.off" \
   "tools/font-inject-work/Twilight Struggle/TwilightStruggle_Data/Managed"
```

## 주의사항

- ⚠️ **m_Scale 수정은 무의미**: 도구가 게임 값으로 덮어쓰므로 SDF JSON에서 바꾸지 말 것
  (에셋을 직접 수정하려면 UnityPy로 FontAsset 필드를 바꾸는 별도 도구 필요 — 비권장)
- ⚠️ **한 번에 큰 폭 변경 금지**: 5~10% 단위로 조절하고 실게임 확인 후 미세 조정
- ⚠️ 글자만 작아지고 줄 간격은 유지된다. 줄 간격까지 줄이려면 도구 포크 수정 필요 (비권장)
- 원복: `D:/Games/.../backup-20260812/resources.assets.pre-scale90` 복사 (크기 조절 전)
- 관련 문서: `docs/runbooks/phase-3-windows-font-injection.md`, 이 스킬의 상위 절차는
  `twilight-struggle-font-swap` (폰트 자체 교체 시)
