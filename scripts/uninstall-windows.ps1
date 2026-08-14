# Twilight Struggle 한글 패치 — 제거 스크립트 (Windows)
#
# 용도: 패치 제거 (파일 복원만)
#   - patched 파일 → 원본(.bak) 복원
# 언어 설정: 건드리지 않음 (2026-08-14 — EN 로케일 대체 방식, 복원 불필요)
#
# 사용법 (PowerShell 5.1+):
#   powershell -ExecutionPolicy Bypass -File scripts\uninstall-windows.ps1
#
# 옵션:
#   -GameData <경로>   게임 Data 폴더 (기본: Steam 기본 설치 경로)
#
# 참고:
#   - 게임이 실행 중이면 파일이 잠겨 실패하므로 종료 후 실행
#   - .bak이 없으면 Steam "파일 무결성 확인"으로 원복 후 이 스크립트 재실행
#   - Steam 업데이트로 .bak이 옛 버전이면 Steam 무결성 확인이 더 안전 (아래 안내 출력)

param(
    [string]$GameData = "$env:ProgramFiles(x86)\Steam\steamapps\common\Twilight Struggle\TwilightStruggle_Data"
)

$ErrorActionPreference = "Stop"
$Files = @("resources.assets", "sharedassets0.assets", "level1", "level2", "level3")

function Write-Step($msg)  { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  [!] $msg" -ForegroundColor Yellow }

Write-Host "=== Twilight Struggle 한글 패치 제거 (Windows) ===" -ForegroundColor White

# ── 사전 검증 ──
if (-not (Test-Path $GameData)) {
    Write-Host "[오류] 게임 Data 폴더를 찾을 수 없습니다: $GameData" -ForegroundColor Red
    Write-Host "  -GameData <경로>로 직접 지정할 수 있습니다."
    exit 1
}

# 게임 실행 중이면 중단 (파일 잠금 방지)
$proc = Get-Process -Name "TwilightStruggle*" -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "[오류] 게임이 실행 중입니다. 종료 후 다시 실행하세요." -ForegroundColor Red
    exit 1
}

# ── 원본(.bak) 복원 ──
Write-Step "원본(.bak) 복원"
$restored = 0; $missing = 0
foreach ($f in $Files) {
    $dst = Join-Path $GameData $f
    $bak = "$dst.bak"
    if (Test-Path $bak) {
        Copy-Item $bak $dst -Force
        Write-OK "$f <- $f.bak"
        $restored++
    } elseif (Test-Path $dst) {
        $missing++
    }
}
if ($restored -eq 0) {
    Write-Warn "복원할 .bak이 없습니다."
    Write-Warn "Steam → 라이브러리 → Twilight Struggle → 속성 → 설치된 파일 → '파일 무결성 확인' 실행"
} else {
    Write-OK "원본 복원 $restored개 완료"
    if ($missing -gt 0) {
        Write-Warn "$missing개 파일은 .bak이 없어 Steam 무결성 확인이 필요할 수 있습니다."
    }
}

# ── 완료 ──
Write-Host ""
Write-Host "=== 제거 완료! ===" -ForegroundColor Green
Write-Host ""
Write-Host "  Steam에서 Twilight Struggle을 실행하면 원래(영문) 상태로 돌아갑니다."
Write-Host ""
Write-Host "  ※ 재설치: powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1"
