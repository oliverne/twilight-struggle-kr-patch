---
name: Twilight Struggle 한글 패치 — 배포 사이트
description: Steam판 Twilight Struggle 한글 패치를 배포하는 빛바랜 냉전 작전 문서 — 오래된 지도와 봉투형 서류의 세계
colors:
  signal-red: "#c71d22"
  red-deep: "#5d1916"
  red-bright: "#ef6a6e"
  nato-blue: "#2a5999"
  blue-soft: "#738f9a"
  navy-cover: "#17191e"
  navy-panel: "#1f2027"
  navy-border: "#5a6164"
  board-sea: "#738f9a"
  dossier-paper: "#c8c6a8"
  paper-deep: "#9f925b"
  off-white: "#f7f5ed"
  cream: "#dae5eb"
  ink: "#1f2027"
  ink-soft: "#3d4848"
  steel: "#c0c6be"
  steel-dim: "#9c9fa0"
  map-gold: "#c5af3f"
  map-green: "#5d9e4f"
  logo-black: "#050607"
typography:
  headline:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "clamp(1.7rem, 3.4vw, 2.5rem)"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  title:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1.15rem"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  action:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1.05rem"
    fontWeight: 700
    lineHeight: 1.15
  patch-label:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.08em"
  logo-wordmark:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(1.8rem, 7.8vw, 6rem)"
    fontWeight: 600
    lineHeight: 0.82
    letterSpacing: "0.01em"
  logo-wordmark-ko:
    fontFamily: "Paperlogy, Apple SD Gothic Neo, sans-serif"
    fontSize: "0.88em"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.015em"
  archive-title:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1.35rem"
    fontWeight: 400
    lineHeight: 1.15
  body:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.75
  body-sm:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.82rem"
    fontWeight: 400
    lineHeight: 1.7
  caption:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.78rem"
    fontWeight: 400
    lineHeight: 1.6
  fine:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.7
  annotation:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.66rem"
    fontWeight: 400
    lineHeight: 1.5
  micro:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.58rem"
    fontWeight: 400
    lineHeight: 1.45
  step-number:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "1.35rem"
    fontWeight: 400
    lineHeight: 1
  label:
    fontFamily: "YKompyuta, D2Coding, SF Mono, Consolas, monospace"
    fontSize: "0.72rem"
    fontWeight: 400
    letterSpacing: "0.14em"
rounded:
  xs: "0"
  sm: "1px"
  md: "2px"
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
    typography: "{typography.action}"
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
    backgroundColor: "{colors.dossier-paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xs}"
    padding: "1.15rem 0 0"
---

# Design System: Twilight Struggle 한글 패치 — 배포 사이트

## Overview

**Creative North Star: "해제된 작전 파일 (The Declassified Dossier)"**

한글 패치라는 제품을 봉인이 풀린 냉전 작전 서류로 표현한다. 페이지는 거칠게 복사된 철색 파일 커버로 열리고, 제목이 파일 가장자리 안에서 인양되며 정보가 해제된다. 이어지는 본문은 위경도선과 빛바랜 세계지도가 인쇄된 청회색 작전판 위에 펼친 카키 봉투형 문서다. 공식 로고의 빨강·검정, 진영 색, 아프리카 지역의 바랜 카키가 낡은 종이 섬유와 복사 얼룩으로 이어진다.

밀도는 중간에서 낮음 사이로, 한 화면에 하나의 주장만 둔다. 장식은 세계의 재질로만 한다: 오프셋 망점 세계지도, 위경도선, 아카이브 종이 스캔, 봉투 접힘선, 사건 메타, 고무도장. 실제 스캔 질감은 표면마다 혼합 강도만 달리해 반복 사용하고, 광택 그라데이션·베벨·엠보싱은 쓰지 않는다. 액션은 항상 도장이다 — 빨간 도장이 곧 다운로드 버튼이다.

