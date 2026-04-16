export default function CircularProgress({ value = 0, label, subtitle }) {
  const clampedValue = Math.max(0, Math.min(100, value))

  return (
    <div
      className="circular-progress"
      style={{ background: `conic-gradient(#000000 0 ${clampedValue}%, #eceff3 ${clampedValue}% 100%)` }}
      aria-label={`${label}: ${Math.round(clampedValue)}%`}
    >
      <div className="circular-progress__inner">
        <span className="circular-progress__value">{Math.round(clampedValue)}%</span>
        <span className="circular-progress__label">{label}</span>
        <span className="circular-progress__subtitle">{subtitle}</span>
      </div>
    </div>
  )
}