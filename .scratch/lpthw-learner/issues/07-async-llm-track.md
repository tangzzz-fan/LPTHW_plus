# 07 · Priority: Async / LLM enterprise track

Status: done (extended A01–A14)
Type: AFK

## What to build

Full runnable lessons for asyncio → httpx → streaming → semaphore → queue → structured retry → RAG → to_thread → HTTP backoff → FastAPI async → SSE consume → circuit breaker.

## Acceptance criteria

- [x] A01–A14 under `content/tracks/async-llm/`
- [x] Each lesson has explanation, starter, and can run locally
- [x] Marked as priority in UI
- [x] Enterprise gaps closed vs original plan: FastAPI async, sync-SDK bridge, HTTP retry/SSE, circuit breaker

## Out of scope (deeper in mit-python / mit-llm)

- Full observability stack (OpenTelemetry)
- Real vendor SDKs / auth
- TaskGroup-heavy structured concurrency (optional later)

## Blocked by

- 04 · Workspace files
- 05 · Interactive stdin
- 06 · Three-track nav