**Key Characteristics:**
- 두 표면 문법: 거친 철색 파일 커버와 작전 지도 위에 펼친 카키 봉투형 서류
- 텍스트 워드마크: Oswald로 로고 구조를 재현하고 TWILIGHT는 빨간 블록, STRUGGLE은 검정 트랙 위 빨강으로 표현
- 액션 = 도장: 회전·점선 외곽선·'찍히는' 호버로 버튼을 고무도장으로 만든다
- 클리핑 리빌: 페이지 진입 시 제목이 부모 영역 안에서 아래에서 위로 인양되며, 별도 찢김 오버레이나 하단 잔상을 남기지 않는다. 한글은 글리프 중간을 자르는 와이프 없이 한 번에 인쇄하고, 완료 뒤 필터·변형·클리핑 합성 레이어를 남기지 않아 선명하게 렌더링한다
- 해제된 기록물: 히어로는 실시간 추적·레이더 효과 없이 이미 분류가 끝난 1970년대 정보기관 파일 표지다
- 냉전 대치 지도: 파랑(서반구)과 빨강(동반구) 인쇄판을 강한 대비로 나누고 몇 픽셀 어긋나게 겹친다
- 사건 메타: CASE NO.·DATE RELEASED·DISTRIBUTION·DECLASSIFIED를 실제 서류 필드처럼 비대칭 배치한다
- 아카이브 표면: 무문자 종이 스캔의 섬유·복사 얼룩·스크래치를 표지, 지도, 서류, 푸터에 같은 계보로 적용한다
- 작전판: 청회색 바닥에 세계지도 윤곽, 30도 간격을 연상시키는 위경도 격자, 바랜 인쇄 농도를 겹친다
- 봉투형 문서: 상단의 큰 삼각 덮개 접힘선, 점선 봉합선, 접힌 귀퉁이로 개봉된 마닐라 봉투를 만든다
- 단일 문서 글자: 텍스트 로고만 Oswald(영문)·Paperlogy(한글), 나머지 제목·본문·번호·버튼·라벨은 모두 YKompyuta를 쓴다. D2Coding은 로딩 실패 시 폴백이다

## Colors

철색 파일 커버와 카키 작전 서류를 게임 보드의 청회색 바다 위에 놓는다. 게임 로고의 빨강이 액션을 담당하고, 미국 진영의 블루와 아프리카 보드의 카키·골드·그린은 표면과 보조 상태를 담당한다. 팔레트의 주요 값은 제공된 영문 게임 스크린샷에서 직접 추출했다.

