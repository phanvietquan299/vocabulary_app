const DIVISIONS = [
  { amount: 60, unit: 'second' },
  { amount: 60, unit: 'minute' },
  { amount: 24, unit: 'hour' },
  { amount: 7, unit: 'day' },
  { amount: 4.34524, unit: 'week' },
  { amount: 12, unit: 'month' },
  { amount: Number.POSITIVE_INFINITY, unit: 'year' },
]

const relativeTimeFormatter = new Intl.RelativeTimeFormat('vi', {
  numeric: 'auto',
})

export function formatRelativeLearnTime(value) {
  if (!value) {
    return 'Chua co thoi gian hoc'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return 'Chua co thoi gian hoc'
  }

  let duration = (date.getTime() - Date.now()) / 1000

  for (const division of DIVISIONS) {
    if (Math.abs(duration) < division.amount) {
      return relativeTimeFormatter.format(Math.round(duration), division.unit)
    }

    duration /= division.amount
  }

  return 'Chua co thoi gian hoc'
  // return date.toLocaleString('vi', { dateStyle: 'short', timeStyle: 'short' })
}
