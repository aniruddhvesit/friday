$code = @"
using System;
using System.Runtime.InteropServices;

public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool BringWindowToTop(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, int dwExtraInfo);
}
"@

Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue

param(
    [string]$SearchTerm = ""
)

if (-not $SearchTerm) { exit }

$wsh = New-Object -ComObject WScript.Shell

for ($i = 0; $i -lt 15; $i++) {
    [Win32]::keybd_event(0x12, 0, 0, 0)
    [Win32]::keybd_event(0x12, 0, 2, 0)

    $activated = $false

    # 1. Check all processes
    $procs = Get-Process -ErrorAction SilentlyContinue | Where-Object {
        ($_.ProcessName -like "*$SearchTerm*" -or $_.MainWindowTitle -like "*$SearchTerm*") -and $_.MainWindowHandle -ne 0
    }

    foreach ($p in $procs) {
        $hwnd = $p.MainWindowHandle
        [Win32]::ShowWindowAsync($hwnd, 9) # SW_RESTORE
        [Win32]::ShowWindowAsync($hwnd, 5) # SW_SHOW
        [Win32]::SetForegroundWindow($hwnd)
        [Win32]::BringWindowToTop($hwnd)
        $wsh.AppActivate($p.Id)
        $wsh.AppActivate($p.MainWindowTitle)
        $activated = $true
    }

    # 2. Also try AppActivate directly by title / term
    if ($wsh.AppActivate($SearchTerm)) {
        $activated = $true
    }

    if ($activated) {
        break
    }

    Start-Sleep -Milliseconds 200
}
