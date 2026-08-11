# Twilight Struggle 한글 패치 — Windows 설치 스크립트
#
# 용도: patched/ → Steam 게임 폴더로 파일 복사 (백업 + 해시 검증)
# 멱등성: 이미 적용된 파일은 해시 확인 후 건너뜀. 재실행 안전.
#
# 사용법 (PowerShell 5.1+):
#   powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
#
# 옵션:
#   -GameData <경로>   게임 Data 폴더 (기본: Steam 기본 설치 경로)
#   -Force             백업 스킵 없이 강제 재복사
#
# 참고:
#   - 게임이 실행 중이면 파일이 잠겨 실패하므로 종료 후 실행
#   - 복원: 백업 폴더(backup-<날짜>)에서 파일을 되돌리거나
#     Steam "파일 무결성 확인" 실행
#   - macOS용: scripts/install.sh (코드사인 자동)

param(
    [string]$GameData = "$env:ProgramFiles(x86)\Steam\steamapps\common\Twilight Struggle\TwilightStruggle_Data",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$PatchedDir = Join-Path $PSScriptRoot "..\patched"
$Files = @("resources.assets", "sharedassets0.assets", "level1", "level2", "level3")

function Write-Step($msg)  { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  [!] $msg" -ForegroundColor Yellow }

# Get-FileHash가 없는 구형 환경 호환 (PS 2.0+)
function Get-SHA256($path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.IO.File]::ReadAllBytes($path)
        return ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '')
    } finally { $sha.Dispose() }
}

Write-Host "=== Twilight Struggle 한글 패치 설치 (Windows) ===" -ForegroundColor White

# ── 사전 검증 ──
if (-not (Test-Path $GameData)) {
    Write-Host "[오류] 게임 Data 폴더를 찾을 수 없습니다: $GameData" -ForegroundColor Red
    Write-Host "  -GameData <경로>로 직접 지정할 수 있습니다."
    exit 1
}
if (-not (Test-Path (Join-Path $PatchedDir "resources.assets"))) {
    Write-Host "[오류] 패치 파일이 없습니다: $PatchedDir" -ForegroundColor Red
    exit 1
}

# 게임 실행 중이면 중단 (파일 잠금 방지)
$proc = Get-Process -Name "TwilightStruggle*" -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "[오류] 게임이 실행 중입니다. 종료 후 다시 실행하세요." -ForegroundColor Red
    exit 1
}

# ── 백업 (최초 1회만 — .bak이 없을 때) ──
Write-Step "백업 확인"
$BackupDir = Join-Path $GameData ("backup-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
$backedUp = 0
foreach ($f in $Files) {
    $src = Join-Path $GameData $f
    $bak = "$src.bak"
    if ((Test-Path $src) -and (-not (Test-Path $bak))) {
        Copy-Item $src $bak
        Write-OK "$f -> $f.bak"
        $backedUp++
    }
}
if ($backedUp -eq 0) {
    Write-Warn "백업이 이미 존재하거나 복사할 원본이 없습니다 (.bak 유지)"
} else {
    Write-OK "백업 $backedUp개 완료"
}

# ── 패치 파일 복사 + 해시 검증 ──
Write-Step "패치 파일 복사"
$copied = 0; $skipped = 0; $failed = 0
foreach ($f in $Files) {
    $patched = Join-Path $PatchedDir $f
    if (-not (Test-Path $patched)) { continue }   # patched에 없는 파일은 스킵

    $dst = Join-Path $GameData $f
    $h1 = Get-SHA256 $patched
    if ((-not $Force) -and (Test-Path $dst) -and ((Get-SHA256 $dst) -eq $h1)) {
        Write-OK "$f — 이미 적용됨 (스킵)"
        $skipped++
        continue
    }
    Copy-Item $patched $dst -Force
    $h2 = Get-SHA256 $dst
    if ($h1 -eq $h2) {
        Write-OK "$f — 복사 + 해시 일치"
        $copied++
    } else {
        Write-Host "  [실패] $f — 해시 불일치!" -ForegroundColor Red
        $failed++
    }
}

# ── 결과 ──
Write-Host ""
if ($failed -gt 0) {
    Write-Host "=== 설치 실패 ($failed건 해시 불일치) ===" -ForegroundColor Red
    exit 1
}
Write-Host "=== 설치 완료! (복사 $copied건 / 스킵 $skipped건) ===" -ForegroundColor Green
Write-Host ""
Write-Host "  Steam에서 Twilight Struggle을 실행하세요."
Write-Host "  설정 → Languages에서 '한국어' 선택 (또는 레지스트리"
Write-Host "  HKCU\Software\Playdek\TwilightStruggle 의"
Write-Host "  localization_h2525087814 를 KO로 변경)"
Write-Host ""
Write-Host "  ※ 복원: 백업 .bak 파일을 되돌리거나 Steam 무결성 확인"
Write-Host "  ※ Steam 업데이트 후에는 다시 실행하세요."
