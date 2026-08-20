import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type LessonViewProps = {
  title?: string
  bodyMarkdown?: string
}

export function LessonView({ title, bodyMarkdown }: LessonViewProps) {
  if (!bodyMarkdown && !title) {
    return (
      <div className="lesson-view empty">
        <p className="muted">选择左侧课程开始学习</p>
      </div>
    )
  }

  return (
    <div className="lesson-view">
      {title && <h1 className="lesson-heading">{title}</h1>}
      <div className="markdown-body">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {bodyMarkdown ?? ''}
        </ReactMarkdown>
      </div>
    </div>
  )
}
