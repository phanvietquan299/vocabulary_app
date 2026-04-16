import { Link } from 'react-router-dom'

export default function TopicPageHeader({ title, subtitle, topicId }) {
  return (
    <header className="topic-page-header">
      <div>
        <p className="topic-page-eyebrow mb-2">Topic learning</p>
        <h1 className="topic-page-title mb-2">{title}</h1>
        <p className="topic-page-subtitle mb-0">{subtitle}</p>
      </div>

      <div className="d-flex flex-wrap gap-2">
        <Link to="/home" className="btn btn-outline-secondary">
          Home
        </Link>
      </div>
    </header>
  )
}
