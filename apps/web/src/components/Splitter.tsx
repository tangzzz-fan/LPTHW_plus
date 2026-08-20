import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from 'react'

type SplitterProps = {
  /** Horizontal = drag left/right (column widths). Vertical = drag up/down. */
  orientation?: 'horizontal' | 'vertical'
  onDrag: (deltaPx: number) => void
  title?: string
  className?: string
}

/** Thin drag handle between panels. */
export function Splitter({
  orientation = 'horizontal',
  onDrag,
  title,
  className,
}: SplitterProps) {
  const dragging = useRef(false)
  const last = useRef(0)

  const onPointerDown = useCallback(
    (e: ReactPointerEvent<HTMLDivElement>) => {
      e.preventDefault()
      dragging.current = true
      last.current = orientation === 'horizontal' ? e.clientX : e.clientY
      e.currentTarget.setPointerCapture(e.pointerId)
      document.body.classList.add(
        orientation === 'horizontal' ? 'col-resizing' : 'row-resizing',
      )
    },
    [orientation],
  )

  const onPointerMove = useCallback(
    (e: ReactPointerEvent<HTMLDivElement>) => {
      if (!dragging.current) return
      const pos = orientation === 'horizontal' ? e.clientX : e.clientY
      const delta = pos - last.current
      last.current = pos
      if (delta !== 0) onDrag(delta)
    },
    [onDrag, orientation],
  )

  const end = useCallback((e: ReactPointerEvent<HTMLDivElement>) => {
    if (!dragging.current) return
    dragging.current = false
    try {
      e.currentTarget.releasePointerCapture(e.pointerId)
    } catch {
      /* ignore */
    }
    document.body.classList.remove('col-resizing', 'row-resizing')
  }, [])

  return (
    <div
      className={['splitter', `splitter-${orientation}`, className]
        .filter(Boolean)
        .join(' ')}
      role="separator"
      aria-orientation={orientation}
      title={title}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={end}
      onPointerCancel={end}
    />
  )
}

const LS_KEY = 'lpthw-layout'

type LayoutWidths = {
  sidebar: number
  right: number
  lessonPct: number
}

const DEFAULTS: LayoutWidths = {
  sidebar: 240,
  right: 300,
  lessonPct: 38,
}

function clamp(n: number, min: number, max: number) {
  return Math.min(max, Math.max(min, n))
}

export function useResizableLayout() {
  const [layout, setLayout] = useState<LayoutWidths>(() => {
    try {
      const raw = localStorage.getItem(LS_KEY)
      if (!raw) return DEFAULTS
      return { ...DEFAULTS, ...(JSON.parse(raw) as Partial<LayoutWidths>) }
    } catch {
      return DEFAULTS
    }
  })

  useEffect(() => {
    localStorage.setItem(LS_KEY, JSON.stringify(layout))
  }, [layout])

  const onSidebarDrag = useCallback((delta: number) => {
    setLayout((L) => ({
      ...L,
      sidebar: clamp(L.sidebar + delta, 160, 480),
    }))
  }, [])

  const onRightDrag = useCallback((delta: number) => {
    // Dragging the handle left of right-col: moving right grows right panel
    setLayout((L) => ({
      ...L,
      right: clamp(L.right - delta, 200, 560),
    }))
  }, [])

  const onLessonDrag = useCallback((delta: number) => {
    setLayout((L) => {
      // Approximate: convert px delta to % of main column height via window
      const h = Math.max(window.innerHeight - 40, 400)
      const pctDelta = (delta / h) * 100
      return {
        ...L,
        lessonPct: clamp(L.lessonPct + pctDelta, 18, 70),
      }
    })
  }, [])

  return { layout, onSidebarDrag, onRightDrag, onLessonDrag }
}
