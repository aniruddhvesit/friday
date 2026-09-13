$ErrorActionPreference = 'SilentlyContinue'
$jarvisDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $jarvisDir) { $jarvisDir = 'C:\Users\Aniruddh Yadav\OneDrive\Desktop\jarvis' }

# 1. Start Backend if not already running
$beConn = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if (-not $beConn) {
    $pythonExe = Join-Path $jarvisDir 'backend\.venv\Scripts\python.exe'
    if (-not (Test-Path $pythonExe)) {
        $pythonExe = 'python'
    }
    Start-Process -FilePath $pythonExe -ArgumentList @('-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8765') -WorkingDirectory (Join-Path $jarvisDir 'backend') -WindowStyle Hidden
}

# 2. Start Frontend if not already running
$feConn = Get-NetTCPConnection -LocalPort 1420 -State Listen -ErrorAction SilentlyContinue
if (-not $feConn) {
    Start-Process -FilePath 'node' -ArgumentList @('dev-server.mjs') -WorkingDirectory (Join-Path $jarvisDir 'frontend') -WindowStyle Hidden
}

# 3. Wait for services to be ready (up to 12 seconds)
for ($i = 0; $i -lt 24; $i++) {
    $beConn = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
    $feConn = Get-NetTCPConnection -LocalPort 1420 -State Listen -ErrorAction SilentlyContinue
    if ($beConn -and $feConn) {
        break
    }
    Start-Sleep -Milliseconds 500
}

# 4. Open Tyler App Window (Standalone App HUD)
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

if (Test-Path $edge) {
    Start-Process -FilePath $edge -ArgumentList @('--app=http://localhost:1420')
} elseif (Test-Path $chrome) {
    Start-Process -FilePath $chrome -ArgumentList @('--app=http://localhost:1420')
} else {
    Start-Process 'http://localhost:1420'
}
