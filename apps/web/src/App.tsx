import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import { Sidebar, type ExerciseSummary, type LessonProgress, type Track } from './components/Sidebar'
import { LessonView } from './components/LessonView'
import { EditorPane } from './components/EditorPane'
import { FileTree } from './components/FileTree'
import { Terminal } from './components/Terminal'
import { Splitter, useResizableLayout } from './components/Splitter'
import './App.css'

const PROGRESS_KEY = 'lpthw-progress'

type ProgressMap = {
  [trackId: string]: {
    [lessonId: string]: LessonProgress
  }
}

type Lesson = {
  id: string
  track: string
  title: string
  body?: string
  bodyMarkdown?: string
  entry?: string
  starterFiles?: Record<string, string>
  priority?: boolean
  outlineOnly?: boolean
  timeoutSec?: number
  requires?: string[]
}

type RunResult = {
  sessionId?: string | null
  running?: boolean
  exitCode?: number | null
  stdout?: string
  stderr?: string
  waitingForInput?: boolean
}

function loadProgress(): ProgressMap {
  try {
    const raw = localStorage.getItem(PROGRESS_KEY)
    if (!raw) return {}
    return JSON.parse(raw) as ProgressMap
  } catch {
    return {}
  }
}

function saveProgress(map: ProgressMap) {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(map))
}

function formatRunOutput(res: RunResult): string {
  const stripAnsi = (s: string) =>
    s.replace(/\u001b\[[0-9;]*[A-Za-z]|\u001b\][^\u0007]*\u0007/g, '')
  const parts: string[] = []
  if (res.stdout) parts.push(stripAnsi(res.stdout))
  if (res.stderr) parts.push(stripAnsi(res.stderr))
  if (!res.running && res.exitCode != null) {
    parts.push(`\n[exit ${res.exitCode}]`)
  }
  return parts.join('')
}

