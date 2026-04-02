import { Link } from 'react-router-dom'

export default function StudyNavigator({
  topicId,
  currentIndex,
  total,
  onPrevious,
  onNext,
}) {
  return (
    <div className="study-nav-bar">
      <Link to={`/topics/${topicId}`} className="btn btn-outline-secondary">
        Xem danh sach tu
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
