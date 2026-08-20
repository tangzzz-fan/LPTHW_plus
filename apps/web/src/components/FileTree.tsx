type FileTreeProps = {
  files: { path: string }[]
  currentPath: string | null
  onSelect: (path: string) => void
  onNewFile: () => void
  onDelete: (path: string) => void
}

export function FileTree({
  files,
  currentPath,
  onSelect,
  onNewFile,
  onDelete,
}: FileTreeProps) {
  return (
    <div className="file-tree">
      <div className="panel-header">
        <span className="panel-label">文件</span>
        <button type="button" className="btn ghost sm" onClick={onNewFile}>
          新建
        </button>
      </div>
      <ul className="file-list">
        {files.length === 0 && (
          <li className="muted empty-hint">暂无文件</li>
        )}
        {files.map((f) => (
          <li key={f.path} className="file-row">
            <button
              type="button"
              className={`file-item${currentPath === f.path ? ' active' : ''}`}
              onClick={() => onSelect(f.path)}
            >
              {f.path}
            </button>
            <button
              type="button"
              className="btn ghost danger sm file-del"
              title="删除"
              onClick={() => onDelete(f.path)}
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
