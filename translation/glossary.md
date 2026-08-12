# 용어 통일표 (Glossary)

> Phase 7(도움말/규칙 번역) 착수 시 신설 — 2026-08-13
> 근거: 기존 번역(런타임 TSV 2,253쌍 + cards/strings + manual-*.json)에서의 실제 사용 빈도 조사
> 규칙: **Phase 7 번역 시 아래 용어표를 기준으로 통일**한다. 새 용어가 필요하면 이 표에 추가하고,
> 카드/UI 번역과 어긋나지 않게 한다. EN 원문을 확인한 뒤 의미가 다르면 별도로 기록한다.

## 1. 게임 시스템 용어

| EN | 통일 한글 | 비고 (근거/사용처) |
|---|---|---|
| Victory Points (VP) | 승점 | "승점 트랙"(VP Track), "+1 승점" — 카드/점수 계산 전반 |
| Scoring Card | 점수 카드 | non-scoring card → **비점수 카드** |
| Operations Point | 작전치 | 카드의 작전치, "작전치 2 이상" |
| Influence (Marker) | 영향력 (마커) | "영향력 마커", "영향력 2를 추가" |
| Stability Number | 안정 수치 | "안정도" 혼용 사례 있음 → **안정 수치로 통일** (예: "안정 수치 1 또는 2") |
| Coup | 쿠데타 | "쿠데타 시도/굴림", "무료 쿠데타 굴림" |
| Realignment | 재편성 | "재편성 굴림", "재편성 시도" ("재편" 혼용 사례 → 재편성으로 통일) |
| DEFCON | 데프콘 | "데프콘 단계/수준", "데프콘 1" |
| Space Race | 우주 경쟁 | "우주 경쟁 트랙/마커" |
| China Card | 중국 카드 | "중국 카드 뒤집기"(Flip China Card) |
| Headline Phase / Card | 헤드라인 단계 / 헤드라인 카드 | |
| Action Round | 행동 라운드 | 턴 구성 요소 |
| Phasing Player | 차례 플레이어 | "현재 차례인 플레이어" 문장형으로도 사용 |
| Military Operations | 군사 작전 | "군사 작전 트랙", "군사 작전 현황 확인"(Check Military Operations) |
| Military Action | 군사 행동 | 카드 효과 문맥 |
| Hand | 손패 | "손패 한도/장수", "손에 있는 카드" |
| Discard / Discard Pile | 버리다 / 버린 카드 더미 | "카드를 버리고", "버린 카드 더미에서" |
| Deck / Draw | 덱 / 뽑다 | "덱에서 새로 뽑을 수 있다" |
| Bid | 입찰 | "진영 입찰"(Bid for Sides), "입찰하려는 영향력 수치" |
| Turn / Round | 턴 / 라운드 | "10턴", "행동 라운드" |
| Event | 이벤트 | "이벤트로 플레이할 수 없다", "'글라스노스트' 이벤트" |
| Add / Remove / Place | 추가 / 제거 / 배치·놓다 | "영향력 2를 추가", "미국 영향력을 모두 제거", "영향력 마커를 놓다" |
| Adjacent | 인접한 | "인접한 국가", "인접한 것으로 본다" |
| Sub-region | 하위 지역 | 유럽/동유럽·서유럽 등 |

## 2. 지역 점수 3단계 (Presence / Domination / Control)

| EN | 통일 한글 | 비고 |
|---|---|---|
| Presence | **진출** | "진출 없음"(No Presence), "그 지역에 진출한 것으로 본다" |
| Domination | **지배** | 지역 점수 2단계 |
| Control | **장악** | 지역 점수 3단계 — 단, 일반 문맥의 동사 control("US controlled country")은 **"지배"** 로 번역 (예: "미국이 지배하는 국가") |

⚠️ Control은 지역 점수 기준(장악)과 일반 동사(지배)가 다르므로 문맥 판단 필요.
예: "If the US controls Canada" → "미국이 캐나다를 지배하고 있다면" (기존 번역 확인)

## 3. 국가·진영·지역

| EN | 통일 한글 | 비고 |
|---|---|---|
| US / USSR | 미국 / 소련 | |
| Superpower | 초강대국 | |
| Region | 지역 | 6개 지역: 유럽, 아시아, 중앙아메리카, 남아메리카, 아프리카, 중동 |
| Battleground / Non-Battleground | 격전지 / 비격전지 | "격전지 국가", "비격전지" |
| Neutral | 중립 | |
| Pro-US / Pro-USSR | 친미 / 친소련 | |
| Communist / Democrat | 공산 / 민주 (국가별 정부 유형) | 상황 보고 필요 |

## 4. 카드·게임 요소

| EN | 통일 한글 | 비고 |
|---|---|---|
| Card | 카드 | |
| Crisis Card / Statecraft Card | 위기 카드 / 국정 카드 | Turn Zero |
| Starred Event | 별표 이벤트 | "이벤트 제목에 별표가 있으면" |
| Scoring (동사) | 점수 계산 | "점수 계산 지역" |
| Set Aside | 제쳐두다 | 카드 효과 문맥 |
| Shuffle | 섞다 | |
| Game Ends | 게임 종료 | |
| Final Scoring | 최종 점수 계산 | "최종 점수 계산에는 포함되지 않는다" |

## 5. 번역 시 주의 사항

- **TMP 리치텍스트 태그 보존**: `<color=white>`, `<br>`, `<indent=1em>`, `<margin-right=12em>`, `<font="...">`, `<i>` — 태그 위치와 짝 유지
- **승점/점수 카드/작전치 구분**: "점수"는 Scoring(계산)에, "승점"은 VP에만 사용
- **카드명은 기존 번역 유지**: '글라스노스트', '수렁', '마셜 계획', '바르샤바 조약', '닉슨의 중국 카드 플레이' 등 — cards.json과 대조
- **숫자·기호**: `1-4`(주사위), `+1`, `#42`(카드 번호) 형식 유지
- **단위**: "1개당", "매 ~마다" — "for each" → "~마다/1개당"

## 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-08-13 | 신설 — 기존 번역 빈도 조사 기반 초안 (Phase 7 착수) |
