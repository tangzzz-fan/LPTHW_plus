from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import signal
import sys
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
CONTENT_ROOT = ROOT / "content" / "tracks"
WORKSPACE_ROOT = ROOT / "learner_workspace"

# Python 3.13+ colorizes tracebacks; strip for browser <pre> display.
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07|\x1b[\[\]()#;?]*.")


def _strip_ansi(text: str) -> str:
    if not text:
        return text
    return _ANSI_RE.sub("", text)


def _run_env() -> dict[str, str]:
    env = os.environ.copy()
    env["NO_COLOR"] = "1"
    env["PYTHON_COLORS"] = "0"
    env["TERM"] = "dumb"
    env.pop("FORCE_COLOR", None)
    env.pop("CLICOLOR_FORCE", None)
    return env

app = FastAPI(title="LPTHW Learner API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# session_id -> running process state
_sessions: dict[str, dict[str, Any]] = {}


def _safe_join(base: Path, relative: str) -> Path:
    rel = relative.replace("\\", "/").lstrip("/")
    if ".." in Path(rel).parts:
        raise HTTPException(status_code=400, detail="Path traversal denied")
    target = (base / rel).resolve()
    base_resolved = base.resolve()
    if not str(target).startswith(str(base_resolved)):
        raise HTTPException(status_code=400, detail="Path outside workspace")
    return target


def _track_dir(track: str) -> Path:
    path = CONTENT_ROOT / track
    if not path.is_dir():
        raise HTTPException(status_code=404, detail=f"Unknown track: {track}")
    return path


def _load_lesson(track: str, lesson_id: str) -> dict[str, Any]:
    path = _track_dir(track) / f"{lesson_id}.json"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Lesson not found")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    data["track"] = track
    data["id"] = lesson_id
    return data


def _workspace(track: str, lesson_id: str) -> Path:
    return WORKSPACE_ROOT / track / lesson_id


def _ensure_workspace(track: str, lesson_id: str) -> Path:
    lesson = _load_lesson(track, lesson_id)
    ws = _workspace(track, lesson_id)
    ws.mkdir(parents=True, exist_ok=True)
    starter = lesson.get("starterFiles") or {}
    for name, content in starter.items():
        target = _safe_join(ws, name)
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    return ws


class RunRequest(BaseModel):
    track: str
    exerciseId: str
    entry: str | None = None
    code: str | None = None
    stdin: str | None = None
    sessionId: str | None = None
    timeoutSec: int | None = None


class FilePutRequest(BaseModel):
    path: str
    content: str = ""


class StdinRequest(BaseModel):
    sessionId: str
    data: str
    eof: bool = False


@app.get("/api/health")
def health() -> dict[str, Any]:
    info: dict[str, Any] = {
        "ok": True,
        "service": "lpthw-learner",
        "python": sys.version.split()[0],
        "contentRoot": str(CONTENT_ROOT),
    }
    try:
        import torch  # type: ignore

        info["torch"] = torch.__version__
        info["mps"] = bool(torch.backends.mps.is_available())
    except Exception:
        info["torch"] = None
        info["mps"] = False
    return info


@app.get("/api/tracks")
def list_tracks() -> list[dict[str, Any]]:
    meta = {
        "lpthw": {"title": "LPTHW 基础", "priority": False, "order": 0},
        "async-llm": {"title": "Async / LLM 落地", "priority": True, "order": 1},
        "pytorch": {"title": "PyTorch", "priority": True, "order": 2},
        "llm-from-scratch": {
            "title": "LLMFromScratch",
            "priority": True,
            "order": 3,
        },
        "mit-python": {"title": "MIT-Python", "priority": True, "order": 4},
        "mit-llm": {"title": "MIT-LLM", "priority": True, "order": 5},
    }
    tracks = []
    if not CONTENT_ROOT.exists():
        return tracks
    for child in CONTENT_ROOT.iterdir():
        if child.is_dir() and not child.name.startswith("."):
            info = meta.get(child.name, {"title": child.name, "priority": False, "order": 99})
            tracks.append({"id": child.name, "title": info["title"], "priority": info["priority"]})
    order = {k: v.get("order", 99) for k, v in meta.items()}
    tracks.sort(key=lambda t: order.get(t["id"], 99))
    return tracks


@app.get("/api/tracks/{track}/exercises")
def list_exercises(track: str) -> list[dict[str, Any]]:
    folder = _track_dir(track)
    items: list[dict[str, Any]] = []
    for path in sorted(folder.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        items.append(
            {
                "id": path.stem,
                "track": track,
                "title": data.get("title", path.stem),
                "priority": bool(data.get("priority", False)),
                "timeoutSec": data.get("timeoutSec", 5),
                "requires": data.get("requires", []),
                "outlineOnly": bool(data.get("outlineOnly", False)),
            }
        )
    return items


@app.get("/api/exercises/{track}/{lesson_id}")
def get_exercise(track: str, lesson_id: str) -> dict[str, Any]:
    lesson = _load_lesson(track, lesson_id)
    _ensure_workspace(track, lesson_id)
    return lesson


@app.get("/api/files/{track}/{lesson_id}")
def list_files(track: str, lesson_id: str) -> list[dict[str, str]]:
    ws = _ensure_workspace(track, lesson_id)
    files: list[dict[str, str]] = []
    for path in sorted(ws.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(ws)).replace("\\", "/")
            files.append({"path": rel})
    return files


@app.get("/api/files/{track}/{lesson_id}/content")
def read_file(track: str, lesson_id: str, path: str) -> dict[str, str]:
    ws = _ensure_workspace(track, lesson_id)
    target = _safe_join(ws, path)
    if not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return {"path": path, "content": target.read_text(encoding="utf-8")}


@app.put("/api/files/{track}/{lesson_id}")
def write_file(track: str, lesson_id: str, body: FilePutRequest) -> dict[str, str]:
    ws = _ensure_workspace(track, lesson_id)
    target = _safe_join(ws, body.path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.content, encoding="utf-8")
    return {"path": body.path, "status": "saved"}


@app.delete("/api/files/{track}/{lesson_id}")
def delete_file(track: str, lesson_id: str, path: str) -> dict[str, str]:
    ws = _ensure_workspace(track, lesson_id)
    target = _safe_join(ws, path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()
    return {"path": path, "status": "deleted"}


async def _read_available(stream: asyncio.StreamReader, limit: int = 200_000) -> str:
    chunks: list[bytes] = []
    total = 0
    while True:
        try:
            chunk = await asyncio.wait_for(stream.read(4096), timeout=0.05)
        except asyncio.TimeoutError:
            break
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total >= limit:
            break
    return b"".join(chunks).decode("utf-8", errors="replace")


async def _drain_session(session: dict[str, Any]) -> None:
    proc: asyncio.subprocess.Process = session["proc"]
    if proc.stdout:
        session["stdout"] += _strip_ansi(await _read_available(proc.stdout))
    if proc.stderr:
        session["stderr"] += _strip_ansi(await _read_available(proc.stderr))


def _session_payload(session_id: str | None, session: dict[str, Any], running: bool) -> dict[str, Any]:
    proc: asyncio.subprocess.Process = session["proc"]
    return {
        "sessionId": session_id if running else None,
        "running": running,
        "exitCode": None if running else proc.returncode,
        "stdout": _strip_ansi(session["stdout"]),
        "stderr": _strip_ansi(session["stderr"]),
        "waitingForInput": running,
    }


@app.post("/api/run")
async def run_code(req: RunRequest) -> dict[str, Any]:
    lesson = _load_lesson(req.track, req.exerciseId)
    ws = _ensure_workspace(req.track, req.exerciseId)
    timeout = req.timeoutSec or int(lesson.get("timeoutSec", 5))
    entry = req.entry or lesson.get("entry") or "main.py"

    if req.code is not None:
        target = _safe_join(ws, entry)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(req.code, encoding="utf-8")

    script = _safe_join(ws, entry)
    if not script.is_file():
        raise HTTPException(status_code=400, detail=f"Entry not found: {entry}")

    # Continue existing interactive session
    if req.sessionId and req.sessionId in _sessions:
        session = _sessions[req.sessionId]
        proc: asyncio.subprocess.Process = session["proc"]
        if req.stdin is not None and proc.stdin and not proc.stdin.is_closing():
            payload = req.stdin if req.stdin.endswith("\n") else req.stdin + "\n"
            proc.stdin.write(payload.encode())
            await proc.stdin.drain()
        await _drain_session(session)
        deadline = session.get("deadline")
        wait = 0.25
        if deadline is not None:
            wait = max(0.05, min(0.25, deadline - asyncio.get_event_loop().time()))
            if wait <= 0 and proc.returncode is None:
                try:
                    proc.kill()
                except ProcessLookupError:
                    pass
                await proc.wait()
                await _drain_session(session)
                result = _session_payload(None, session, running=False)
                result["stderr"] = (result.get("stderr") or "") + "\n[killed: timeout]\n"
                _sessions.pop(req.sessionId, None)
                return result
        try:
            await asyncio.wait_for(proc.wait(), timeout=wait)
        except asyncio.TimeoutError:
            return _session_payload(req.sessionId, session, running=True)
        await _drain_session(session)
        result = _session_payload(None, session, running=False)
        _sessions.pop(req.sessionId, None)
        return result

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-u",
        str(script.name),
        cwd=str(ws),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=_run_env(),
    )

    session_id = str(uuid.uuid4())
    session: dict[str, Any] = {"proc": proc, "stdout": "", "stderr": ""}
    _sessions[session_id] = session

    if req.stdin is not None and proc.stdin:
        payload = req.stdin if req.stdin.endswith("\n") else req.stdin + "\n"
        proc.stdin.write(payload.encode())
        await proc.stdin.drain()

    # Wait up to lesson timeout. Interactive input() lessons use a short timeoutSec
    # so the client gets a session quickly; torch lessons use 30–120s.
    loop = asyncio.get_event_loop()
    deadline = loop.time() + float(timeout)
    while loop.time() < deadline:
        await _drain_session(session)
        if proc.returncode is not None:
            break
        remaining = deadline - loop.time()
        try:
            await asyncio.wait_for(proc.wait(), timeout=min(0.15, max(0.05, remaining)))
            break
        except asyncio.TimeoutError:
            continue

    await _drain_session(session)
    if proc.returncode is not None:
        result = _session_payload(None, session, running=False)
        _sessions.pop(session_id, None)
        return result

    session["deadline"] = loop.time() + float(timeout)
    return _session_payload(session_id, session, running=True)


@app.post("/api/run/stdin")
async def send_stdin(body: StdinRequest) -> dict[str, Any]:
    session = _sessions.get(body.sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    proc: asyncio.subprocess.Process = session["proc"]
    if proc.stdin is None:
        raise HTTPException(status_code=400, detail="stdin closed")
    if body.eof:
        proc.stdin.close()
    else:
        data = body.data if body.data.endswith("\n") else body.data + "\n"
        proc.stdin.write(data.encode())
        await proc.stdin.drain()

    stdout = _strip_ansi(await _read_available(proc.stdout) if proc.stdout else "")
    stderr = _strip_ansi(await _read_available(proc.stderr) if proc.stderr else "")
    session["stdout"] += stdout
    session["stderr"] += stderr

    try:
        await asyncio.wait_for(proc.wait(), timeout=0.2)
    except asyncio.TimeoutError:
        return {
            "sessionId": body.sessionId,
            "running": True,
            "exitCode": None,
            "stdout": _strip_ansi(session["stdout"]),
            "stderr": _strip_ansi(session["stderr"]),
            "waitingForInput": True,
        }

    stdout2 = _strip_ansi(await _read_available(proc.stdout) if proc.stdout else "")
    stderr2 = _strip_ansi(await _read_available(proc.stderr) if proc.stderr else "")
    session["stdout"] += stdout2
    session["stderr"] += stderr2
    result = {
        "sessionId": body.sessionId,
        "running": False,
        "exitCode": proc.returncode,
        "stdout": _strip_ansi(session["stdout"]),
        "stderr": _strip_ansi(session["stderr"]),
    }
    _sessions.pop(body.sessionId, None)
    return result


@app.post("/api/run/kill")
async def kill_session(sessionId: str) -> dict[str, str]:
    session = _sessions.pop(sessionId, None)
    if not session:
        return {"status": "gone"}
    proc: asyncio.subprocess.Process = session["proc"]
    try:
        proc.send_signal(signal.SIGTERM)
        try:
            await asyncio.wait_for(proc.wait(), timeout=1)
        except asyncio.TimeoutError:
            proc.kill()
    except ProcessLookupError:
        pass
    return {"status": "killed"}


@app.on_event("startup")
async def _startup() -> None:
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