### Primary
- **신호 빨강 (Signal Red)** (#c71d22): 공식 로고의 빨강. 도장·버튼 면, 제본 테이프, 기밀 바에 사용한다.
- **진한 빨강 (Red Deep)** (#5d1916): 소련 보드에서 추출한 어두운 빨강. 작전 서류 위 링크·도장에 쓴다.
- **밝은 빨강 (Red Bright)** (#ef6a6e): 철색 상황판 위의 빨강 텍스트·진행 바·경고.

### Secondary
- **미군 블루 (NATO Blue)** (#2a5999): 미국 진영에서 추출한 파랑. 서반구 지도 도트와 진영 표시에 쓴다.
- **보드 바다 (Board Sea)** (#738f9a): 게임 화면의 가장 넓은 면. 작전 서류 바깥 캔버스를 전담한다.
- **보드 골드·그린** (#c5af3f / #5d9e4f): 아시아·남미 보드에서 추출한 보조색. 작은 상태와 문서 표식에만 제한한다.

### Neutral
- **철색 표지 (Navy Cover)** (#17191e): 히어로 바닥. navy-panel(#1f2027)은 게임 하단 레일과 다운로드 패널, navy-border(#5a6164)는 금속 구분선이다.
- **작전 서류 (Dossier Paper)** (#c8c6a8): 다운로드·설치·도움말을 담는 단일 문서. paper-deep(#9f925b)은 탭과 눌린 면이다.
- **먹 (Ink)** (#1f2027): 서류 위 본문·테두리. ink-soft(#3d4848)는 부차 텍스트.
- **강철 (Steel)** (#c0c6be): 철색 면 위 본문. steel-dim(#9c9fa0)은 부차 텍스트·라벨.
- **크림 (Cream)** (#dae5eb)·**오프화이트 (Off White)** (#f7f5ed): 철색 면 위 강조 텍스트·제목.
- **로고 블랙 (Logo Black)** (#050607): 텍스트 워드마크의 검정 트랙에만 쓴다.

### Named Rules
**The Red Context Rule.** 빨강은 표면에 따라 역할이 갈린다: 면(도장·테이프·버튼)은 signal-red, 서류지 위 텍스트는 red-deep, 네이비 위 텍스트는 red-bright. 단색 signal-red를 작은 텍스트에 억지로 쓰지 않는다 — 대비 4.5:1 미만이면 역할을 바꾼다.
**The Two-Surface Rule.** 밝은 텍스트는 네이비 위에만, 어두운 텍스트는 서류지 위에만 둔다. 표면이 바뀌면 텍스트 색도 바뀐다 (steel ↔ ink).

## Typography

**Brand Logotype:** Oswald 600으로 공식 로고의 블록 구조를 재현한 텍스트 워드마크
**Headline Font:** YKompyuta Regular (400, 본문과 같은 타자기 인쇄 계열)
**Body Font:** YKompyuta Regular (400, jsDelivr 제공 — 낡은 타자기 인쇄의 불균일한 획)
**Label Font:** YKompyuta (파일 라벨·도장·메타, 대문자 + 자간). D2Coding은 네트워크 실패 시 폴백.
**Numeral Font:** YKompyuta (400, 설치 단계 번호용)

**Character:** 영문·한글 텍스트 로고에만 Oswald와 Paperlogy의 굵은 인쇄물 대비를 남긴다. 그 밖의 모든 정보는 YKompyuta로 타자해 한 장의 기밀 문서처럼 묶는다.

### Hierarchy
- **Brand Lockup** (Oswald 600 영문 / Paperlogy 700 한글, clamp(1.8rem, 7.8vw, 6rem)): 유일한 비-YKompyuta 영역.
- **Step Number** (YKompyuta 400, 1.35rem, 1): 순서가 중요한 설치 단계 번호.
- **Headline** (YKompyuta 400, clamp(1.7rem, 3.4vw, 2.5rem), 1.15): 사건 파일의 주요 제목.
- **Title** (YKompyuta 400, 1.0–1.15rem): 파일명·현장 기록·설치 단계 제목.
- **Body** (YKompyuta 400, 1rem, 1.75): 모든 본문. 한 줄 65–75자(36rem)로 제한.
- **Label** (YKompyuta 400, 0.72rem, 자간 0.14–0.18em, 대문자): 파일 탭·문서함 머리·메타·도장.
- **Annotation** (YKompyuta 400, 0.66rem, 1.5): 표지 검수 표식과 모바일 사건 필드.
- **Micro** (YKompyuta 400, 0.58rem, 1.45): 사건 메타의 필드명.

### Named Rules
**The Real-Type Rule.** 텍스트 로고만 Oswald·Paperlogy를 쓰고, 나머지는 예외 없이 YKompyuta를 쓴다. D2Coding은 네트워크 로딩 실패 시 가독성을 지키는 폴백이다.

## Layout

히어로와 푸터는 아카이브 스캔이 밴 철색 풀블리드다. 본문은 세계지도와 위경도선이 바랜 청회색 작전판 위에 폭 1120px 이하의 단일 카키 봉투형 서류를 올린다.

- **히어로**: 사건 메타 → 좌측 파일 라벨형 제목·설명·다운로드 도장 → 우측 하단 검수 표식의 비대칭 파일 편집. 지속 애니메이션 없이 검열 해제와 도장 등장만 한 번 실행한다.
- **서류 흐름**: 모든 화면에서 배포 승인 → 실행 절차 → 현장 기록 순의 단일 사건 파일. 적용 범위와 문제 해결은 하나의 기록 목록으로 합친다.
- **문서 크롬**: 파일 번호, 타공 두 개, 공개 도장, 상단 붉은 제본 테이프, 봉투 덮개 접힘선과 접힌 귀퉁이가 개봉된 작전 서류를 분명히 만든다.
- **반응형**: 560px 이하에서 청회색 바깥 여백을 제거하고, OS 탭과 다운로드 버튼을 전체 폭으로 확장한다.
- **리듬**: 서류 내부 주요 영역 사이는 `clamp(3.5rem, 7vw, 5.5rem)`. 도움말 앞에는 먹색 헤어라인을 둔다.
- **진행**: 화면 최상단 3px 빨간 스크롤 진행 바(scaleX).

## Elevation & Depth

하이브리드: 어두운 면은 **톤 레이어링**(navy-cover → navy-panel → navy-border)으로, 밝은 면은 **소프트 섀도**로 깊이를 준다. 하드 오프셋 섀도(네오브루탈)는 세계에 없다.

### Shadow Vocabulary
- **paper** (`3px 4px 0 rgba(31,32,39,.22), 0 26px 56px -18px rgba(31,32,39,.72)`): 작전판 위에 놓인 거친 봉투형 서류.
- **stamp** (`0 10px 26px -10px rgba(93,25,22,.7)`): 빨간 도장 CTA가 '찍혀' 있음을 강조.

**The Archive-Surface Rule.** 질감은 실제 무문자 아카이브 스캔 한 장에서만 가져오고 표면 색과 혼합 강도로 변주한다. 그라데이션은 지도 격자와 봉투 접힘선 같은 인쇄 선에만 쓰며, 광택·베벨·엠보싱으로 재질을 꾸미지 않는다.

## Shapes

- **모서리**: 1px(radius sm). 낡은 종이·철제 패널·도장의 거의 직각인 모서리 — 카드류 12–16px 둥금은 이 세계에 없다.
- **원형 도장**: 3px 실선 원 + 7px 안쪽 점선 원. -6~8도 회전이 '찍힘'을 만든다.
- **주 CTA**: 사각 도장 — 2px 실선 + 3px 오프셋 점선 외곽선, -1.5도 회전.
- **파일 접힘선**: 표지에는 낮은 대비의 비뚤어진 점선과 연필선만 두며, 상태나 진행으로 오해할 수 있는 세로 레일은 쓰지 않는다.
- **서류 시트**: 상단 8px 붉은 제본 테이프 + 파일 메타 헤어라인 + 두 개의 타공 + 큰 봉투 덮개 접힘선 + 접힌 귀퉁이.

## Components

### Buttons (도장)
- **Shape:** 1px radius, 회전(-1.5deg), 2px 점선 외곽선(offset 3px).
- **Primary (stamp-btn):** 아카이브 질감을 곱한 signal-red 배경 · off-white 텍스트 · YKompyuta 1.05rem · padding 0.95rem 1.6rem · stamp 섀도.
- **Hover / Focus:** 호버 = scale(1.06) + red-deep 배경 + 회전 증가 — '도장이 다시 찍히는' 느낌. active = scale(0.96). 포커스 = 흰 점선.
- **Secondary:** 텍스트 링크(red-deep, 밑줄 offset 3px)와 미니 도장(stamp-mini, 2px 테두리 0.66rem 대문자)만.

### OS 선택 카드 (radio)
- **Style:** 서류지 배경 · 1px 먹 테두리 · 1px radius · 3열 그리드(글리프/이름/파일명).
- **State:** 선택 = 오프화이트 배경 + 빨간 테두리 + inset 1px 빨강 링. 호버 = 오프화이트. 포커스 = 빨간 점선.

### 다운로드 패널
- **Style:** 아카이브 스캔이 밴 navy-cover 배경 · 크림 텍스트 · 1px radius · 파일명 모노. 기본 숨김, OS 선택 시 `.on`으로 나타난다.

### 설치 실행 기록
- **Style:** 별도 카드 없이 카키 사건 파일 위의 이중선과 행 구분으로 이어진다. 단계 번호·제목·본문은 모두 YKompyuta이며 red-deep 번호가 순서만 표시한다.
- **명령 블록:** navy-cover 배경 · 위쪽 1px 빨간 헤어라인 · 모노 0.74rem · 가로 스크롤 + 복사 버튼(steel → 호버 red).

### 기밀 해제 오프닝 (히어로 시그니처)
- 제목은 별도 찢김 바 없이 부모 클리핑 안에서 인양된다. 영문 로고가 드러난 뒤 1.35초에 검은 잉크가 덮고, 덮기가 끝나면 영문 글리프 레이어를 제거한다. 1.9초부터 폭이 한글 내용에 맞게 줄어든 뒤 2.08초에 `황혼의 투쟁`이 글리프 잘림 없이 한 번에 재인쇄된다. 다운로드 도장은 2.55초에 찍힌다. `prefers-reduced-motion`에서는 한글 로고를 최종 폭으로 즉시 표시한다.

### 해제된 사건 파일 (히어로 시그니처)
- 정적 2색 망점 세계지도에 아카이브 스캔과 위경도선을 겹친다. 서반구·동반구 인쇄판은 서로 4px가량 어긋나며, Canvas·스캔선·접촉점·패럴랙스는 사용하지 않는다. CASE NO.·DATE RELEASED·DISTRIBUTION·DECLASSIFIED가 파일 표지의 진위를 만든다.

## Do's and Don'ts

### Do:
- **Do** 액션은 도장 언어로 만든다: 회전 + 점선 외곽선 + 찍히는 호버.
- **Do** 마스킹 리빌은 실제 정보를 드러내는 데만 쓴다 — 스크롤 후에도 남는 장식용 마스킹은 금지.
- **Do** 빨강 3역할을 지킨다: 면=signal-red, 서류지 텍스트=red-deep, 네이비 텍스트=red-bright.
- **Do** 텍스트 로고 외 모든 글자는 YKompyuta로 통일한다. D2Coding은 폴백으로만 둔다.
- **Do** 표면이 바뀌면 텍스트 색도 바꾼다 (steel ↔ ink).
- **Do** 실제 아카이브 스캔 한 장을 표면마다 다른 혼합 강도로 재사용해 같은 시대의 물성으로 묶는다.
- **Do** 지도 격자에는 실제 세계지도 윤곽을 함께 두어 의미 있는 작전판으로 만든다.

### Don't:
- **Don't** 유니코드 글리프·이모지(⬇ ⚠ ▲ ■ 등)를 아이콘 대용으로 쓰지 않는다 — SVG로 직접 그린다.
- **Don't** 본문에 em-dash를 남발하지 않는다 — 한국어 구두점(마침표·가운뎃점)을 쓴다.
- **Don't** 네이비 위 작은 텍스트에 단색 signal-red를 쓰지 않는다 (대비 3:1 미만).
- **Don't** 광택 그라데이션·베벨·엠보싱·매끈한 유리 효과로 현대적인 재질을 끌어들이지 않는다.
- **Don't** 의미 없는 격자만 단독으로 쓰지 않는다 — 위경도선은 세계지도 윤곽과 함께 쓴다.
- **Don't** 증거 없는 계량("설치 약 3분" 등)을 주장하지 않는다 — 사실만.
- **Don't** 시스템 디스플레이 폰트(Impact류)나 하드 오프셋 섀도를 세계에 끌어들이지 않는다.
