$ErrorActionPreference = 'SilentlyContinue'

Write-Host "Stopping Tyler AI Assistant background services..." -ForegroundColor Cyan

# Find and stop processes on port 8765 (Backend)
$port8765 = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if ($port8765) {
    $port8765.OwningProcess | Select-Object -Unique | ForEach-Object {
        Write-Host "Stopping backend process (PID $_)..." -ForegroundColor Yellow
        Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue
    }
}

# Find and stop processes on port 1420 (Frontend)
$port1420 = Get-NetTCPConnection -LocalPort 1420 -State Listen -ErrorAction SilentlyContinue
if ($port1420) {
    $port1420.OwningProcess | Select-Object -Unique | ForEach-Object {
        Write-Host "Stopping frontend process (PID $_)..." -ForegroundColor Yellow
        Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Tyler AI Assistant services stopped." -ForegroundColor Green
