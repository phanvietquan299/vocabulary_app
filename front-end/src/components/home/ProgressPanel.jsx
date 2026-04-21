import { useMemo, useState } from 'react'
import CircularProgress from './CircularProgress'
import { progressStrategies } from './ProgressStrategies'
import { importVocabularyFile } from '../../data/topicService'

export default function ProgressPanel({ items, overallProgress }) {
  const displayMode = 'percentage'
  const [selectedFile, setSelectedFile] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const strategy = progressStrategies[displayMode] ?? progressStrategies.percentage
  const dailyGoal = 20
  const dailyProgress = useMemo(() => {
    const learned = Number(overallProgress?.learned ?? 0)
    return Math.min(100, Math.round((learned / dailyGoal) * 100))
  }, [dailyGoal, overallProgress?.learned])

  async function handleImportSubmit(event) {
    event.preventDefault()
    const form = event.currentTarget

    if (!selectedFile) {
      alert('Please choose a CSV or JSON file before submitting.')
      return
    }

    setIsSubmitting(true)

    try {
      const result = await importVocabularyFile(selectedFile)
      alert(result.message || 'Import successful.')
      setSelectedFile(null)
      form.reset()
    } catch (error) {
      alert(error.message || 'Import failed.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <aside className="progress-panel">
      <div className="progress-sticky">
        <div className="progress-panel-header">
          <p className="progress-kicker mb-1">Daily Goal</p>
          <h2 className="progress-title mb-0">Tien do hoc</h2>
        </div>

        <div className="daily-goal-card">
          <CircularProgress
            value={dailyProgress}
            label="Daily Goal"
            subtitle={`${overallProgress?.learned ?? 0}/${dailyGoal} words`}
          />

          <div className="daily-goal-copy">
            <p className="daily-goal-eyebrow mb-1">Focus target</p>
            <h3 className="daily-goal-title mb-2">Keep the streak moving</h3>
            <p className="daily-goal-subtitle mb-0">
              Track your daily words and keep progress visible at a glance.
            </p>
          </div>
        </div>

        <section className="progress-card progress-card--summary">
          <div className="d-flex align-items-center justify-content-between mb-2">
            <span className="progress-label">Tong tien do</span>
            <span className="progress-value">{strategy.render(items[0] ?? { value: 0, displayValue: '0%' })}</span>
          </div>
          <div className="progress-card__meta">
            <span>{items[1]?.displayValue ?? '0 tu'}</span>
            <span>{items[2]?.displayValue ?? '0 tu'}</span>
          </div>
        </section>

        <section className="progress-card progress-card--import">
          <div className="progress-import-header">
            <span className="progress-label">Import vocabulary</span>
            <span className="progress-chip">CSV / JSON</span>
          </div>
          <p className="progress-import-copy mb-0">
            Upload a vocabulary file here to push new words into the database.
          </p>
          <form className="progress-import-form" onSubmit={handleImportSubmit}>
            <input
              className="progress-file-input"
              type="file"
              accept=".csv,.json,application/json,text/csv"
              onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
            />
            <button className="topic-btn topic-btn--solid progress-import-button" disabled={isSubmitting} type="submit">
              {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
          </form>
        </section>
      </div>
    </aside>
  )
}
