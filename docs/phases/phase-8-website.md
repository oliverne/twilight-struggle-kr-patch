# Phase 8 — 배포 웹사이트

## 상태

- 상태: 🚧 진행 중 — 사이트 구축·콘텐츠·CI 수정 **완료**, 공개 배포 **차단**(리포 private + Free 플랜)
- 선행 Phase: Phase 6 완료 (v0.1.2 릴리스, 2026-09-21)
- 착수: 2026-08-14 · 재개(상태 점검·보완): 2026-09-21
- 설계 기준: [`PRODUCT.md`](../../PRODUCT.md), [`DESIGN.md`](../../DESIGN.md)

## 목표

비개발자 유저가 커뮤니티·검색으로 유입해 **몇 분 안에 패치를 내려받아 설치**할 수 있는 공개 사이트를 제공한다. 개발자용 정보(README·docs)는 저장소에 두고, 사이트는 일반 유저 진입구 역할만 한다.

## 체크리스트

- [x] Astro + GitHub Pages 사이트 구축 — Dossier(정보 문서) 세계관, 도트 세계지도, `website/` (`736316f`)
- [x] npm → pnpm 전환 (lockfile·CI 정리) — `5034943`
- [x] 디자인 개편 — 살아있는 상황판 히어로·기밀 해제 연출·기밀 문서 톤 (`fa6a6a9`, `fb6bb82`)
- [x] 콘텐츠 — OS별 다운로드 카드, 설치 안내, FAQ(적용 범위·호환 버전·멀티플레이 사실 고지), 스크린샷 갤러리, 크레딧 (`bd71202`, `63651f9`, `ceece14`)
- [x] 웹폰트 외부화 — D2Coding·Paperlogy를 jsDelivr CDN 로드로 전환 + preconnect (저장소 1.6MB 감소, `d0e2871`)
- [x] 릴리스 버전 연동 — `RELEASE` 상수 `v0.1.2`·용량 표기 갱신 (`7b491e2`)
- [x] CI 워크플로 수정 — pnpm 버전 감지·Pages API 404·Node 20 3건 해결 + private 리포 배포 가드 (`c2f4bfb`, `909f2c3`, `ceffa66`)
- [ ] **GitHub Pages 활성화 + 공개 배포** — ❌ 차단 (아래 블로커)
- [ ] 공개 상태에서 다운로드·설치 링크 실접속 검증
- [ ] 유입 경로 준비 (커뮤니티 공지·검색 노출) — 배포 후

## 블로커 — 리포 private + Free 플랜 (2026-09-21 실측)

- `gh api -X POST repos/.../pages -f build_type=workflow` → **422** `Your current plan does not support GitHub Pages for this repository.`
  → `has_pages: false`, 라이브 URL 404. GitHub Pages는 **private 리포에서 Pro/Team/Enterprise 플랜**이 필요하다.
- 릴리스 자산도 공개 접근 불가 — 로그아웃 상태에서 `releases/download/v0.1.1/...zip` → **404**, 릴리스 페이지 → **404** (private 리포의 Releases는 공개되지 않음)
- 결과: **사이트를 어디에 올려도 다운로드 링크가 동작하지 않는다.** 호스팅 방식 결정이 선행돼야 한다.

| 안 | 내용 | 비용 | 비고 |
| --- | --- | --- | --- |
| A. 리포 공개 전환 | Pages·Releases 즉시 동작, 워크플로 그대로 | 무료 | 게임 파생 에셋(패치 `.assets`·SDF 폰트)이 공개 배포됨 — 패치 자체가 공개 배포 목적이라 의도와는 일치. 저작권 최종 판단은 사용자 결정 |
| B. private 유지 | 사이트는 Cloudflare Pages/Netlify(무료, private 리포 연결) + 다운로드 파일은 별도 공개 저장소·버킷 | 무료 | 워크플로 교체 + 다운로드 소스 이전 필요 |
| C. Pro 업그레이드 | private + Pages | 유료 | Releases 공개 접근은 여전히 불가 → B의 파일 호스팅과 병행해야 함 |

## 배포 구성

```text
website/
├── astro.config.mjs        # site: oliverne.github.io, base: /twilight-struggle-kr-patch/
├── package.json            # packageManager: pnpm@11.21.0 (CI가 이 값을 읽는다)
├── src/layouts/Base.astro  # 웹폰트(CDN)·메타
├── src/pages/index.astro   # 단일 페이지 — RELEASE 상수가 다운로드 URL을 만든다
├── src/styles/global.css
├── public/img/             # 로고·스크린샷·도트 지도 마스크
└── scripts/gen-map.py      # 지도 마스크 생성 보조

.github/workflows/deploy-site.yml   # website/** 변경 시 build → (public일 때만) deploy
다운로드 URL 패턴: releases/download/<RELEASE>/twilight-struggle-kr-patch-<RELEASE>-<os>.zip
```
## 검증 결과

