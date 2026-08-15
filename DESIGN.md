---
name: Twilight Struggle 한글 패치 — 배포 사이트
description: Steam판 Twilight Struggle 한글 패치를 배포하는 해제된 작전 문서 — 냉전 기밀 파일 세계
colors:
  signal-red: "#c8102e"
  red-deep: "#9e0b24"
  red-bright: "#f05a70"
  nato-blue: "#2f5aa8"
  blue-soft: "#3d6bbd"
  navy-cover: "#0a1322"
  navy-panel: "#0e1a2f"
  navy-border: "#20344f"
  dossier-paper: "#e9e0cb"
  paper-deep: "#d9cdb2"
  off-white: "#f7f3e8"
  cream: "#f2ecdc"
  ink: "#20242e"
  ink-soft: "#4a4f5c"
  steel: "#aab4c4"
  steel-dim: "#7e8a9c"
typography:
  display:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(2.6rem, 7.5vw, 5.6rem)"
    fontWeight: 600
    lineHeight: 0.98
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Paperlogy, Pretendard, sans-serif"
    fontSize: "clamp(1.7rem, 3.4vw, 2.5rem)"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: "D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.75
  label:
    fontFamily: "D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.72rem"
    fontWeight: 400
    letterSpacing: "0.14em"
rounded:
  sm: "4px"
spacing:
  xs: "0.35rem"
  sm: "0.75rem"
  md: "1rem"
  lg: "1.6rem"
  xl: "2.5rem"
components:
  button-primary:
    backgroundColor: "{colors.signal-red}"
    textColor: "{colors.off-white}"
    typography: "{typography.headline}"
    rounded: "{rounded.sm}"
    padding: "0.95rem 1.6rem"
  button-primary-hover:
    backgroundColor: "{colors.red-deep}"
  os-card:
    backgroundColor: "{colors.dossier-paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0.85rem 1rem"
  os-card-selected:
    backgroundColor: "{colors.off-white}"
  download-panel:
    backgroundColor: "{colors.navy-cover}"
    textColor: "{colors.cream}"
    rounded: "{rounded.sm}"
    padding: "1.1rem 1.2rem"
  filebox:
    backgroundColor: "{colors.navy-panel}"
    textColor: "{colors.cream}"
    rounded: "{rounded.sm}"
    padding: "1.75rem 1.6rem"
---

# Design System: Twilight Struggle 한글 패치 — 배포 사이트

## Overview

**Creative North Star: "해제된 작전 파일 (The Declassified Dossier)"**

한글 패치라는 제품을 기밀 작전 문서가 공개로 전환된 순간으로 표현한다. 페이지는 네이비 표지로 열리고, 방문자가 스크롤할 때마다 검은 마스킹 바가 벗겨지며 실제 정보가 해제된다. 세계는 냉전 보드게임 Twilight Struggle의 두 가지 재질, 즉 진영 색(파랑 vs 빨강)과 서류(도장·기밀 바·검은 마스킹)로 이뤄진다.

밀도는 중간에서 낮음 사이로, 한 화면에 하나의 주장만 둔다. 장식은 세계의 재질로만 한다: 도트 세계지도, 헤어라인, 붉은 제본 테이프, 고무도장. 평면 인쇄 문법을 지키며, 그라데이션이나 가짜 물리 질감(베벨·엠보싱)은 쓰지 않는다. 액션은 항상 도장이다 — 빨간 도장이 곧 다운로드 버튼이다.

**Key Characteristics:**
- 두 표면 문법: 네이비 표지(진영·어두운 재질)와 크림 서류지(정보·밝은 재질)의 교차
- 액션 = 도장: 회전·점선 외곽선·'찍히는' 호버로 버튼을 고무도장으로 만든다
- 검은 마스킹 리빌: 페이지 진입 시 히어로 제목 줄이 기밀 마스킹 바를 찢고 해제되고, 서류 시트 진입 시에도 마스킹 바가 벗겨진다
- 살아있는 상황판: 히어로 도트 지도 위로 스캔선이 돌고, 육지 위 접촉점이 맥박하며 스캔에 응답한다(Canvas + 커서·스크롤 패럴랙스)
- 도트 세계지도: 파랑(미주)·빨강(유라시아) 진영 도트가 표지 배경을 이룬다
- 세 글자 세계: Oswald(라틴) · Paperlogy(한글) · D2Coding(본문) — 셋만 쓴다

