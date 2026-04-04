import { Link } from 'react-router-dom'

export default function TopicCard({
  kicker,
  title,
  subtitle,
  badges = [],
  review = false,
  topicId,
  primaryActionTo,
  primaryActionLabel = 'Kiem tra',
  secondaryActionTo,
  secondaryActionLabel = 'Hoc',
}) {
  const hasActions = Boolean(topicId || primaryActionTo)
  const resolvedSecondaryActionTo = secondaryActionTo ?? (topicId ? `/topics/${topicId}` : null)
  const resolvedPrimaryActionTo = primaryActionTo ?? (topicId ? `/topics/${topicId}/study` : null)

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
        {hasActions ? (
          <div className="topic-actions">
            {resolvedSecondaryActionTo ? (
              <Link
                to={resolvedSecondaryActionTo}
                className="btn btn-sm btn-outline-primary"
              >
                {secondaryActionLabel}
              </Link>
            ) : null}
            <Link to={resolvedPrimaryActionTo} className="btn btn-sm btn-primary">
              {primaryActionLabel}
            </Link>
          </div>
        ) : null}
      </div>
    </article>
  )
}
