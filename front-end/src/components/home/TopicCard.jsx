import { Link } from 'react-router-dom'

export default function TopicCard({
  kicker,
  title,
  subtitle,
  badges = [],
  review = false,
  topicId,
}) {
  return (
    <article className={`topic-card${review ? ' review-card' : ''}`}>
      <div>
        <p className="topic-kicker mb-1">{kicker}</p>
        <h2 className="topic-title mb-1">{title}</h2>
        <p className="topic-subtitle mb-0">{subtitle}</p>
      </div>

      <div className="topic-meta">
        {badges.map((badge) => (
          <span key={badge}>{badge}</span>
        ))}
        {topicId ? (
          <div className="topic-actions">
            <Link to={`/topics/${topicId}`} className="btn btn-sm btn-outline-primary">
              Hoc
            </Link>
            <Link to={`/topics/${topicId}/study`} className="btn btn-sm btn-primary">
              Kiem tra
            </Link>
          </div>
        ) : null}
      </div>
    </article>
  )
}
