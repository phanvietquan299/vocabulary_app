export default function ProgressPanel({ items }) {
  return (
    <aside className="progress-panel">
      <div className="progress-sticky">
        <div className="progress-panel-header">
          <p className="progress-kicker mb-1">Progress</p>
          <h2 className="progress-title mb-0">Tien do hien tai</h2>
        </div>

        <div className="progress-stack">
          {items.map((item) => (
            <section className="progress-card" key={item.label}>
              <div className="d-flex align-items-center justify-content-between mb-2">
                <span className="progress-label">{item.label}</span>
                <span className="progress-value">{item.displayValue ?? `${item.value}%`}</span>
              </div>
              <div className="progress bar-shell">
                <div
                  className={`progress-bar bg-${item.tone}`}
                  role="progressbar"
                  style={{ width: `${item.barValue ?? item.value}%` }}
                  aria-valuenow={item.barValue ?? item.value}
                  aria-valuemin="0"
                  aria-valuemax="100"
                />
              </div>
            </section>
          ))}
        </div>
      </div>
    </aside>
  )
}
