# Twilight Struggle 한글 패치 — Windows 설치 스크립트
#
# 용도: patched/ → Steam 게임 폴더로 파일 복사 (백업 + 해시 검증)
# 멱등성: 이미 적용된 파일은 해시 확인 후 건너뜀. 재실행 안전.
# 언어 설정: 건드리지 않음 (2026-08-14 — EN 로케일을 한글로 대체, 유저는 기본 언어 EN 사용)
#
# 사용법 (PowerShell 5.1+):
#   powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
#
# 옵션:
#   -GameData <경로>   게임 Data 폴더 (기본: Steam 설치 위치 자동 탐색)
#   -Force             백업 스킵 없이 강제 재복사
#
# 참고:
#   - 게임이 실행 중이면 파일이 잠겨 실패하므로 종료 후 실행
#   - Steam이 기본 경로(C:\Program Files (x86)\Steam)가 아닌 곳에 있으면
#     레지스트리(SteamPath) + libraryfolders.vdf로 자동 탐색 (D 드라이브 등)
#   - 복원: 백업 폴더(backup-<날짜>)에서 파일을 되돌리거나
#     Steam "파일 무결성 확인" 실행
#   - macOS용: scripts/install.sh (코드사인 자동)

param(
    [string]$GameData = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$PatchedDir = Join-Path $PSScriptRoot "..\patched\windows"
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

# Steam 설치 위치 자동 탐색 (기본 경로가 아닌 D 드라이브 등)
function Find-GameData {
    $libPaths = @()

    # 1) Steam 설치 경로: 레지스트리 (HKCU: 실제 설치 위치, HKLM: 32비트 Steam)
    $steamPath = ""
    try { $steamPath = (Get-ItemProperty -Path "HKCU:\Software\Valve\Steam" -Name "SteamPath" -ErrorAction SilentlyContinue).SteamPath } catch {}
    if (-not $steamPath) { try { $steamPath = (Get-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432Node\Valve\Steam" -Name "InstallPath" -ErrorAction SilentlyContinue).InstallPath } catch {} }
    if ($steamPath) { $libPaths += $steamPath }

    # 2) libraryfolders.vdf에서 추가 라이브러리 폴더 파싱
    if ($steamPath) {
        $vdf = Join-Path $steamPath "steamapps\libraryfolders.vdf"
        if (Test-Path $vdf) {
            $vdfText = Get-Content $vdf -Raw -ErrorAction SilentlyContinue
            if ($vdfText) {
                foreach ($m in [regex]::Matches($vdfText, '"path"\s+"([^"]+)"')) {
                    $p = $m.Groups[1].Value -replace '\\\\', '\'  # VDF 이스케이프 해제
                    if ($p -and ($libPaths -notcontains $p)) { $libPaths += $p }
                }
            }
        }
    }

    # 3) 기본 설치 경로 후보도 포함
    $libPaths += "$env:ProgramFiles(x86)\Steam"
    $libPaths += "$env:ProgramFiles\Steam"

    # 4) 후보 탐색
    foreach ($lp in $libPaths) {
        $cand = Join-Path $lp "steamapps\common\Twilight Struggle\TwilightStruggle_Data"
        if (Test-Path $cand) { return $cand }
    }
    return $null
}

Write-Host "=== Twilight Struggle 한글 패치 설치 (Windows) ===" -ForegroundColor White

# ── 게임 경로 결정: -GameData 지정 > 자동 탐색 ──
if (-not $GameData) {
    $GameData = Find-GameData
    if ($GameData) { Write-OK "Steam 위치 자동 탐색: $GameData" }
}

# ── 사전 검증 ──
if (-not (Test-Path $GameData)) {
    Write-Host "[오류] 게임 Data 폴더를 찾을 수 없습니다: $GameData" -ForegroundColor Red
    Write-Host "  -GameData <경로>로 직접 지정할 수 있습니다."
    exit 1
}

# ── .assets.gz 자동 해제 (git clone 후 첫 실행 대응) ──
$gzs = Get-ChildItem -Path $PatchedDir -Filter "*.assets.gz" -ErrorAction SilentlyContinue
if ($gzs) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if ($py) {
        Write-Step "git 공유 압축 에셋(.assets.gz) 자동 해제"
        & python (Join-Path $PSScriptRoot "assets-sync.py") decompress
    } else {
        Write-Warn "python 없음 — .assets.gz 해제를 건너뜁니다"
    }
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
Write-Host "  (언어 설정은 변경하지 않습니다 — EN 로케일이 한글로 대체되어 메뉴가 즉시 한글 표시)"
Write-Host ""
Write-Host "  ※ 영문(원래 언어) 복귀: scripts\uninstall-windows.ps1 (원본 .bak 복원)"
Write-Host "  ※ Steam 무결성 검사 후에는 다시 실행하세요."
