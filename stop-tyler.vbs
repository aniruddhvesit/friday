Set WshShell = CreateObject("WScript.Shell")
strDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & strDir & "\stop-tyler.ps1""", 0, True
WshShell.Popup "Tyler AI Assistant has been stopped.", 2, "Tyler AI Assistant", 64
