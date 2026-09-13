Option Explicit
Dim WshShell, fso, strDir, q, pythonExe, edgePath, chromePath
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
q = Chr(34)

Function IsServiceRunning(url)
    On Error Resume Next
    Dim xmlHttp
    Set xmlHttp = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    xmlHttp.Open "GET", url, False
    xmlHttp.Send
    If Err.Number = 0 Then
        IsServiceRunning = True
    Else
        IsServiceRunning = False
    End If
    Set xmlHttp = Nothing
    On Error Goto 0
End Function

' 1. Start Backend silently if not running
If Not IsServiceRunning("http://127.0.0.1:8765/api/health") Then
    pythonExe = strDir & "\backend\.venv\Scripts\pythonw.exe"
    If Not fso.FileExists(pythonExe) Then
        pythonExe = strDir & "\backend\.venv\Scripts\python.exe"
    End If
    If Not fso.FileExists(pythonExe) Then
        pythonExe = "pythonw"
    End If
    WshShell.CurrentDirectory = strDir & "\backend"
    WshShell.Run q & pythonExe & q & " run_server.py", 0, False
End If

' 2. Start Frontend silently if not running
If Not IsServiceRunning("http://127.0.0.1:1420/") Then
    WshShell.CurrentDirectory = strDir & "\frontend"
    WshShell.Run "node dev-server.mjs", 0, False
End If

' 3. Wait for services to be ready (up to 12 seconds)
Dim i
For i = 1 To 24
    If IsServiceRunning("http://127.0.0.1:8765/api/health") And IsServiceRunning("http://127.0.0.1:1420/") Then
        Exit For
    End If
    WScript.Sleep 500
Next

' 4. Open Tyler App Window (Standalone App HUD)
edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

If fso.FileExists(edgePath) Then
    WshShell.Run q & edgePath & q & " --app=http://localhost:1420", 1, False
ElseIf fso.FileExists(chromePath) Then
    WshShell.Run q & chromePath & q & " --app=http://localhost:1420", 1, False
Else
    WshShell.Run "http://localhost:1420", 1, False
End If
