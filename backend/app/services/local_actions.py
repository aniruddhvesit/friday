from dataclasses import dataclass
import os
import re
import sys
from typing import Sequence

from app.settings import settings

LocalAppId = str


@dataclass(frozen=True)
class LocalApp:
    app_id: LocalAppId
    label: str
    aliases: tuple[str, ...]
    launch_target: str
    fallback_targets: tuple[str, ...] = ()


LOCAL_APPS: tuple[LocalApp, ...] = (
    LocalApp("whatsapp", "WhatsApp", ("whatsapp", "whats app", "wa"), "whatsapp:", ("explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", "WhatsApp.exe")),
    LocalApp("discord", "Discord", ("discord", "dc"), "discord:", ("Discord.exe", "Discord.lnk")),
    LocalApp("valorant", "VALORANT", ("valorant", "val", "valo"), "VALORANT.lnk", ("RiotClientServices.exe", "Riot Client.lnk")),
    LocalApp("spotify", "Spotify", ("spotify", "music app"), "spotify:", ("Spotify.exe", "Spotify.lnk")),
    LocalApp("steam", "Steam", ("steam", "steam games"), "steam:", ("Steam.exe", "Steam.lnk")),
    LocalApp("telegram", "Telegram", ("telegram", "tg"), "tg:", ("Telegram.exe", "Telegram.lnk")),
    LocalApp("calculator", "Calculator", ("calculator", "calc"), "ms-calculator:"),
    LocalApp("notepad", "Notepad", ("notepad", "text editor", "notes"), "notepad.exe"),
    LocalApp("file_explorer", "File Explorer", ("file explorer", "explorer", "my computer", "this pc", "files folder"), "explorer.exe"),
    LocalApp("vscode", "Visual Studio Code", ("visual studio code", "vs code", "vscode", "code editor"), "vscode://", ("code.cmd", "Code.exe")),
    LocalApp("task_manager", "Task Manager", ("task manager", "taskmgr", "activity monitor", "processes"), "taskmgr.exe"),
    LocalApp("terminal", "Terminal", ("terminal", "command prompt", "cmd", "powershell", "console"), "cmd.exe", ("wt.exe", "powershell.exe")),
    LocalApp("paint", "Paint", ("paint", "mspaint", "drawing app"), "mspaint.exe"),
    LocalApp("snipping_tool", "Snipping Tool", ("snipping tool", "snip", "screenshot", "screen clip", "screen capture"), "snippingtool.exe"),
    LocalApp("settings", "Settings", ("settings", "windows settings", "system settings", "control panel"), "ms-settings:"),
    LocalApp("clock", "Clock", ("clock", "timer", "stopwatch", "alarm"), "ms-clock:"),
    LocalApp("camera", "Camera", ("camera", "webcam"), "microsoft.windows.camera:"),
    LocalApp("blender", "Blender", ("blender", "blender 3d"), "blender.exe", ("Blender 5.2.lnk", "Blender.lnk")),
    LocalApp("fusion", "Autodesk Fusion", ("fusion", "autodesk fusion", "fusion 360"), "Autodesk Fusion.lnk", ("fusion.exe", "Fusion360.exe")),
    LocalApp("lasercad", "LaserCAD", ("lasercad", "laser cad"), "LaserCAD V8.28.lnk", ("LaserCAD.exe", "LaserCAD.lnk")),
    LocalApp("vlc", "VLC Media Player", ("vlc", "vlc media player", "video player"), "vlc.exe", ("VLC media player.lnk",)),
    LocalApp("word", "Microsoft Word", ("word", "microsoft word", "ms word", "doc", "docs"), "winword.exe", ("Word.lnk",)),
    LocalApp("excel", "Microsoft Excel", ("excel", "microsoft excel", "ms excel", "spreadsheet", "sheets"), "excel.exe", ("Excel.lnk",)),
    LocalApp("powerpoint", "Microsoft PowerPoint", ("powerpoint", "ppt", "power point", "presentation", "slides"), "powerpnt.exe", ("PowerPoint.lnk",)),
    LocalApp("chrome", "Google Chrome", ("chrome", "google chrome"), "chrome.exe"),
    LocalApp("edge", "Microsoft Edge", ("edge", "microsoft edge"), "msedge.exe"),
)


