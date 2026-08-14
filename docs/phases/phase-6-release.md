# Phase 6 — 배포

## 상태

- 상태: ✅ 완료 (2026-08-14)
- 선행 Phase: Phase 5 완료

## 목표

사용자가 안전하게 설치·복구할 수 있는 패치 배포물을 만들고, 기존 패치 제작자에게 크레딧과 업데이트 소식을 전달한다.

## 체크리스트

- [x] README 사용자 설치·복구 안내 작성 — 설치/제거/언어 KO 자동 설정 반영으로 갱신됨 (2026-08-12, 최종 확인 필요)
- [x] Windows 설치 스크립트(`install-windows.ps1`) 작성 — **Phase 5에서 완료** (언어 KO 자동 설정 포함)
- [x] **배포 패키징 스크립트(`scripts/package-release.sh`) 작성 (2026-08-12)** — 사용자용/재현용 zip 2종 + SHA256SUMS 생성, 실동작 검증 완료 (104MB → 8.9MB)
- [x] 라이선스와 크레딧 정리 — LICENSE(MIT + 번역 출처 + 면책 + 폰트 OFL) 작성 완료, README '감사의 말' 섹션 추가 (2026-08-14). CREDITS.md 별도 파일은 두지 않음 (LICENSE와 중복) — package-release.sh가 LICENSE를 LICENSE.txt로 자동 포함
- [x] 배포물에 원본 게임 파일이 포함되지 않았는지 확인 — v0.1.0 zip 목록 검증 완료 (patched 5종 + 스크립트 2 + README/LICENSE/SHA256SUMS만 포함, 2026-08-14)
- [x] GitHub Releases 배포 — `v0.1.0` 생성 완료 (2026-08-14) — https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.0 — **`v0.1.1` 생성 완료 (2026-08-14, Windows+macOS+src)** — https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1
- [ ] 기존 패치 제작자 크레딧·연락 — 크레딧은 LICENSE/README/릴리스 노트에 반영됨. 직접 연락은 미실시
- [x] 알려진 이슈와 지원 게임 버전 명시 — 릴리스 노트에 한계(턴 히스토리·튜토리얼)와 게임 버전 명시 완료

## 배포 구성 (package-release.sh, 2026-08-14 개편 — 플랫폼별 zip 3종)

```
dist/twilight-struggle-kr-patch-<버전>-windows.zip   # Windows 사용자용 (~9MB)
  patched/windows/{resources.assets, sharedassets0.assets, level1~3, hashes.txt}
  scripts/{install-windows.ps1, uninstall-windows.ps1}
  README.md + LICENSE.txt
  SHA256SUMS

dist/twilight-struggle-kr-patch-<버전>-macos.zip      # macOS 사용자용 (~9MB)
  patched/macos/{resources.assets, sharedassets0.assets, level1~3, hashes.txt}
  scripts/{install.sh, uninstall.sh, restore-original.sh}
  README.md + LICENSE.txt
  SHA256SUMS

dist/twilight-struggle-kr-patch-<버전>-src.zip        # 재현용 (~3MB)
  translation/  fonts/  scripts/(파이프라인 전체 + 설치·제거)  docs/{PLAN,PROGRESS}.md  SHA256SUMS
```

- ⚠️ patched/는 플랫폼별 분리 (2026-08-14): `patched/windows/`·`patched/macos/` — level1~3 교차 복사 시 크래시 (실측)
- 존재하지 않는 플랫폼 폴더는 경고 후 자동 스킵 — 배포 전 양쪽 플랫폼 패치 완성 필수
- `patched/*/*.assets`는 GitHub 100MB 제한으로 gitignore — **zip 압축 시 104MB → ~8MB**라 Releases 첨부로 충분 (LFS 불필요)
- 사용법: `./scripts/package-release.sh v0.1.0` → `gh release create v0.1.0 dist/*.zip`
- macOS/Linux/Windows(Git Bash) 호환: 해시는 sha256sum/shasum 자동 선택, 압축은 Python zipfile

## 검증 기준

