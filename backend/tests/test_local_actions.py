from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api import local_actions as local_actions_api
from app.main import app
from app.services import local_actions

client = TestClient(app)


def enable_local_actions(monkeypatch) -> None:
    monkeypatch.setattr(local_actions, "settings", SimpleNamespace(local_actions_enabled=True, backend_host="127.0.0.1"))
    monkeypatch.setattr(local_actions.sys, "platform", "win32")


def test_local_planner_returns_whatsapp() -> None:
    plan = local_actions.make_local_action_plan("Please open WhatsApp")
    assert plan == {
        "kind": "open_local_app",
        "app_id": "whatsapp",
        "label": "WhatsApp",
        "requires_confirmation": True,
    }


def test_local_planner_returns_discord() -> None:
    plan = local_actions.make_local_action_plan("Open Discord")
    assert plan == {
        "kind": "open_local_app",
        "app_id": "discord",
        "label": "Discord",
        "requires_confirmation": True,
    }


def test_local_planner_returns_valorant() -> None:
    plan = local_actions.make_local_action_plan("Launch Valorant")
    assert plan == {
        "kind": "open_local_app",
        "app_id": "valorant",
        "label": "VALORANT",
        "requires_confirmation": True,
    }


def test_local_planner_returns_allowlisted_apps() -> None:
    plan = local_actions.make_local_action_plan("Please open Calculator")
    assert plan == {
        "kind": "open_local_app",
        "app_id": "calculator",
        "label": "Calculator",
        "requires_confirmation": True,
    }

    taskmgr_plan = local_actions.make_local_action_plan("Open Task Manager")
    assert taskmgr_plan == {
        "kind": "open_local_app",
        "app_id": "task_manager",
        "label": "Task Manager",
        "requires_confirmation": True,
    }


def test_execute_uses_fixed_allowlisted_target(monkeypatch) -> None:
    enable_local_actions(monkeypatch)
    launched: list[str] = []
    monkeypatch.setattr(local_actions.os, "startfile", lambda target: launched.append(target), raising=False)

    app_definition = local_actions.execute_local_action("whatsapp")
    assert app_definition.label == "WhatsApp"
    assert "whatsapp:" in launched


def test_execute_is_blocked_when_local_bridge_disabled(monkeypatch) -> None:
    monkeypatch.setattr(local_actions, "settings", SimpleNamespace(local_actions_enabled=False, backend_host="127.0.0.1"))

    try:
        local_actions.execute_local_action("notepad")
    except RuntimeError as error:
        assert "disabled" in str(error)
    else:
        raise AssertionError("Disabled local bridge must reject execution")