def local_action_bridge_available() -> bool:
    return settings.local_actions_enabled and settings.backend_host in {"127.0.0.1", "localhost", "::1"} and sys.platform == "win32"


def _scan_shortcut_for_query(query: str) -> tuple[str, str] | None:
    clean_query = "".join(ch for ch in query.lower() if ch.isalnum())
    if not clean_query:
        return None

    search_dirs = [
        r"C:\Users\Aniruddh Yadav\OneDrive\Desktop",
        r"C:\Users\Aniruddh Yadav\Desktop",
        r"C:\Users\Public\Desktop",
        os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs"),
        os.path.join(os.environ.get("ProgramData", ""), r"Microsoft\Windows\Start Menu\Programs"),
    ]

    for sdir in search_dirs:
        if os.path.exists(sdir):
            for root, _, files in os.walk(sdir):
                for f in files:
                    if f.lower().endswith(".lnk"):
                        name_without_ext = os.path.splitext(f)[0]
                        clean_name = "".join(ch for ch in name_without_ext.lower() if ch.isalnum())
                        if clean_query in clean_name or clean_name in clean_query:
                            return name_without_ext, os.path.join(root, f)
    return None


def find_local_app(text: str) -> LocalApp | None:
    normalized = " ".join(text.lower().split())
    for app in LOCAL_APPS:
        if any(alias in normalized for alias in app.aliases):
            return app

    cleaned = re.sub(r"\b(please|can you|could you|open|launch|start|run|play|bring up|show|tyler|jarvis|app|application)\b", " ", normalized, flags=re.IGNORECASE)
    cleaned = " ".join(cleaned.split()).strip()
    if cleaned:
        match = _scan_shortcut_for_query(cleaned)
        if match:
            label, full_path = match
            app_id = "".join(ch if ch.isalnum() else "_" for ch in label.lower()).strip("_")
            return LocalApp(app_id=app_id, label=label, aliases=(cleaned,), launch_target=full_path)

    return None


def make_local_action_plan(text: str) -> dict[str, str | bool] | None:
    app = find_local_app(text)
    if not app:
        return None
    return {
        "kind": "open_local_app",
        "app_id": app.app_id,
        "label": app.label,
        "requires_confirmation": True,
    }


def execute_local_action(app_id: LocalAppId) -> LocalApp:
    if not local_action_bridge_available():
        raise RuntimeError("Local actions are disabled or the bridge is not running locally.")

    app = next((item for item in LOCAL_APPS if item.app_id == app_id), None)
    if app is None:
        match = _scan_shortcut_for_query(app_id)
        if match:
            label, full_path = match
            app = LocalApp(app_id=app_id, label=label, aliases=(app_id,), launch_target=full_path)
        else:
            raise ValueError("That application is not allowlisted.")

    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.AllowSetForegroundWindow(-1)
        except Exception:
            pass

    targets = [app.launch_target] + list(app.fallback_targets)
    launched = False
    last_err = None

    for target in targets:
        if not target:
            continue
        try:
            if target.endswith(".lnk"):
                if not os.path.isabs(target):
                    match = _scan_shortcut_for_query(os.path.splitext(target)[0])
                    if match:
                        target = match[1]
                if os.path.exists(target):
                    os.startfile(target)
                    launched = True
                    break
            elif target.startswith("explorer.exe shell:AppsFolder\\"):
                import subprocess
                subprocess.Popen(target, shell=True)
                launched = True
                break
            else:
                os.startfile(target)
                launched = True
                break
        except Exception as err:
            last_err = err
            continue

    if not launched:
        if last_err:
            raise last_err
        raise OSError(f"Could not launch {app.label}")

    if sys.platform == "win32":
        try:
            import subprocess
            cmd = f"Start-Sleep -Milliseconds 250; (New-Object -ComObject WScript.Shell).AppActivate('{app.label}')"
            subprocess.Popen(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception:
            pass

    return app
