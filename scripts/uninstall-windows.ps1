# Twilight Struggle 한글 패치 — 제거 스크립트 (Windows)
#
# 용도: 패치 제거 + 원래 언어 복귀 (영문 유저는 EN으로)
#   - patched 파일 → 원본(.bak) 복원
#   - 게임 언어 → 설치 전 값으로 복원 (krpatch-install-info.txt 기록 기준)
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
$InfoFile = Join-Path $GameData "krpatch-install-info.txt"

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

# ── 설치 정보 읽기 (언어 복원용) ──
$prevLang = ""
if (Test-Path $InfoFile) {
    foreach ($line in Get-Content $InfoFile) {
        if ($line -like "previous_localization_h2525087814=*") {
            $prevLang = $line.Substring($line.IndexOf("=") + 1)
        }
    }
    Write-OK "설치 기록 확인: $InfoFile (이전 언어: $prevLang)"
} else {
    Write-Warn "설치 기록 파일이 없습니다: krpatch-install-info.txt"
    Write-Warn "(구버전 설치 또는 게임 삭제·재설치로 기록이 사라진 경우입니다.)"
    Write-Warn "⚠️ 게임을 삭제·재설치해도 언어 설정(레지스트리)은 남아 KO일 수 있습니다."
    Write-Warn '   이 상태로 실행하면 메뉴·카드가 ${Key}로 표시되니 수동으로 되돌리세요:'
    Write-Host "   Set-ItemProperty -Path 'HKCU:\Software\Playdek\TwilightStruggle' -Name 'localization_h2525087814' -Value 'EN'" -ForegroundColor Cyan
    Write-Warn "   (⚠️ 이 게임에는 언어 선택 UI가 없습니다 — 위 레지스트리 명령으로만 변경 가능)"
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

# ── 게임 언어 복원 ──
Write-Step "게임 언어 복원"
$regPath = "HKCU:\Software\Playdek\TwilightStruggle"
$regName = "localization_h2525087814"
if (Test-Path $regPath) {
    if ($prevLang) {
        Set-ItemProperty -Path $regPath -Name $regName -Value $prevLang
        Write-OK "localization_h2525087814 -> $prevLang"
    } else {
        Remove-ItemProperty -Path $regPath -Name $regName -ErrorAction SilentlyContinue
        Write-OK "localization_h2525087814 = (설치 전에 없었음 — 키 제거)"
    }
} else {
    Write-Warn "레지스트리 키가 없어 언어 설정을 건드리지 않았습니다."
}

# ── 설치 정보 파일 제거 ──
if (Test-Path $InfoFile) {
    Remove-Item $InfoFile
    Write-OK "설치 정보 파일 삭제: krpatch-install-info.txt"
}

# ── 완료 ──
Write-Host ""
Write-Host "=== 제거 완료! ===" -ForegroundColor Green
Write-Host ""
Write-Host "  Steam에서 Twilight Struggle을 실행하면 원래 언어로 돌아갑니다."
Write-Host "  (이 게임에는 언어 선택 UI가 없어, 언어 변경은 레지스트리 값으로만 가능합니다)"
Write-Host ""
Write-Host "  ※ 재설치: powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1"
