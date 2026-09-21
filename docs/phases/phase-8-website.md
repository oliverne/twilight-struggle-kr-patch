# Phase 8 — 배포 웹사이트

## 상태

- 상태: ✅ 완료 (2026-09-21) — 사이트 공개 배포 완료: <https://oliverne.github.io/twilight-struggle-kr-patch/>
- 선행 Phase: Phase 6 완료 (v0.1.2 릴리스, 2026-09-21)
- 착수: 2026-08-14 · 재개(상태 점검·배포): 2026-09-21
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
- [x] CI 워크플로 수정 — pnpm 버전 감지·Pages API 404·Node 20·중복 업로드 4건 해결 (`c2f4bfb`, `909f2c3`, `ceffa66`, `eb9a044`)
- [x] **GitHub Pages 활성화 + 공개 배포** (2026-09-21) — 리포 public 전환(안 A) 후 Pages 활성화, run `35610644379` ✅ (build+deploy)
- [x] 공개 상태에서 다운로드·설치 링크 실접속 검증 — 라이브 200, zip 3종 내려받아 `SHA256SUMS` 전량 일치, **macOS 설치→제거→재설치 라운드트립** 실기 검증
- [ ] 유입 경로 준비 (커뮤니티 공지·검색 노출) — 사이트는 공개됐고, 공지는 미실시

## 블로커 — 리포 private + Free 플랜 → ✅ 안 A로 해결 (2026-09-21)

### 증상 (해결 전 실측)
- `gh api -X POST repos/.../pages -f build_type=workflow` → **422** `Your current plan does not support GitHub Pages for this repository.`
  → `has_pages: false`, 라이브 URL 404. GitHub Pages는 **private 리포에서 Pro/Team/Enterprise 플랜**이 필요하다.
- 릴리스 자산도 공개 접근 불가 — 로그아웃 상태에서 `releases/download/v0.1.1/...zip` → **404**, 릴리스 페이지 → **404** (private 리포의 Releases는 공개되지 않음)
- 결과: 사이트를 어디에 올려도 다운로드 링크가 동작하지 않는 상태였다.

### 선택지와 결정

| 안 | 내용 | 비용 | 결과 |
| --- | --- | --- | --- |
| **A. 리포 공개 전환 (채택)** | Pages·Releases 즉시 동작, 워크플로 그대로 | 무료 | 게임 파생 에셋(패치 `.assets`·SDF 폰트)이 공개 배포됨 — 패치 자체가 공개 배포 목적이라 의도와 일치. 사용자 결정 (2026-09-21) |
| B. private 유지 | 사이트는 Cloudflare Pages/Netlify + 파일은 별도 공개 저장소·버킷 | 무료 | 미채택 |
| C. Pro 업그레이드 | private + Pages | 유료 | 미채택 (Releases 공개 문제는 남음) |

**전환 전 감사 (2026-09-21)**: 추적 파일 309개에서 시크릿·토큰·키 0건, 이메일·개인정보 0건 (`website/.impeccable` 세션 로그는 미추적 확인). 로컬 절대 경로 1건(`gen-map.py` docstring)은 제거 후 전환(`8a81197`).

**전환 절차**: `gh repo edit --visibility public` → `gh api -X POST .../pages -f build_type=workflow` → 평소대로 `git push` (워크플로 가드가 자동으로 참이 되어 build+deploy 실행)

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

.github/workflows/deploy-site.yml   # website/** 변경 시 build → deploy (private이면 Pages 단계는 자동 skip)
다운로드 URL 패턴: releases/download/<RELEASE>/twilight-struggle-kr-patch-<RELEASE>-<os>.zip
```
## 검증 결과

| 항목 | 방법 | 결과 |
| --- | --- | --- |
| 로컬 빌드 | `cd website && pnpm build` | ✅ 성공 — `dist/index.html` 22KB, 정적 라우트 1개 (2026-09-21) |
| 다운로드 링크 생성 | `dist/index.html`에서 v0.1.2 URL grep | ✅ windows·macos 링크 2종 생성 (공개 전환 시 유효) |
| CI 실패 원인 규명 | `gh run view 32153516544 --log-failed` 등 5회 실행 분석 | ✅ 4건: ① `pnpm/action-setup` `No pnpm version is specified`(리포 루트에 package.json 없음) ② `configure-pages` private 리포 Pages API 404 ③ `withastro/action` 기본 Node 20으로 pnpm 11.x 실패(`node:sqlite`) ④ 워크플로의 중복 아티팩트 업로드 → **409 Conflict** |
| CI 수정 | `package_json_file` 지정, `node-version: 22`, Pages 단계 가드, 중복 업로드 제거 | ✅ 수정 (`c2f4bfb`, `909f2c3`, `ceffa66`, `eb9a044`) |
| CI private 모드 | run `35609844485` | ✅ success — build 성공, Pages 단계·deploy는 조건부 skip |
| Pages 활성화 | public 전환 후 `gh api -X POST .../pages -f build_type=workflow` | ✅ 활성화 — `build_type: workflow`, `html_url: https://oliverne.github.io/twilight-struggle-kr-patch/` |
| 사이트 배포 | run `35610644379` (main push) | ✅ **success** — build+deploy 두 job 모두 성공 |
| 라이브 접속 | `curl -o /dev/null -w %{http_code}` | ✅ **200** — HTML 22KB, `v0.1.2` 표기 확인 |
| 사이트 자산 로딩 | CSS·이미지 4종 URL curl (base 경로 검증) | ✅ 전부 200 (`/_astro/*.css`, `/img/*.webp`, `/img/*.jpg`) |
| 릴리스 공개 접근 | 로그아웃 상태 curl (repo·릴리스 페이지·zip URL) | ✅ 전부 **200** (수정 전 404) |
| 다운로드 무결성 | 공개 URL에서 zip 3종 내려받아 내부 `SHA256SUMS` 검증 | ✅ windows 10건 / macos 11건 / src 45건 **실패 0** |
| **설치 라운드트립 (실기)** | 내려받은 macOS zip의 `install.sh` → `uninstall.sh` → `install.sh` | ✅ 설치=패치본 해시 5/5 일치, 제거=원본 해시 일치(`.bak` 유지), 재설치=패치본 일치 + 애드혹 서명(`unity.Playdek.TwilightStruggle`) |
| 사이트 참조 릴리스 | GitHub Releases `v0.1.2` 3종 업로드·검증 | ✅ 완료 (2026-09-21) |

