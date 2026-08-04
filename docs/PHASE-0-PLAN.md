# Phase 0 실행 계획 — 준비

> 작성일: 2026-02 · 상태: 대기
> 전제: [PLAN.md](PLAN.md) §4 Phase 0

## 현재 상태 (확인 완료)

| 항목 | 상태 |
|---|---|
| 게임 설치 | ✅ v1.4.11, `build-guid=beff29feda834098ab218792d4d80249` |
| Lua 파일 | ✅ 6개 존재 (`twilight_cards.lua` 3,764줄 포함) |
| `resources.assets` | ✅ 14MB |
| git | 초기화됨, 커밋 0개 |
| dotnet | ❌ 미설치 (UABEA 필수) |
| Python | ✅ 3.9.6 (시스템 버전 → venv 권장) |

## Step 1 — 저장소 스켈레톤 + 초기 커밋

```
patched/ original/ translation/ fonts/ scripts/ tools/
```

- `.gitignore`: `original/`, `tools/` 바이너리, `*.resS`
- PLAN §3 구조 그대로 생성

**검증**: `git status` clean + `tree -L 2` 결과가 PLAN §3과 일치

## Step 2 — 도구 설치

| 도구 | 설치 | 검증 방법 |
|---|---|---|
| .NET 8 | `brew install dotnet` | `dotnet --version` ≥ 8.0 |
| UABEA | GitHub 릴리스 zip → `tools/uabea/` | `dotnet UABEA.dll` 기동 확인 |
| Python venv | `python3 -m venv .venv` + numpy/scipy/Pillow | `python -c "import numpy, scipy, PIL"` 성공 |

> AssetRipper는 Phase 1에서 UABEA 파싱 실패 시에만 설치

## Step 3 — 원본 백업 + 버전 고정

- 대상만 `original/`로 복사: `resources.assets`, `level0~3`, `StreamingAssets/`, `globalgamemanagers*` (`.resS` 74MB 제외)
- 해시 기록: `original/hashes.txt` (sha256)
- 버전 정보: `original/VERSION.txt` (v1.4.11, build-guid)

**검증**:

```bash
sha256sum -c hashes.txt  # 원본과 복사본 동일
```

이 해시는 Phase 5 `verify.sh`(버전 불일치 경고)의 기반.

## Step 4 — 기존 패치 확보 (수동 포함)

- 블루칩 블로그 v1.0.1/v2.0.1: https://bluechip2022.tistory.com/2
- 한패 백업: https://hanpe.net/hanguls/t
- 저장 위치: `tools/legacy-patches/` (gitignore)

**검증**: 압축 해제 가능 + 패치 내 수정 파일 목록 식별 (Phase 2 번역 추출 대상)

---

# Phase 1 검증 설계 (실험 프로토콜)

원칙: **한 번에 한 소스만, 표시 식별자로 테스트**

| 실험 | 조작 | 성공 기준 |
|---|---|---|
| A. Lua | `twilight_cards.lua` 카드 이름 하나를 `"테스트카드_KR"`로 변경 | 게임 내 해당 카드 이름이 변경 표시됨 |
| B. 에셋 | UABEA로 `Common_Strings` 또는 `TS_Cards` 문자열 변경 | 게임 내 해당 문자열 변경 표시됨 |
| C. 경로 매핑 | Lua 로더는 `"twilight/database/..."` 참조, 파일은 플랫 → 로드 경로 확인 | 로드 실패 시 Lua는 잔재 파일 판정 |

- 각 실험 후 반드시 `original/`에서 원본 복원 → 게임 정상 동작 확인
- 실험 순서: A(가장 빠름) → C(A 실패 시) → B

**판정 기준**: A 또는 B 중 실게임 반영 확인된 소스가 Phase 2 주 작업 대상.
둘 다 반영되면 `Common_Strings` 우선 (다국어 구조 재사용 가능).
