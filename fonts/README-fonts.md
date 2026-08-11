# 폰트 라이선스 정보

이 프로젝트에서 사용하는 폰트는 모두 SIL Open Font License 1.1 (OFL) 하에
재배포 가능한 폰트입니다. 본문 전문은 `LICENSE-OFL-1.1.txt` 참조.

## 제목용 — Paperlogy 5 Medium

- 파일: `Paperlogy-5Medium.ttf`
- 출처: 산돌구름 페이퍼로지 (https://www.sandollcloud.com/free-font/21071/Paperlogy)
- 라이선스: SIL OFL 1.1 — 상업적 사용·수정·재배포 가능 (글꼴 단독 유료 판매 금지)
- 용도: 게임 제목/헤드라인 폰트 (BlackHanSans-Regular SDF 교체)
- 크기: m_PointSize 77 (기존 대비 ~9% 축소)

## 본문용 — D2Coding Regular

- 파일: `D2Coding-Ver1.3.3-20260725.ttf`
- 출처: NAVER D2Coding (https://github.com/naver/d2codingfont)
- 라이선스: SIL OFL 1.1 — Copyright (c) 2015 NAVER Corporation,
  Reserved Font Name: D2Coding
- 용도: 게임 본문 폰트 (NotoSerifKR SDF 교체)
- 크기: m_PointSize 77 (기존 대비 ~9% 축소)
- 참고: Bold(`D2CodingBold-...ttf`) 버전은 두께가 과해 Regular로 교체함

## 참고

- SDF 아틀라스(JSON/PNG)는 위 TTF에서 생성된 파생물이며 OFL 조건을 따릅니다.
- 크기 조절은 SDF JSON의 `m_PointSize` 수정 + 재주입으로 수행 — 절차는
  `.pi/skills/twilight-struggle-font-size/SKILL.md` 참조.
- 이전 폰트(Noto Serif KR, Black Han Sans, D2Coding Bold)와 구 SDF 산출물은
  `backup-20260812/`에 보관 (원복 시 사용).
