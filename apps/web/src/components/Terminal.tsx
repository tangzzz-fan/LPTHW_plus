import { useEffect, useRef, useState, type KeyboardEvent } from 'react'

type TerminalProps = {
  output: string
  waitingForInput: boolean
  onSubmitInput: (line: string) => void
}

export function Terminal({
  output,
  waitingForInput,
  onSubmitInput,
}: TerminalProps) {
  const [input, setInput] = useState('')
  const endRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [output])

  useEffect(() => {
    if (waitingForInput) {
      // Keep focus after each prompt refresh (e.g. next room in a game).
      inputRef.current?.focus()
    }
  }, [waitingForInput, output])

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key !== 'Enter') return
    e.preventDefault()
    const line = input
    setInput('')
    onSubmitInput(line)
  }

  return (
    <div className="terminal">
      <div className="panel-header">
        <span className="panel-label">终端</span>
        {waitingForInput && (
          <span className="badge waiting">等待输入</span>
        )}
      </div>
      <pre className="terminal-output">
        {output || '（运行结果会显示在这里）'}
        <div ref={endRef} />
      </pre>
      <div className="terminal-input-row">
        <span className="prompt">{'>'}</span>
        <input
          ref={inputRef}
          className="terminal-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={waitingForInput ? '输入后按 Enter…' : 'stdin'}
          disabled={!waitingForInput}
          spellCheck={false}
          autoComplete="off"
        />
      </div>
    </div>
  )
}
