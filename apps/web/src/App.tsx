import { useCallback, useEffect, useMemo, useState } from 'react'
import { Sidebar, type ExerciseSummary, type LessonProgress, type Track } from './components/Sidebar'
import { LessonView } from './components/LessonView'
import { EditorPane } from './components/EditorPane'
import { FileTree } from './components/FileTree'
import { Terminal } from './components/Terminal'
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
  const parts: string[] = []
  if (res.stdout) parts.push(res.stdout)
  if (res.stderr) parts.push(res.stderr)
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
  const [progress, setProgress] = useState<ProgressMap>(() => loadProgress())
  const [terminalOutput, setTerminalOutput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [waitingForInput, setWaitingForInput] = useState(false)
  const [saving, setSaving] = useState(false)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)

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
    },
    [],
  )

  const selectLesson = useCallback(
    async (lessonId: string) => {
      if (!activeTrack) return
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
    (res: RunResult, trackId: string, lessonId: string) => {
      setTerminalOutput(formatRunOutput(res))
      if (res.running && res.sessionId) {
        setSessionId(res.sessionId)
        setWaitingForInput(true)
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
    async (sid: string, trackId: string, lessonId: string) => {
      for (let i = 0; i < 600; i++) {
        await new Promise((r) => setTimeout(r, 300))
        const res = await api<RunResult>('/api/run', {
          method: 'POST',
          body: JSON.stringify({
            track: trackId,
            exerciseId: lessonId,
            sessionId: sid,
          }),
        })
        applyRunResult(res, trackId, lessonId)
        if (!res.running) return
      }
    },
    [applyRunResult],
  )

  const handleRun = useCallback(async () => {
    if (!activeTrack || !activeLessonId || running) return
    setRunning(true)
    setError(null)
    setWaitingForInput(false)
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
      applyRunResult(res, activeTrack, activeLessonId)
      if (res.running && res.sessionId) {
        // Keep UI responsive for input(); also poll long jobs.
        void pollSession(res.sessionId, activeTrack, activeLessonId)
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
      setTerminalOutput(
        (prev) =>
          `${prev}\n[error] ${e instanceof Error ? e.message : String(e)}`,
      )
    } finally {
      setRunning(false)
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
      setError(null)
      try {
        let res: RunResult
        try {
          res = await api<RunResult>('/api/run/stdin', {
            method: 'POST',
            body: JSON.stringify({ sessionId, data: line }),
          })
        } catch {
          res = await api<RunResult>('/api/run', {
            method: 'POST',
            body: JSON.stringify({
              track: activeTrack,
              exerciseId: activeLessonId,
              sessionId,
              stdin: line,
            }),
          })
        }
        applyRunResult(res, activeTrack, activeLessonId)
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e))
        setWaitingForInput(false)
        setSessionId(null)
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

      <div className="app-body">
        <Sidebar
          tracks={tracks}
          activeTrack={activeTrack}
          onSelectTrack={setActiveTrack}
          exercises={exercises}
          activeLessonId={activeLessonId}
          onSelectLesson={selectLesson}
          progress={trackProgress}
        />

        <main className="main-col">
          <section className="lesson-section">
            <LessonView title={lesson?.title} bodyMarkdown={bodyMarkdown} />
          </section>
          <section className="editor-section">
            <EditorPane
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
