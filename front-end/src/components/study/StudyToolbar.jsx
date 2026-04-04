export default function StudyToolbar({
  mode,
  onModeChange,
  currentIndex,
  total,
  learned,
  totalLearned,
  eyebrow = 'Topic exam',
  title = 'Practice and review',
  subtitlePrefix = '',
}) {
  const baseSubtitle = `Tu ${currentIndex + 1}/${total} • Da danh dau ${totalLearned}/${total} • Dang hoc: ${learned ? 'Da hoc' : 'Chua hoc'}`
  const resolvedSubtitle = subtitlePrefix
    ? `${subtitlePrefix} • ${baseSubtitle}`
    : baseSubtitle

  return (
    <header className="study-toolbar">
      <div>
        <p className="topic-page-eyebrow mb-2">{eyebrow}</p>
        <h1 className="study-toolbar-title mb-1">{title}</h1>
        <p className="study-toolbar-subtitle mb-0">{resolvedSubtitle}</p>
      </div>

      <div className="study-mode-box">
        <label htmlFor="study-mode" className="study-mode-label">
          Mode hoc
        </label>
        <select
          id="study-mode"
          className="form-select"
          value={mode}
          onChange={(event) => onModeChange(event.target.value)}
        >
          <option value="flashcard">Flash card</option>
          <option value="multiple-choice">Trac nghiem</option>
        </select>
      </div>
    </header>
  )
}
