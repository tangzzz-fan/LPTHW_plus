import { useEffect, useRef } from 'react'
import Editor, { type OnMount } from '@monaco-editor/react'
import type { editor as MonacoEditor } from 'monaco-editor'

type EditorPaneProps = {
  path: string | null
  value: string
  onChange: (value: string) => void
  onSave: () => void
  onRun: () => void
  saving?: boolean
  running?: boolean
}

const isMac =
  typeof navigator !== 'undefined' &&
  (/Mac|iPhone|iPad|iPod/i.test(navigator.platform) ||
    navigator.userAgent.includes('Mac'))

const mod = isMac ? '⌘' : 'Ctrl'

export function EditorPane({
  path,
  value,
  onChange,
  onSave,
  onRun,
  saving,
  running,
}: EditorPaneProps) {
  const hostRef = useRef<HTMLDivElement>(null)
  const editorRef = useRef<MonacoEditor.IStandaloneCodeEditor | null>(null)
  const onSaveRef = useRef(onSave)
  const onRunRef = useRef(onRun)
  const savingRef = useRef(saving)
  const runningRef = useRef(running)
  const pathRef = useRef(path)
  const lockRef = useRef(false)
  onSaveRef.current = onSave
  onRunRef.current = onRun
  savingRef.current = saving
  runningRef.current = running
  pathRef.current = path

  const run = () => {
    if (runningRef.current || lockRef.current) return
    lockRef.current = true
    onRunRef.current()
    window.setTimeout(() => {
      lockRef.current = false
    }, 1000)
  }

  const save = () => {
    if (!pathRef.current || savingRef.current || lockRef.current) return
    onSaveRef.current()
  }

  // Global shortcuts in capture phase so they win over Monaco's default handling.
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const modPressed = isMac ? e.metaKey : e.ctrlKey
      if (!modPressed || e.altKey || e.shiftKey) return

      const isEnter =
        e.key === 'Enter' || e.code === 'Enter' || e.code === 'NumpadEnter'
      const isS = e.key === 's' || e.key === 'S' || e.code === 'KeyS'
      if (!isEnter && !isS) return

      const t = e.target as HTMLElement | null
      if (isS && t?.closest?.('.terminal-input-row')) return

      e.preventDefault()
      e.stopPropagation()
      if (typeof e.stopImmediatePropagation === 'function') {
        e.stopImmediatePropagation()
      }
      if (isEnter) run()
      else save()
    }
    window.addEventListener('keydown', onKeyDown, true)
    return () => window.removeEventListener('keydown', onKeyDown, true)
  }, [])

  // Keep Monaco in sync when splitters resize the panel (automaticLayout alone is flaky in CSS grid).
  useEffect(() => {
    const host = hostRef.current
    if (!host || typeof ResizeObserver === 'undefined') return
    const ro = new ResizeObserver(() => {
      editorRef.current?.layout()
    })
    ro.observe(host)
    return () => ro.disconnect()
  }, [])

  const handleMount: OnMount = (ed, monaco) => {
    editorRef.current = ed
    ed.layout()
    // Backup when focus is inside Monaco (some builds swallow keys oddly).
    ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => run())
    ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => save())
  }

  return (
    <div className="editor-pane">
      <div className="editor-toolbar">
        <span className="editor-path" title={path ?? undefined}>
          {path ?? '未打开文件'}
        </span>
        <div className="editor-actions">
          <button
            type="button"
            className="btn"
            onClick={save}
            disabled={!path || saving}
            title={`${mod}+S`}
          >
            {saving ? '保存中…' : `保存 ${mod}+S`}
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={run}
            disabled={running}
            title={`${mod}+Enter`}
          >
            {running ? '运行中…' : `运行 ${mod}+Enter`}
          </button>
        </div>
      </div>
      <div className="editor-host" ref={hostRef}>
        <Editor
          height="100%"
          width="100%"
          language="python"
          theme="vs-dark"
          value={value}
          onMount={handleMount}
          onChange={(v) => onChange(v ?? '')}
          options={{
            fontSize: 13,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: 'on',
            padding: { top: 8 },
          }}
        />
      </div>
    </div>
  )
}
