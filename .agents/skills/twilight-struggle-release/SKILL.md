---
name: twilight-struggle-release
description: Twilight Struggle 한글 패치 배포(Phase 6) 절차. 플랫폼별(windows/macos) 패치 완성 조건 확인 → package-release.sh로 zip 3종 생성 → 산출물 검증 → GitHub Releases 업로드까지. 배포/릴리스 요청 시 사용. (패치 재생성은 twilight-struggle-update, 주입은 twilight-struggle-font-injection 참조)
---

# Twilight Struggle 한글 패치 — 배포(Release) 절차

## 배경

- 배포는 **플랫폼별로 분리**된 패치본 기준 (2026-08-14 확정)
  - `patched/windows/` — Windows 원본 기준 (install-windows.ps1이 사용)
  - `patched/macos/` — macOS 원본 기준 (install.sh가 사용)
  - ⚠️ level1~3(씬)은 플랫폼별 — 교차 복사 시 크래시 (2026-08-12 실측)
- `patched/*/*.assets`는 GitHub 100MB 제한으로 gitignore지만 **zip 압축 시 104MB → ~8MB**라 Releases 첨부(파일당 2GB)로 충분
- 원본 문서: `docs/phases/phase-6-release.md` (체크리스트 원본)

## 사전 조건 (게이트 — 미충족 시 배포 금지)

각 플랫폼에 대해:

- [ ] `patched/<플랫폼>/`에 5종 존재: `resources.assets`, `sharedassets0.assets`, `level1`, `level2`, `level3`, `hashes.txt`
- [ ] verify_assets.py 검증 통과: `m_Script 불일치 0건`, TextAsset 0건 (주입 직후 기준)
- [ ] 실게임 확인 완료: 메뉴·카드·인게임 UI 한글, 폰트 정상 (언어=EN 기본값에서)
- [ ] hashes.txt가 현재 patched 파일과 일치: `sha256sum -c patched/<플랫폼>/hashes.txt`
- [ ] 알려진 한계 문서화: 턴 히스토리/튜토리얼(계층 3) 영어 — ISSUES #11·#17
- [ ] (배포 전 정리) LICENSE 존재 — 폰트 OFL + 기존 패치 번역 크레딧은 LICENSE [2][5]항과 README '감사의 말' 섹션에 포함 (CREDITS.md 별도 파일 없음)

## 절차

### 1. 사전 검증

```bash
# patched 파일 ↔ hashes.txt 일치 확인 (플랫폼별 — hashes.txt는 폴더 내부 기준 경로)
(cd patched/windows && sha256sum -c hashes.txt)   # Windows
(cd patched/macos && sha256sum -c hashes.txt)     # macOS (존재 시)

# m_Script 무손상 재확인 (선택 — 주입 직후 이미 검증했다면 생략 가능)
.venv/Scripts/python.exe scripts/verify_assets.py --orig <원본> --patched patched/<플랫폼>/resources.assets
```

### 2. 패키징

```bash
./scripts/package-release.sh v0.1.0
# → dist/twilight-struggle-kr-patch-v0.1.0-windows.zip   (Windows 사용자용 ~9MB)
# → dist/twilight-struggle-kr-patch-v0.1.0-macos.zip     (macOS 사용자용 ~9MB)
# → dist/twilight-struggle-kr-patch-v0.1.0-src.zip       (재현용 ~3MB)
```

- 존재하지 않는 플랫폼 폴더는 **경고 후 자동 스킵** — 두 플랫폼 모두 배포하려면 둘 다 패치 완성 필수
- 해시는 sha256sum/shasum 자동 선택, 압축은 Python zipfile (전 플랫폼 호환)

### 3. 산출물 검증

```bash
# zip 내부 구조 확인 (플랫폼별 파일이 정확히 들어갔는지)
python -m zipfile -l dist/twilight-struggle-kr-patch-v0.1.0-windows.zip | grep -E "patched|scripts|README" | head
# Windows zip: install-windows.ps1 / uninstall-windows.ps1 포함
# macOS zip:   install.sh / uninstall.sh / restore-original.sh 포함

# SHA256SUMS 검증 (압축 해제 후)
unzip -q dist/*.zip -d /tmp/rel-check && (cd /tmp/rel-check/* && sha256sum -c SHA256SUMS)
```

- 원본 게임 파일(Steam 설치본의 다른 에셋)이 포함되지 않았는지 확인
- 개인 파일(레지스트리 덤프 등) 미포함 확인

### 4. GitHub Releases 업로드

```bash
gh release create v0.1.0 \
  dist/twilight-struggle-kr-patch-v0.1.0-windows.zip \
  dist/twilight-struggle-kr-patch-v0.1.0-macos.zip \
  dist/twilight-struggle-kr-patch-v0.1.0-src.zip \
  --title "v0.1.0" --notes "..."
```

- 릴리스 노트에 포함할 내용: 지원 플랫폼(Windows/macOS/스팀덱·Linux Proton), 알려진 한계(턴 히스토리·튜토리얼 영어), 설치/제거 방법 요약, 기존 패치 제작자 크레딧

### 5. 배포 후 확인 (사용자 관점)

- [ ] 배포 zip을 받은 사용자가 설치 → 한글 확인 → 제거 → 영어 복귀되는지 (uninstall 검증)
- [ ] Steam 무결성 검사 시나리오: 파일 원복 시 영어로 돌아가고 `${Key}` 노출이 없는지 (언어 설정 무조작 덕분에 자연 해결)
- [ ] 알려진 이슈와 지원 게임 버전 명시 확인

## 주의사항

- ⚠️ **플랫폼 zip 교차 금지**: macOS zip을 Windows에, Windows zip을 macOS에 적용하지 않도록 README·릴리스 노트에 명시 (level1~3 크래시)
- ⚠️ **스팀덱/리눅스(Proton)**: Windows 배포본을 그대로 사용 — 별도 zip 불필요 (README에 안내)
- ⚠️ **언어 설정 무조작 방식** (2026-08-14): 설치 스크립트가 레지스트리/plist를 건드리지 않음 — 설치=한글, 제거=영어. 사용자 안내에서 언어 설정 관련 조작을 제거할 것
- ⚠️ 배포 zip에는 LICENSE가 `LICENSE.txt`로 자동 포함된다 (package-release.sh가 복사) — 별도 CREDITS.md는 두지 않고 LICENSE [2][5]항 + README '감사의 말'로 대체
- Steam 업데이트로 패치가 무효화되면 `twilight-struggle-update` 스킬로 재적용
