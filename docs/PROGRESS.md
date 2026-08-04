# 진행 상황 (Progress)

> Phase 진행 시 **이 문서를 항상 함께 업데이트**한다. (규칙: AGENTS.md)
> 상태 표기: ✅ 완료 · 🚧 진행 중 · ⬜ 대기 · ❌ 실패/보류

## 현재 상태

**Phase 0 — 준비** (🚧 진행 중) · 최종 업데이트: 2026-08-04

---

## Phase 0 — 준비

- [x] Git 저장소 초기화
- [x] 저장소 디렉터리 스켈레톤 + `.gitignore` (commit `0abad37`)
- [x] 게임 설치 확인: v1.4.11, build-guid `beff29feda834098ab218792d4d80249`
- [ ] .NET 8 설치 (`brew install dotnet`)
- [ ] UABEA 설치 → `tools/uabea/` + 기동 확인
- [ ] Python venv + numpy/scipy/Pillow 설치
- [ ] 원본 백업 → `original/` (resources.assets, level0~3, StreamingAssets, globalgamemanagers*)
- [ ] `original/hashes.txt` (sha256) + `original/VERSION.txt` 기록
- [ ] 기존 패치 다운로드 (블루칩 v1/v2, 한패) → `tools/legacy-patches/`

## Phase 1 — 텍스트 위치 검증

- [ ] 실험 A: Lua 카드 이름 변경 → 실게임 반영 확인
- [ ] 실험 C: Lua 로드 경로 매핑 확인 (A 실패 시)
- [ ] 실험 B: UABEA로 `Common_Strings` / `TS_Cards` 문자열 변경 → 실게임 반영 확인
- [ ] 살아있는 텍스트 소스 확정 → 주 작업 대상 기록

## Phase 2 — 문자열 추출 & 번역 소스 구축

- [ ] 영문 문자열 추출 → `translation/` JSON
- [ ] 기존 패치에서 한글 번역 추출
- [ ] 자동 매칭 (기존 번역 ↔ 현재 문자열)
- [ ] 용어 통일표 `translation/glossary.md`
- [ ] TMP 리치텍스트 태그 보존 규칙 수립

## Phase 3 — 한글 SDF 폰트 아틀라스 생성

- [ ] 사용 글자 문자셋 산출
- [ ] 대체 폰트 준비 (Noto Serif KR, Black Han Sans, Gugi, 나눔손글씨)
- [ ] SDF 아틀라스 생성 (`make_sdf.py` 우선, 실패 시 Unity Editor)
- [ ] 아틀라스 주입 (UABEA) + 게임 내 한글 출력 확인

## Phase 4 — 텍스트 주입 & 레이아웃 조정

- [ ] 번역 주입 스크립트 (반복 적용 가능)
- [ ] 레이아웃/줄바꿈 조정
- [ ] 튜토리얼·규칙 문서 번역

## Phase 5 — 플랫폼 적용 & 테스트

- [ ] macOS: `scripts/install-mac.sh` + codesign 재서명 테스트
- [ ] Windows: `scripts/install-windows.ps1` 테스트
- [ ] 멀티플레이 동작 테스트
- [ ] Steam 무결성 확인 후 재설치 테스트

## Phase 6 — 배포

- [ ] README 사용자 안내
- [ ] GitHub Releases / zip 배포
- [ ] 기존 패치 제작자 크레딧·연락

---

## 로그

| 날짜 | 내용 | 커밋 |
|---|---|---|
| 2026-08-04 | 프로젝트 계획서·에이전트 지침 작성 | `915feb2` |
| 2026-08-04 | 저장소 스켈레톤 + `.gitignore` | `0abad37` |