async function api<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail ?? JSON.stringify(body)
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export default function App() {
  const [healthOk, setHealthOk] = useState<boolean | null>(null)
  const [tracks, setTracks] = useState<Track[]>([])
  const [activeTrack, setActiveTrack] = useState<string | null>(null)
  const [exercises, setExercises] = useState<ExerciseSummary[]>([])
  const [activeLessonId, setActiveLessonId] = useState<string | null>(null)
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [files, setFiles] = useState<{ path: string }[]>([])
  const [currentPath, setCurrentPath] = useState<string | null>(null)
  const [editorValue, setEditorValue] = useState('')
  const [editorEpoch, setEditorEpoch] = useState(0)
  const [progress, setProgress] = useState<ProgressMap>(() => loadProgress())
  const [terminalOutput, setTerminalOutput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [waitingForInput, setWaitingForInput] = useState(false)
  const [saving, setSaving] = useState(false)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { layout, onSidebarDrag, onRightDrag, onLessonDrag } =
    useResizableLayout()
  /** Bumped on lesson switch / new run so stale session polls cannot overwrite the terminal. */
  const runGenerationRef = useRef(0)

  const trackProgress = useMemo(
    () => (activeTrack ? progress[activeTrack] ?? {} : {}),
    [progress, activeTrack],
  )

  const markProgress = useCallback(
    (trackId: string, lessonId: string, patch: LessonProgress) => {
      setProgress((prev) => {
        const next: ProgressMap = {
          ...prev,
          [trackId]: {
            ...(prev[trackId] ?? {}),
            [lessonId]: {
              ...(prev[trackId]?.[lessonId] ?? {}),
              ...patch,
            },
          },
        }
        saveProgress(next)
        return next
      })
    },
    [],
  )

  // Health + tracks on mount
  useEffect(() => {
    let cancelled = false

    async function boot() {
      try {
        const health = await api<{ ok: boolean }>('/api/health')
        if (!cancelled) setHealthOk(!!health.ok)
      } catch {
        if (!cancelled) setHealthOk(false)
      }

      try {
        const list = await api<Track[]>('/api/tracks')
        if (cancelled) return
        setTracks(list)
        if (list.length > 0) {
          setActiveTrack(list[0].id)
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : String(e))
        }
      }
    }

    void boot()
    const timer = window.setInterval(async () => {
      try {
        const health = await api<{ ok: boolean }>('/api/health')
        if (!cancelled) setHealthOk(!!health.ok)
      } catch {
        if (!cancelled) setHealthOk(false)
      }
    }, 15000)

    return () => {
      cancelled = true
      window.clearInterval(timer)
    }
  }, [])

  // Load exercises when track changes
  useEffect(() => {
    if (!activeTrack) {
      setExercises([])
      return
    }
    let cancelled = false
    runGenerationRef.current += 1
    setActiveLessonId(null)
    setLesson(null)
    setFiles([])
    setCurrentPath(null)
    setEditorValue('')
    setTerminalOutput('')
    setSessionId(null)
    setWaitingForInput(false)

    async function loadExercises() {
      try {
        const list = await api<ExerciseSummary[]>(
          `/api/tracks/${activeTrack}/exercises`,
        )
        if (!cancelled) {
          setExercises(list)
          setError(null)
        }
      } catch (e) {
        if (!cancelled) {
          setExercises([])
          setError(e instanceof Error ? e.message : String(e))
        }
      }
    }

    void loadExercises()
    return () => {
      cancelled = true
    }
  }, [activeTrack])

  const refreshFiles = useCallback(async (track: string, lessonId: string) => {
    const list = await api<{ path: string }[]>(
      `/api/files/${track}/${lessonId}`,
    )
    setFiles(list)
    return list
  }, [])

  const openFile = useCallback(
    async (track: string, lessonId: string, path: string) => {
      const data = await api<{ path: string; content: string }>(
        `/api/files/${track}/${lessonId}/content?path=${encodeURIComponent(path)}`,
      )
      setCurrentPath(data.path)
      setEditorValue(data.content)
      setEditorEpoch((n) => n + 1)
    },
    [],
  )

  const selectLesson = useCallback(
    async (lessonId: string) => {
      if (!activeTrack) return
      runGenerationRef.current += 1
      setActiveLessonId(lessonId)
      setError(null)
      setTerminalOutput('')
      setSessionId(null)
      setWaitingForInput(false)
      markProgress(activeTrack, lessonId, { opened: true })

      try {
        const data = await api<Lesson>(
          `/api/exercises/${activeTrack}/${lessonId}`,
        )
        setLesson(data)

        const fileList = await refreshFiles(activeTrack, lessonId)
        const entry = data.entry || 'main.py'
        const preferred =
          fileList.find((f) => f.path === entry)?.path ??
          fileList[0]?.path ??
          null

        if (preferred) {
          await openFile(activeTrack, lessonId, preferred)
        } else {
          setCurrentPath(null)
          setEditorValue('')
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e))
      }
    },
    [activeTrack, markProgress, openFile, refreshFiles],
  )

  const handleSave = useCallback(async () => {
    if (!activeTrack || !activeLessonId || !currentPath) return
    setSaving(true)
    setError(null)
    try {
      await api(`/api/files/${activeTrack}/${activeLessonId}`, {
        method: 'PUT',
        body: JSON.stringify({ path: currentPath, content: editorValue }),
      })
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setSaving(false)
    }
  }, [activeTrack, activeLessonId, currentPath, editorValue])

  const applyRunResult = useCallback(
    (res: RunResult, trackId: string, lessonId: string, gen: number) => {
      if (gen !== runGenerationRef.current) return res
      setTerminalOutput(formatRunOutput(res))
      if (res.running && res.sessionId) {
        setSessionId(res.sessionId)
        setWaitingForInput(Boolean(res.waitingForInput))
      } else {
        setSessionId(null)
        setWaitingForInput(false)
        if (res.exitCode === 0) {
          markProgress(trackId, lessonId, { ranOk: true })
        }
      }
      return res
    },
    [markProgress],
  )

  const pollSession = useCallback(
    async (sid: string, trackId: string, lessonId: string, gen: number) => {
      for (let i = 0; i < 600; i++) {
        if (gen !== runGenerationRef.current) return
        await new Promise((r) => setTimeout(r, 300))
        if (gen !== runGenerationRef.current) return
        try {
          const res = await api<RunResult>('/api/run', {
            method: 'POST',
            body: JSON.stringify({
              track: trackId,
              exerciseId: lessonId,
              sessionId: sid,
            }),
          })
          if (gen !== runGenerationRef.current) return
          // If the server says it is waiting for stdin, stop polling — further
          // updates come from /api/run/stdin. Polling here races and clears the input box.
          if (res.waitingForInput) {
            applyRunResult(res, trackId, lessonId, gen)
            return
          }
          applyRunResult(res, trackId, lessonId, gen)
          if (!res.running) return
        } catch {
          // Do not clear waitingForInput — a transient 404/reload must not lock the box.
          return
        }
      }
    },
    [applyRunResult],
  )

  const handleRun = useCallback(async () => {
    if (!activeTrack || !activeLessonId || running) return
    const gen = ++runGenerationRef.current
    setRunning(true)
    setError(null)
    setWaitingForInput(false)
    setSessionId(null)
    setTerminalOutput('')
    try {
      const entry = lesson?.entry || currentPath || 'main.py'
      const res = await api<RunResult>('/api/run', {
        method: 'POST',
        body: JSON.stringify({
          track: activeTrack,
          exerciseId: activeLessonId,
          entry,
          code: editorValue,
          timeoutSec: lesson?.timeoutSec,
        }),
      })
      applyRunResult(res, activeTrack, activeLessonId, gen)
      if (
        res.running &&
        res.sessionId &&
        gen === runGenerationRef.current &&
        !res.waitingForInput
      ) {
        // Background compute only. Interactive input() sessions must not be polled.
        void pollSession(res.sessionId, activeTrack, activeLessonId, gen)
      }
    } catch (e) {
      if (gen === runGenerationRef.current) {
        setError(e instanceof Error ? e.message : String(e))
        setTerminalOutput(
          `[error] ${e instanceof Error ? e.message : String(e)}`,
        )
      }
    } finally {
      if (gen === runGenerationRef.current) {
        setRunning(false)
      }
    }
  }, [
    activeTrack,
    activeLessonId,
    currentPath,
    lesson?.entry,
    lesson?.timeoutSec,
    editorValue,
    applyRunResult,
    pollSession,
    running,
  ])

  const handleTerminalInput = useCallback(
    async (line: string) => {
      if (!sessionId || !activeTrack || !activeLessonId) return
      const gen = runGenerationRef.current
      const sid = sessionId
      setError(null)
      setTerminalOutput(
        (prev) =>
          `${prev}${prev.endsWith('\n') || !prev ? '' : '\n'}> ${line}\n`,
      )
      try {
        const res = await api<RunResult>('/api/run/stdin', {
          method: 'POST',
          body: JSON.stringify({ sessionId: sid, data: line }),
        })
        applyRunResult(res, activeTrack, activeLessonId, gen)
      } catch (e) {
        // Fallback: same session via /api/run + stdin field
        try {
          const res = await api<RunResult>('/api/run', {
            method: 'POST',
            body: JSON.stringify({
              track: activeTrack,
              exerciseId: activeLessonId,
              sessionId: sid,
              stdin: line,
            }),
          })
          applyRunResult(res, activeTrack, activeLessonId, gen)
        } catch (e2) {
          if (gen === runGenerationRef.current) {
            const msg = e2 instanceof Error ? e2.message : String(e2)
            setError(msg)
            setTerminalOutput(
              (prev) =>
                `${prev}\n[stdin 失败] ${msg}\n（若刚改过代码，API 可能热重载丢了会话：请再点一次「运行」）\n`,
            )
            setWaitingForInput(false)
            setSessionId(null)
          }
        }
      }
    },
    [sessionId, activeTrack, activeLessonId, applyRunResult],
  )

  const handleSelectFile = useCallback(
    async (path: string) => {
      if (!activeTrack || !activeLessonId) return
      try {
        await openFile(activeTrack, activeLessonId, path)
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e))
      }
    },
    [activeTrack, activeLessonId, openFile],
  )

  const handleNewFile = useCallback(async () => {
    if (!activeTrack || !activeLessonId) return
    const name = window.prompt('新文件名（相对路径）')
    if (!name || !name.trim()) return
    const path = name.trim().replace(/^\/+/, '')
    try {
      await api(`/api/files/${activeTrack}/${activeLessonId}`, {
        method: 'PUT',
        body: JSON.stringify({ path, content: '' }),
      })
      await refreshFiles(activeTrack, activeLessonId)
      await openFile(activeTrack, activeLessonId, path)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    }
  }, [activeTrack, activeLessonId, refreshFiles, openFile])

  const handleDeleteFile = useCallback(
    async (path: string) => {
      if (!activeTrack || !activeLessonId) return
      if (!window.confirm(`删除文件 ${path}？`)) return
      try {
        await api(
          `/api/files/${activeTrack}/${activeLessonId}?path=${encodeURIComponent(path)}`,
          { method: 'DELETE' },
        )
        const list = await refreshFiles(activeTrack, activeLessonId)
        if (currentPath === path) {
          const next = list[0]?.path ?? null
          if (next) {
            await openFile(activeTrack, activeLessonId, next)
          } else {
            setCurrentPath(null)
            setEditorValue('')
          }
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e))
      }
    },
    [activeTrack, activeLessonId, currentPath, refreshFiles, openFile],
  )

  const bodyMarkdown = lesson?.body ?? lesson?.bodyMarkdown ?? ''

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <span className="brand-mark">LPTHW</span>
          <span className="brand-sub">本地 Python 学习台</span>
        </div>
        <div className="header-right">
          {error && <span className="error-chip" title={error}>{error}</span>}
          <span
            className={`health${healthOk === true ? ' ok' : healthOk === false ? ' bad' : ''}`}
            title={
              healthOk === true
                ? 'API 正常'
                : healthOk === false
                  ? 'API 不可用'
                  : '检查中…'
            }
          >
            <span className="health-dot" />
            {healthOk === true ? 'API' : healthOk === false ? '离线' : '…'}
          </span>
        </div>
      </header>

      <div
        className="app-body"
        style={
          {
            '--sidebar-w': `${layout.sidebar}px`,
            '--right-w': `${layout.right}px`,
            '--lesson-pct': `${layout.lessonPct}%`,
          } as CSSProperties
        }
      >
        <Sidebar
          tracks={tracks}
          activeTrack={activeTrack}
          onSelectTrack={setActiveTrack}
          exercises={exercises}
          activeLessonId={activeLessonId}
          onSelectLesson={selectLesson}
          progress={trackProgress}
        />

        <Splitter
          orientation="horizontal"
          onDrag={onSidebarDrag}
          title="拖动调整左侧栏宽度"
          className="splitter-sidebar"
        />

        <main className="main-col">
          <section className="lesson-section">
            <LessonView title={lesson?.title} bodyMarkdown={bodyMarkdown} />
          </section>
          <Splitter
            orientation="vertical"
            onDrag={onLessonDrag}
            title="拖动调整课文 / 编辑器高度"
          />
          <section className="editor-section">
            <EditorPane
              key={`${activeLessonId ?? ''}:${currentPath ?? ''}:${editorEpoch}`}
              path={currentPath}
              value={editorValue}
              onChange={setEditorValue}
              onSave={handleSave}
              onRun={handleRun}
              saving={saving}
              running={running}
            />
          </section>
        </main>

        <Splitter
          orientation="horizontal"
          onDrag={onRightDrag}
          title="拖动调整编辑器 / 右侧栏宽度"
          className="splitter-right"
        />

        <aside className="right-col">
          <FileTree
            files={files}
            currentPath={currentPath}
            onSelect={handleSelectFile}
            onNewFile={handleNewFile}
            onDelete={handleDeleteFile}
          />
          <Terminal
            output={terminalOutput}
            waitingForInput={waitingForInput}
            onSubmitInput={handleTerminalInput}
          />
        </aside>
      </div>
    </div>
  )
}