| 항목 | 방법 | 결과 |
| --- | --- | --- |
| 로컬 빌드 | `cd website && pnpm build` | ✅ 성공 — `dist/index.html` 22KB, 정적 라우트 1개 (2026-09-21) |
| 다운로드 링크 생성 | `dist/index.html`에서 v0.1.2 URL grep | ✅ windows·macos 링크 2종 생성 (공개 전환 시 유효) |
| CI 실패 원인 규명 | `gh run view 32153516544 --log-failed` 등 4회 실행 분석 | ✅ 3건: ① `pnpm/action-setup` `No pnpm version is specified`(리포 루트에 package.json 없음) ② `configure-pages` private 리포 Pages API 404 ③ `withastro/action` 기본 Node 20으로 pnpm 11.x 실패(`node:sqlite`) |
| CI 수정 | `package_json_file: website/package.json`, `node-version: 22`, Pages 단계 가드 | ✅ 수정 (`c2f4bfb`, `909f2c3`, `ceffa66`) |
| CI 재실행 | run `35609844485` (main push, 2026-09-21) | ✅ **success** — build 성공(install+build), Pages 단계·deploy는 조건부 skip |
| Pages 활성화 | `gh api -X POST .../pages` | ❌ 422 — 플랜 미지원 (private + Free) |
| 라이브 URL | `curl https://oliverne.github.io/twilight-struggle-kr-patch/` | ❌ 404 |
| 릴리스 자산 공개 접근 | 로그아웃 상태 curl | ❌ 404 (private 리포) |
| 사이트 참조 릴리스 | GitHub Releases `v0.1.2` 3종 업로드·SHA256SUMS 검증 | ✅ 완료 (2026-09-21) |

## 결정 사항

- **Astro + GitHub Pages 유지** (2026-08-14 사용자 결정) — 블로커는 배포 방식(리포 공개 여부)의 문제이며 스택 변경 사유가 아니다.
- **CI는 `!github.event.repository.private` 조건으로 Pages 관련 단계를 전부 게이팅** (configure-pages·upload-pages-artifact·deploy) — public 전환 시 추가 설정 없이 자동 배포되고, private에서는 install+build만 돌아 초록 상태를 유지한다. Pro로 업그레이드해 private + Pages를 쓸 경우 이 조건 3곳을 제거하면 된다. `withastro/action`에는 `node-version: 22`를 명시해야 한다(자체 기본값 20은 pnpm 11.x와 비호환).
- **웹폰트는 jsDelivr CDN 사용** — 저장소에서 woff2 2종 제거(1.6MB), 첫 로드만 외부 의존.
- 사이트가 참조하는 릴리스는 **v0.1.2** — 버전을 올릴 때 `RELEASE` 상수와 용량 표기를 함께 갱신한다(누락 시 다운로드 404).

## 미해결 이슈

- **ISSUES #19** — GitHub Pages·Releases 공개 차단 (private + Free) → 위 블로커. 호스팅 방식 결정 필요.
- **ISSUES #20** — 재현용(src) zip에 `assets-sync.py` 누락 → ✅ 해결 (v0.1.2부터 포함).
- 사이트 FAQ의 스팀데크/Proton 안내는 내부 실기 검증이 아니라 플랫폼 공용 에셋 전제에 근거한 서술이다(유저에게 사실로만 고지).
- 멀티플레이 미검증 — 사이트에도 미검증으로 표기.

## 다음 Phase로 핸드오프

### 즉시 실행할 작업

1. 호스팅 A/B/C 결정 (사용자 결정 필요) → Pages 활성화 또는 호스팅 이전
2. 결정 후 **공개 접속 검증**: 라이브 URL 200 + zip 다운로드 링크 200 + (가능하면) 외부 설치 → 한글 → uninstall → 영어 복귀 1회
3. 검증 결과를 이 문서 `검증 결과` 표에 추가하고 상태를 ✅로 갱신, `PROGRESS.md` 반영

### 결정 사항·산출물

- 사이트 소스 `website/`(git 추적), 릴리스 zip은 `dist/`(gitignore) + GitHub Releases 첨부
- 블로커 해제 전에는 사이트를 공개해도 다운로드가 404다 — 배포 순서 주의(릴리스 공개 → 사이트 배포)

### 주의

- `RELEASE` 상수·README 최신 릴리스 표기·PRODUCT.md 다운로드 소스는 릴리스마다 함께 갱신 (2026-09-21에 v0.1.2로 동기화)
- private 리포에서 `gh release create`는 성공하지만 외부인은 접근할 수 없다는 점을 "배포 완료"로 착각하지 않는다
