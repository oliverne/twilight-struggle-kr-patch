# Phase 6 — 배포

## 상태

- 상태: ⬜ 대기
- 선행 Phase: Phase 5 완료

## 목표

사용자가 안전하게 설치·복구할 수 있는 패치 배포물을 만들고, 기존 패치 제작자에게 크레딧과 업데이트 소식을 전달한다.

## 체크리스트

- [x] README 사용자 설치·복구 안내 작성 — 설치/제거/언어 KO 자동 설정 반영으로 갱신됨 (2026-08-12, 최종 확인 필요)
- [x] Windows 설치 스크립트(`install-windows.ps1`) 작성 — **Phase 5에서 완료** (언어 KO 자동 설정 포함)
- [x] **배포 패키징 스크립트(`scripts/package-release.sh`) 작성 (2026-08-12)** — 사용자용/재현용 zip 2종 + SHA256SUMS 생성, 실동작 검증 완료 (104MB → 8.9MB)
- [ ] 라이선스와 크레딧 정리 (폰트 OFL + 기존 패치 번역 크레딧) — **package-release.sh가 LICENSE.txt/CREDITS.md 부재 시 경고 출력**
- [ ] 배포물에 원본 게임 파일이 포함되지 않았는지 확인
- [ ] GitHub Releases 배포 — `gh release create` 또는 웹 UI로 dist/*.zip 첨부 (gitignore와 무관, 파일당 2GB 제한 내)
- [ ] 기존 패치 제작자 크레딧·연락
- [ ] 알려진 이슈와 지원 게임 버전 명시 (턴 히스토리 미번역 등)

## 배포 구성 (package-release.sh, 2026-08-14 개편 — 플랫폼별 zip 3종)

```
dist/twilight-struggle-kr-patch-<버전>-windows.zip   # Windows 사용자용 (~9MB)
  patched/windows/{resources.assets, sharedassets0.assets, level1~3, hashes.txt}
  scripts/{install-windows.ps1, uninstall-windows.ps1}
  README.md (+ LICENSE.txt, CREDITS.md — 존재 시)
  SHA256SUMS

dist/twilight-struggle-kr-patch-<버전>-macos.zip      # macOS 사용자용 (~9MB)
  patched/macos/{resources.assets, sharedassets0.assets, level1~3, hashes.txt}
  scripts/{install.sh, uninstall.sh, restore-original.sh}
  README.md (+ LICENSE.txt, CREDITS.md — 존재 시)
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
| — | — | ⬜ 배포 대기 |

## 완료 기록

Phase 완료 시 배포 URL, 지원 버전, 해시, 알려진 이슈, 크레딧·연락 결과를 기록한다.
