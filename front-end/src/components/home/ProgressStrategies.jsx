export const progressStrategies = {
  percentage: {
    label: 'Percentage',
    render: (item) => `${Math.round(item.progressValue ?? item.value ?? 0)}%`,
  },
  number: {
    label: 'Number',
    render: (item) => item.displayValue ?? `${Math.round(item.value ?? 0)}`,
  },
  bar: {
    label: 'Bar',
    render: (item) => (
      <div className="progress-inline">
        <div className="progress-inline-track">
          <div className="progress-inline-fill" style={{ width: `${item.barValue ?? item.value ?? 0}%` }} />
        </div>
        <span className="progress-inline-copy">{item.displayValue ?? `${Math.round(item.value ?? 0)}%`}</span>
      </div>
    ),
  },
}