| 항목 | 성공 기준 |
|---|---|
| 설치 안내 | 대상 플랫폼에서 처음부터 따라 할 수 있음 |
| 배포물 | 필요한 스크립트·패치·번역 소스·라이선스가 포함됨 |
| 안전성 | 원본 게임 파일과 불필요한 개인 파일이 배포물에 없음 |
| 재현성 | README의 명령으로 패치 파일을 재생성할 수 있음 |

## 검증 결과

| 항목 | 방법 | 결과 |
|---|---|---|
| 패키징 스크립트 | `./scripts/package-release.sh v0.1.0-test` 실행 | ✅ 성공 — 사용자용 8.9MB / 재현용 3.4MB 생성, zip 내용·SHA256SUMS 확인 (2026-08-12) |
| zip 내용 | python zipfile 목록 비교 | ✅ 사용자용(patched 6 + scripts 5 + README + SHA256SUMS), 재현용 35개 (fonts backup 제외) — uninstall 2종 포함 확인 (2026-08-12) |
| v0.1.0 배포 | gh release create | ✅ Windows+src 릴리스 완료 (2026-08-14) — https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.0 (macOS는 패치본 미생성으로 제외) |
| v0.1.1 배포 | gh release create + 산출물 검증 | ✅ Windows+macOS+src 릴리스 완료 (2026-08-14) — https://github.com/oliverne/twilight-struggle-kr-patch/releases/tag/v0.1.1 (windows 9MB + macos 10MB + src 16MB). 검증: zip 내부 `patched/<플랫폼>/` 구조 확인, SHA256SUMS zip별 전체 일치 (windows 10/macos 11/src 44) |
| macOS 실게임 | install.sh 설치 후 Steam 실행 | ✅ 사용자 실게임 확인 완료 — 메뉴·카드 한글 (2026-08-14) |
| v0.1.1 패키징 버그 수정 | package-release.sh 실행·검증 | ✅ zip 레이아웃 `patched/<플랫폼>/` 수정(`aab7c7f`) + SHA256SUMS 자기 자신 포함 버그 수정(`7587793`) — v0.1.0 zip은 두 버그로 설치 불가였음 |

## 완료 기록

- **배포 URL**: v0.1.0 (Windows+src, 2026-08-14) · v0.1.1 (Windows+macOS+src, 2026-08-14) — https://github.com/oliverne/twilight-struggle-kr-patch/releases
- **지원 버전**: Steam Twilight Struggle (App ID 406290, Unity 6000.0.58f2, IL2CPP) — Windows 10/11, macOS 10.13+, 스팀덱·Linux(Proton, Windows 배포본 사용)
- **해시**: zip 내부 SHA256SUMS (windows 10개 / macos 11개 / src 44개 파일 전부 일치, 2026-08-14)
- **알려진 이슈**: 턴 히스토리 로그·튜토리얼 안내(계층 3, IL2CPP) 영어 — BepInEx 런타임 훅 필요 (ISSUES #11·#17), 보드맵 텍스처 국가명 범위 제외, 멀티플레이 미검증
- **크레딧**: 한식구 런타임 패치(2026-03-15) 번역 재사용 + 블루칩 v1.0.1 참고 — LICENSE/README '감사의 말'/릴리스 노트 반영. 직접 연락은 미실시

## 다음 Phase로 핸드오프 (프로젝트 마감)

- **마지막 Phase** — 이후 작업은 모두 보류/선택 사항.
- 미해결 이슈 (보류 유지):
  1. 계층 3 한글화 (턴 히스토리·튜토리얼) — BepInEx 런타임 훅 별도 프로젝트 (ISSUES #11·#17)
  2. 배포 후 사용자 설치 검증 (외부 사용자 zip 설치→한글→uninstall→영어 복귀) — 내부 검증은 완료
  3. 멀티플레이 테스트 미실시
  4. 폰트 줄 간격 보조 보정 (`--use-game-line-metrics`) 미적용
  5. ISSUES #6(setup-uabea-mac.sh 체크섬)·#7(restore-original.sh while read)·#9(asset-tool HintPath) — 보류
- **재적용 경로**: Steam 업데이트/무결성으로 원복 시 `twilight-struggle-update` 스킬 → 파이프라인 재실행 → 재배포
