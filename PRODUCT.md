# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

- **Astro** (정적 사이트, `output: 'static'` 기본값) — 최신 메이저 v6.x (2026-08, context7 인덱스 기준)
- 배포: **GitHub Pages** — Astro 공식 가이드의 `withastro/action` GitHub Actions 워크플로우 사용
- 저장소는 프로젝트 사이트(`oliverne.github.io/twilight-struggle-kr-patch/`)이므로 `astro.config.mjs`에 `base: '/twilight-struggle-kr-patch/'` 설정 필요 (커스텀 도메인 도입 시 해제)
- 사용자 결정 (2026-08-14): Astro + GitHub Pages

## Users

- 1차 사용자: **한국어로 Twilight Struggle를 즐기고 싶은 일반 플레이어** — Steam 데스크톱판(Windows 10/11, macOS 10.13+, Steam Deck/Linux는 Proton 경유) 사용자
- 기술 지식이 낮은 유저가 전제 — GitHub 저장소·README 문법을 읽지 않음. "OS에 맞는 파일 다운로드 → 압축 해제 → 설치 스크립트 실행"만으로 끝나야 함
- 패치 제작자/유지보수자는 이 사이트의 사용자가 아님 (개발자용 정보는 리포지토리 README·docs에 별도 유지)

## Product Purpose

Steam판 Twilight Struggle(App ID 406290)의 비공식 한글 패치를 일반 유저가 쉽게 발견하고 다운로드·설치하게 하는 **배포 웹사이트**. 성공 = 유저가 몇 분 안에 패치를 받아 설치하고, 게임 전체(카드·메뉴·인게임 UI·규칙북·도움말)를 한글로 즐긴다.

패치 자체(제품의 핵심 산출물)는 이미 완성 — v0.1.2 릴리스, 파일 패치 가능 범위 100% 한글화. 사이트는 그 완성된 패치의 유저용 프론트 도어다.

## Positioning

- **현행 유일한 한글 패치 배포 채널** — 기존 커뮤니티 패치(한식구 카페 런타임 2026-03-15, 블루칩 v1.0.1)는 현재 게임 버전에서 동작하지 않는 구버전. 이 사이트만이 현행 버전을 배포한다.
- GitHub 리포지토리(개발자 대상)와 대비되는 **일반 유저 대상 진입구** — 게임 지식만 있으면 되는 진입 장벽.
- **언어 설정 무조작** — 게임 설정을 건드리지 않고 EN 로케일을 한글로 덮어쓰는 방식. 설치=한글, 제거(원본 복원)=영어. "설치하면 바로 한글"이 차별 지점.

## Operating Context

- 유저는 커뮤니티(한식구 카페 등)·검색 유입 → 사이트에서 본인 OS 확인 → 해당 zip 다운로드
- 설치 흐름: Steam 게임 설치 확인 → zip 압축 해제 → 설치 스크립트 실행(백업 → 복사 → SHA-256 검증 → macOS는 임시 코드 서명) → 게임 실행 → 한글 확인
- **Steam 무결성 확인/게임 업데이트는 패치를 원복시킨다** — 사이트에 재설치 안내가 필요한 반복 상황
- 다운로드 소스: GitHub Releases v0.1.2 — Windows/macOS 사용자용 zip(~9MB) 2종 + 재현용 src zip(~15MB), `SHA256SUMS` 포함
- 게임은 싱글플레이 기준 검증 완료, 멀티플레이 미검증 — 유저에게 사실로만 안내

## Capabilities and Constraints

- 사이트 범위 (사용자 확정): **소개 + 다운로드 + 설치 방법 + 크레딧/라이선스** — 마이크로 캠페인 사이트 성격, 이 이상 확장하지 않는다
- **BepInEx·IL2CPP 등 기술적 세부사항은 유저에게 필요 없음 — 사이트에 노출하지 않는다**
- 패치가 커버하지 못하는 영역은 사실로만 표기: 턴 히스토리 로그·튜토리얼 안내(IL2CPP 코드 문자열, 영어 잔존), 보드맵 구운 문자, 멀티플레이 미검증
- 콘텐츠 언어: 한국어. 간결하고 쉬운 톤
- 정적 사이트(GitHub Pages), 클라이언트 JS 최소화

## Brand Commitments

- 제품명: **"Twilight Struggle 한글 패치"** (게임 제목 그대로 사용)
- **룩앤필: 실제 게임과 비슷한 디자인** (사용자 확정 2026-08-14 — 구체적 시각 방향은 new-work에서 구체화, 이 약속 자체는 확정)
- 톤: 유저 친화적 · 간결 · 쉬움 — GitHub/개발자 용어 금지
- 크레딧 필수 고지: 번역은 신규 런타임 패치(한식구 네이버 카페) 재사용 + 블루칩님 패치 참고 — 원저작자 존중
- 라이선스 체계: 자체 코드·문서 MIT / 번역문은 원저작자 정책 / 게임 자산 저작권은 Playdek·Valve·GMT Games / 폰트(D2Coding·Paperlogy) SIL OFL 1.1

## Evidence on Hand

- GitHub Releases **v0.1.2**: https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.2 — zip 3종 + SHA256SUMS (산출물은 `dist/`, `scripts/package-release.sh`가 생성)
- 설치·제거 스크립트: `scripts/install.sh`(macOS), `install-windows.ps1`(Windows), `uninstall-*` 2종
- 번역 소스: `translation/*.json` (런타임 TSV 2,253쌍 재사용 + 수동 번역)
- **폰트 자산: `fonts/`의 D2Coding·Paperlogy (OFL 1.1) — 웹에서 재사용 가능한 실자산**
- 게임 룩앤필 참조: 패치 적용 게임 화면(메뉴·보드·카드) 실측 가능
- ❗ **스크린샷은 아직 없음** — 패치 적용 게임에서 직접 캡처해야 하며, 허위·가상 이미지로 대체 금지

## Product Principles

1. **일반 유저는 GitHub·설치 스크립트를 이해하지 않는다** — 사이트는 "다운로드 → 압축 해제 → 실행"만 안내한다.
2. **기술적 세부사항(BepInEx·IL2CPP 등)은 사이트에 노출하지 않는다.**
3. **게임의 룩앤필을 존중한다** — 게임의 시각적 정체성과 일관된 디자인을 유지한다.
4. **사실만 말한다** — 미검증(멀티플레이)·미지원(턴 히스토리 등) 영역을 숨기거나 과장하지 않는다.
5. **원저작자 크레딧과 라이선스를 항상 지킨다.**
