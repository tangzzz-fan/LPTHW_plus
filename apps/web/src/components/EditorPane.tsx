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

export function EditorPane({
  path,
  value,
  onChange,
  onSave,
  onRun,
  saving,
  running,
}: EditorPaneProps) {
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
          >
            {saving ? '保存中…' : '保存'}
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={onRun}
            disabled={running}
          >
            {running ? '运行中…' : '运行'}
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
