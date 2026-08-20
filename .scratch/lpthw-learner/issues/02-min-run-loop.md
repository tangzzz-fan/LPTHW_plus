# 02 · Minimal code → run → stdout loop

Status: done
Type: AFK

## What to build

User can edit a small Python snippet, click Run, and see stdout/stderr from a real local Python process.

## Acceptance criteria

- [x] Editor (Monaco or equivalent) in the UI
- [x] `POST /api/run` executes code with timeout and returns stdout/stderr/exitCode
- [x] Running `print("hello")` shows hello in the terminal panel

## Blocked by

- 01 · Local scaffold