## Colors

두 표면(네이비 표지 / 크림 서류지) 위에 하나의 신호 빨강 가족이 액션을 담당하고, 미군 블루가 지도·진영을 담당한다. 빨강은 표면에 따라 역할이 갈린다 — 아래 Named Rules 참조.

### Primary
- **신호 빨강 (Signal Red)** (#c8102e): 도장·버튼 면, 제본 테이프, 기밀 바. 흰 텍스트와 함께 쓴다 (대비 5.9:1).
- **진한 빨강 (Red Deep)** (#9e0b24): 서류지 위의 빨강 텍스트·링크·상태 표시 (대비 6.6:1).
- **밝은 빨강 (Red Bright)** (#f05a70): 네이비 위의 빨강 텍스트·진행 바·경고 (대비 5.3:1).

### Secondary
- **미군 블루 (NATO Blue)** (#2f5aa8): 서반구 지도 도트와 진영 표시의 파랑. 밝은 단계(blue-soft #3d6bbd)와 함께 쓴다.

### Neutral
- **네이비 표지 (Navy Cover)** (#0a1322): 페이지 바닥·다운로드 패널·명령 블록. 표지 면 위로 navy-panel(#0e1a2f, 철 문서함·올린 면) → navy-border(#20344f, 구분선)으로 층을 쌓는다.
- **서류지 (Dossier Paper)** (#e9e0cb): 서류 섹션 바닥. paper-deep(#d9cdb2)은 판·플레이트 면.
- **먹 (Ink)** (#20242e): 서류지 위 본문·테두리. ink-soft(#4a4f5c)는 부차 텍스트.
- **강철 (Steel)** (#aab4c4): 네이비 위 본문. steel-dim(#7e8a9c)은 부차 텍스트·라벨.
- **크림 (Cream)** (#f2ecdc)·**오프화이트 (Off White)** (#f7f3e8): 네이비 위 강조 텍스트·제목.

### Named Rules
**The Red Context Rule.** 빨강은 표면에 따라 역할이 갈린다: 면(도장·테이프·버튼)은 signal-red, 서류지 위 텍스트는 red-deep, 네이비 위 텍스트는 red-bright. 단색 signal-red를 작은 텍스트에 억지로 쓰지 않는다 — 대비 4.5:1 미만이면 역할을 바꾼다.
**The Two-Surface Rule.** 밝은 텍스트는 네이비 위에만, 어두운 텍스트는 서류지 위에만 둔다. 표면이 바뀌면 텍스트 색도 바뀐다 (steel ↔ ink).

## Typography

**Display Font:** Oswald (500/600, 자체 호스팅, 영문 대문자용)
**Headline Font:** Paperlogy 5 Medium (500/700, 자체 호스팅, 한글 제목용)
**Body Font:** D2Coding (400, 자체 호스팅 — 게임이 실제로 쓰는 본문 폰트)
**Label Font:** D2Coding (파일 라벨·도장·메타, 대문자 + 자간)

**Character:** 게임 자체의 타이포를 그대로 가져온다. 라틴 디스플레이는 응축된 Oswald로 게임 로고의 위압감을, 한글 제목은 Paperlogy로 부드러운 현대 산스의 균형을, 본문은 D2Coding 모노로 '기계가 찍은 문서'의 질감을 낸다.

### Hierarchy
- **Display** (Oswald 600, clamp(2.6rem, 7.5vw, 5.6rem), 0.98): 히어로의 영문 로고 "TWILIGHT STRUGGLE". 대문자·약간 벌린 자간(0.01em).
- **Headline** (Paperlogy 500, clamp(1.7rem, 3.4vw, 2.5rem), 1.15): 섹션 제목·한글 대제목. 자간 -0.02em, text-wrap: balance.
- **Title** (Paperlogy 700, 1.0–1.15rem): OS 카드 이름·FAQ 질문·설치 단계 제목.
- **Body** (D2Coding 400, 1rem, 1.75): 모든 본문. 한 줄 65–75자(36rem)로 제한.
- **Label** (D2Coding 400, 0.72rem, 자간 0.14–0.18em, 대문자): 파일 탭·문서함 머리·메타·도장.

### Named Rules
**The Real-Type Rule.** 세계의 글자는 시스템 폰트로 대체하지 않는다 — Oswald·Paperlogy·D2Coding 셋만 쓴다. 모노는 '기술적' 코스튬이 아니라 게임의 실제 본문 글자다.

## Layout

컨테이너는 `min(1080px, 100% - 3rem)` 단일 컬럼. 히어로와 푸터는 네이비 풀블리드, 서류 구간은 크림 풀블리드로 표면이 번갈아 나온다.

- **히어로**: 단일 컬럼 중앙 정렬 — 제목 + 다운로드 도장뿐. 최소 높이 74vh. 기밀 해제 오프닝(줄 간 0.16s 스태거)이 열리는 무대.
- **서류 (알아두면 좋은 점 · 다운로드 · 설치)**: 데스크톱에서 5fr/7fr 그리드 — 왼쪽 열에 알아두면 좋은 점, 오른쪽 열에 다운로드 + 철 문서함(설치) 적층. 오른쪽 열은 sticky(top 1rem)로 스크롤 동안 고정된다.
- **반응형**: 880px 이하에서 단일 컬럼(다운로드 → 설치 → 알아두면 좋은 점 순), sticky 해제, 메모는 헤어라인으로 분리. 560px 이하에서 OS 탭이 전체 폭, 다운로드 패널이 세로 적층.
- **리듬**: 서류 섹션 패딩 `clamp(3rem, 7vh, 5rem)` — 제목 위 공간이 아래보다 넉넉하다. 조밀 그룹 0.75–1rem, 섹션 간 헤어라인 + 붉은 제본 테이프(5px)로 구분.
- **진행**: 화면 최상단 3px 빨간 스크롤 진행 바(scaleX).

## Elevation & Depth

하이브리드: 어두운 면은 **톤 레이어링**(navy-cover → navy-panel → navy-border)으로, 밝은 면은 **소프트 섀도**로 깊이를 준다. 하드 오프셋 섀도(네오브루탈)는 세계에 없다.

### Shadow Vocabulary
- **paper** (`0 1px 0 rgba(32,36,46,.1), 0 18px 44px -20px rgba(10,19,34,.5)`): 철 문서함 등 떠 있는 면.
- **stamp** (`0 10px 26px -10px rgba(158,11,36,.55)`): 빨간 도장 CTA가 '찍혀' 있음을 강조.

**The Flat-Print Rule.** 서류는 평면이다. 그라데이션·베벨·엠보싱·그레인으로 종이를 흉내 내지 않는다 — 평면 크림 면 + 헤어라인 + 테이프가 재질이다.

## Shapes

- **모서리**: 4px(radius sm). 종이·서류·도장의 깔끔한 모서리 — 카드류 12–16px 둥금은 이 세계에 없다.
- **원형 도장**: 3px 실선 원 + 7px 안쪽 점선 원. -6~8도 회전이 '찍힘'을 만든다.
- **주 CTA**: 사각 도장 — 2px 실선 + 3px 오프셋 점선 외곽선, -1.5도 회전.
- **스캔선**: 히어로 상황판 위를 도는 1px 헤어라인 + 우측 빨간 스윕 헤드 틱.
- **서류 시트**: 상단 5px 붉은 제본 테이프 + 하단 헤어라인.

## Components

### Buttons (도장)
- **Shape:** 4px radius, 회전(-1.5deg), 2px 점선 외곽선(offset 3px).
- **Primary (stamp-btn):** signal-red 배경 · off-white 텍스트 · Paperlogy 700 1.05rem · padding 0.95rem 1.6rem · stamp 섀도.
- **Hover / Focus:** 호버 = scale(1.06) + red-deep 배경 + 회전 증가 — '도장이 다시 찍히는' 느낌. active = scale(0.96). 포커스 = 흰 점선.
- **Secondary:** 텍스트 링크(red-deep, 밑줄 offset 3px)와 미니 도장(stamp-mini, 2px 테두리 0.66rem 대문자)만.

### OS 선택 카드 (radio)
- **Style:** 서류지 배경 · 1px 먹 테두리 · 4px radius · 3열 그리드(글리프/이름/파일명).
- **State:** 선택 = 오프화이트 배경 + 빨간 테두리 + inset 1px 빨강 링. 호버 = 오프화이트. 포커스 = 빨간 점선.

### 다운로드 패널
- **Style:** navy-cover 배경 · 크림 텍스트 · 4px radius · 파일명 모노. 기본 숨김, OS 선택 시 `.on`으로 나타난다.

### 철 문서함 (설치 카드)
- **Style:** navy-panel 배경 · navy-border 테두리 · paper 섀도. 단계 = Oswald 번호(red-bright) + Paperlogy 제목 + steel 본문, 점선 구분.
- **명령 블록:** navy-cover 배경 · 좌측 3px 빨간 바 · 모노 0.74rem · 가로 스크롤 + 복사 버튼(steel → 호버 red).

### 기밀 해제 오프닝 (히어로 시그니처)
- 페이지 진입 시 제목 두 줄을 검은 마스킹 바(하단 들쭉날쭉 clip-path)가 줄 단위로 찢고 올라가며 해제. 줄 간 0.16s 스태거, 다운로드 도장은 1.35s에 '찍히며' 등장. prefers-reduced-motion에서는 마스킹 없이 즉시 표시.

### 살아있는 상황판 (히어로 Canvas)
- 도트맵 위 Canvas 레이어: 7초 주기 스캔 헤어라인 + 육지 위 접촉점 14개(서반구 파랑·동반구 빨강) — 스캔 통과 시 ping 링. 커서에 반구가 반대 방향으로 기울고, 스크롤 시 지도가 느리게 이동. 뷰포트 이탈 시 일시정지, 모션 절감 시 비활성.

## Do's and Don'ts

### Do:
- **Do** 액션은 도장 언어로 만든다: 회전 + 점선 외곽선 + 찍히는 호버.
- **Do** 마스킹 리빌은 실제 정보를 드러내는 데만 쓴다 — 스크롤 후에도 남는 장식용 마스킹은 금지.
- **Do** 빨강 3역할을 지킨다: 면=signal-red, 서류지 텍스트=red-deep, 네이비 텍스트=red-bright.
- **Do** 글자 세계를 지킨다: Oswald / Paperlogy / D2Coding 셋만.
- **Do** 표면이 바뀌면 텍스트 색도 바꾼다 (steel ↔ ink).

### Don't:
- **Don't** 유니코드 글리프·이모지(⬇ ⚠ ▲ ■ 등)를 아이콘 대용으로 쓰지 않는다 — SVG로 직접 그린다.
- **Don't** 본문에 em-dash를 남발하지 않는다 — 한국어 구두점(마침표·가운뎃점)을 쓴다.
- **Don't** 네이비 위 작은 텍스트에 단색 signal-red를 쓰지 않는다 (대비 3:1 미만).
- **Don't** 가짜 물리 질감(베벨·엠보싱·그레인)이나 그라데이션으로 재질을 흉내 내지 않는다.
- **Don't** 증거 없는 계량("설치 약 3분" 등)을 주장하지 않는다 — 사실만.
- **Don't** 시스템 디스플레이 폰트(Impact류)나 하드 오프셋 섀도를 세계에 끌어들이지 않는다.
