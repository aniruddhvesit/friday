import { API_BASE_URL } from "./api/client";
import { isCapabilityQuery } from "./webActions";

export type LocalAction = {
  kind: "open_local_app";
  appId:
    | "calculator"
    | "notepad"
    | "file_explorer"
    | "vscode"
    | "task_manager"
    | "terminal"
    | "paint"
    | "snipping_tool"
    | "settings"
    | "clock"
    | "camera";
  label: string;
  requiresConfirmation: true;
};

const localAppPattern =
  /\b(calculator|calc|notepad|text editor|notes|file explorer|explorer|my computer|this pc|visual studio code|vs code|vscode|code editor|task manager|taskmgr|activity monitor|terminal|command prompt|cmd|powershell|console|paint|mspaint|drawing|snipping tool|snip|screenshot|screen clip|screen capture|settings|windows settings|system settings|clock|alarm|timer|stopwatch|camera|webcam)\b/i;
const launchPattern = /\b(open|launch|start|run|take a|capture|show|bring up)\b/i;

export function isLocalActionRequest(text: string): boolean {
  if (isCapabilityQuery(text)) return false;
  return launchPattern.test(text) && localAppPattern.test(text);
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (response.ok) return response.json() as Promise<T>;
  const body = await response.json().catch(() => null) as { detail?: string } | null;
  throw new Error(body?.detail || "Tyler could not complete that local action.");
}

export async function getLocalActionStatus(): Promise<boolean> {
  const status = await requestJson<{ enabled: boolean }>("/local-actions/status");
  return status.enabled;
}

export function planLocalAction(text: string): Promise<LocalAction> {
  return requestJson<LocalAction>("/local-actions/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function executeLocalAction(appId: LocalAction["appId"]): Promise<{ ok: true; message: string }> {
  return requestJson<{ ok: true; message: string }>("/local-actions/execute", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ appId, confirmed: true }),
  });
}