## 결정 사항

- **Astro + GitHub Pages 유지** (2026-08-14 사용자 결정) — 블로커는 배포 방식(리포 공개 여부)의 문제이며 스택 변경 사유가 아니다.
- **리포 public 전환 (2026-09-21, 사용자 결정)** — 안 A. 사이트·Releases 공개 접근 문제를 한 번에 해결했고 비용은 없다(안 B·C 미채택).
- **CI는 `!github.event.repository.private` 조건으로 Pages 단계를 게이팅** — public이 된 지금은 항상 참이라 기존 배포 흐름이 그대로 돈다. private으로 되돌리거나 Pro로 업그레이드할 때 이 가드가 있으면 build 검증은 계속 돌아간다.
- **Pages 아티팩트 업로드는 withastro/action에 일임** — 별도 `upload-pages-artifact` 스텝을 두면 409 Conflict. `withastro/action`에는 `node-version: 22`를 명시해야 한다(기본값 20은 pnpm 11.x와 비호환).
- **웹폰트는 jsDelivr CDN 사용** — 저장소에서 woff2 2종 제거(1.6MB), 첫 로드만 외부 의존.
- 사이트가 참조하는 릴리스는 **v0.1.2** — 버전을 올릴 때 `RELEASE` 상수와 용량 표기를 함께 갱신한다(누락 시 다운로드 404).

## 미해결 이슈

- **ISSUES #19** — GitHub Pages·Releases 공개 차단 (private + Free) → ✅ **해결**: 안 A(리포 public 전환, 2026-09-21) — Pages·Releases·사이트 모두 공개 접근 200
- **ISSUES #20** — 재현용(src) zip에 `assets-sync.py` 누락 → ✅ 해결 (v0.1.2부터 포함).
- 커뮤니티 공지·검색 노출 미실시 — 사이트는 공개됐지만 유입 경로는 아직 없다.
- 사이트 FAQ의 스팀데크/Proton 안내는 내부 실기 검증이 아니라 플랫폼 공용 에셋 전제에 근거한 서술이다(유저에게 사실로만 고지).
- 멀티플레이 미검증 — 사이트에도 미검증으로 표기.

## 다음 작업 (핸드오프 — 프로젝트 마감)

### 남은 작업 (선택)

1. **유입 경로** — 커뮤니티(한식구 카페 등) 공지·검색 노출. 사이트·다운로드는 이미 공개 상태라 바로 가능하다.
2. **외부 사용자 검증** — 내부에서는 라운드트립(설치→제거→재설치)까지 확인했으나, 다른 PC·Windows 실기 설치 확인은 미실시.
3. 계층 3(턴 히스토리·튜토리얼 안내) 한글화 — BepInEx 런타임 훅 별도 프로젝트 (ISSUES #11·#17).

### 재배포 시 주의

- `RELEASE` 상수·README 최신 릴리스 표기·PRODUCT.md 다운로드 소스는 릴리스마다 함께 갱신 (2026-09-21에 v0.1.2로 동기화).
- 사이트 변경은 `main`에 push하면 자동 배포된다(`website/**` 경로 트리거). 배포 확인: `gh run list` → 라이브 URL curl.
- 릴리스를 먼저 올리고 사이트 버전 상수를 나중에 올리면 그 사이 다운로드가 404다 — 순서(릴리스 → 사이트 버전 → 배포)를 지킨다.
- 워크플로에 Pages 업로드 스텝을 다시 추가하지 않는다 — `withastro/action`이 이미 업로드하므로 409 Conflict가 난다.
