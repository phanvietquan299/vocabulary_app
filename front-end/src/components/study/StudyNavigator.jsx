import { Link } from 'react-router-dom'

export default function StudyNavigator({
  topicId,
  currentIndex,
  total,
  onPrevious,
  onNext,
  backTo,
  backLabel,
}) {
  const resolvedBackTo = backTo ?? `/topics/${topicId}`
  const resolvedBackLabel = backLabel ?? 'Xem danh sach tu'

  return (
    <div className="study-nav-bar">
      <Link to={resolvedBackTo} className="btn btn-outline-secondary">
        {resolvedBackLabel}
      </Link>

      <div className="d-flex flex-wrap justify-content-center gap-2">
        <button
          type="button"
          className="btn btn-outline-dark"
          onClick={onPrevious}
          disabled={currentIndex === 0}
        >
          Previous
        </button>
        <button
          type="button"
          className="btn btn-dark"
          onClick={onNext}
          disabled={currentIndex === total - 1}
        >
          Next
        </button>
      </div>
    </div>
  )
}
