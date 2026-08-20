import { useEffect, useRef } from 'react'
import Editor from '@monaco-editor/react'

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
  /Mac|iPhone|iPad|iPod/i.test(navigator.platform)

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
  const onSaveRef = useRef(onSave)
  const onRunRef = useRef(onRun)
  onSaveRef.current = onSave
  onRunRef.current = onRun

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const modPressed = isMac ? e.metaKey : e.ctrlKey
      if (!modPressed) return
      // Terminal stdin uses Enter alone; don't steal Cmd/Ctrl+Enter there either if focused
      const t = e.target as HTMLElement | null
      if (t?.closest?.('.terminal-input-row') && e.key !== 'Enter') return

      if (e.key === 'Enter') {
        e.preventDefault()
        onRunRef.current()
      } else if (e.key.toLowerCase() === 's') {
        e.preventDefault()
        onSaveRef.current()
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [])

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
            onClick={onSave}
            disabled={!path || saving}
            title={`${mod}+S`}
          >
            {saving ? '保存中…' : `保存 ${mod}+S`}
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={onRun}
            disabled={running}
            title={`${mod}+Enter`}
          >
            {running ? '运行中…' : `运行 ${mod}+Enter`}
          </button>
        </div>
      </div>
      <div className="editor-host">
        <Editor
          height="100%"
          language="python"
          theme="vs-dark"
          value={value}
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
