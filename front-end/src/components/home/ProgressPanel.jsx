import { useMemo } from 'react'
import CircularProgress from './CircularProgress'
import { progressStrategies } from './ProgressStrategies'

export default function ProgressPanel({ items, overallProgress }) {
  const displayMode = 'percentage'

  const strategy = progressStrategies[displayMode] ?? progressStrategies.percentage
  const dailyGoal = 20
  const dailyProgress = useMemo(() => {
    const learned = Number(overallProgress?.learned ?? 0)
    return Math.min(100, Math.round((learned / dailyGoal) * 100))
  }, [dailyGoal, overallProgress?.learned])

  return (
    <aside className="progress-panel">
      <div className="progress-sticky">
        <div className="progress-panel-header">
          <p className="progress-kicker mb-1">Daily Goal</p>
          <h2 className="progress-title mb-0">Tiến độ học</h2>
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
            <span className="progress-label">Tổng tiến độ</span>
            <span className="progress-value">{strategy.render(items[0] ?? { value: 0, displayValue: '0%' })}</span>
          </div>
          <div className="progress-card__meta">
            <span>{items[1]?.displayValue ?? '0 từ'}</span>
            <span>{items[2]?.displayValue ?? '0 từ'}</span>
          </div>
        </section>
      </div>
    </aside>
  )
}
