export type Track = {
  id: string
  title: string
  priority: boolean
}

export type ExerciseSummary = {
  id: string
  track: string
  title: string
  priority: boolean
  timeoutSec?: number
  requires?: string[]
  outlineOnly: boolean
}

export type LessonProgress = {
  opened?: boolean
  ranOk?: boolean
}

type SidebarProps = {
  tracks: Track[]
  activeTrack: string | null
  onSelectTrack: (trackId: string) => void
  exercises: ExerciseSummary[]
  activeLessonId: string | null
  onSelectLesson: (lessonId: string) => void
  progress: Record<string, LessonProgress>
}

export function Sidebar({
  tracks,
  activeTrack,
  onSelectTrack,
  exercises,
  activeLessonId,
  onSelectLesson,
  progress,
}: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-tracks">
        {tracks.map((t) => (
          <button
            key={t.id}
            type="button"
            className={`track-tab${activeTrack === t.id ? ' active' : ''}`}
            onClick={() => onSelectTrack(t.id)}
            title={t.title}
          >
            <span className="track-tab-title">{t.title}</span>
            {t.priority && <span className="badge priority">优先</span>}
          </button>
        ))}
      </div>

      <div className="sidebar-lessons">
        <div className="panel-label">课程</div>
        {exercises.length === 0 && (
          <p className="muted empty-hint">暂无课程</p>
        )}
        <ul className="lesson-list">
          {exercises.map((ex) => {
            const p = progress[ex.id] ?? {}
            return (
              <li key={ex.id}>
                <button
                  type="button"
                  className={`lesson-item${activeLessonId === ex.id ? ' active' : ''}${ex.outlineOnly ? ' outline-only' : ''}`}
                  onClick={() => onSelectLesson(ex.id)}
                >
                  <span className="lesson-checks">
                    <span
                      className={`check${p.opened ? ' on' : ''}`}
                      title="已打开"
                    >
                      ○
                    </span>
                    <span
                      className={`check${p.ranOk ? ' on' : ''}`}
                      title="运行成功"
                    >
                      ✓
                    </span>
                  </span>
                  <span className="lesson-title">{ex.title}</span>
                  {ex.priority && (
                    <span className="badge priority sm">优先</span>
                  )}
                  {ex.outlineOnly && (
                    <span className="badge outline sm">大纲</span>
                  )}
                </button>
              </li>
            )
          })}
        </ul>
      </div>
    </aside>
  )
}
