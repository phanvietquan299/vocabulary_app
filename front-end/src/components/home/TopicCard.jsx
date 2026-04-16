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
  coverImageUrl,
}) {
  const hasActions = Boolean(topicId || primaryActionTo)
  const resolvedSecondaryActionTo = secondaryActionTo ?? (topicId ? `/topics/${topicId}` : null)
  const resolvedPrimaryActionTo = primaryActionTo ?? (topicId ? `/topics/${topicId}/study` : null)

  return (
    <article className={`topic-card${review ? ' review-card' : ''}`}>
      <div className="topic-card-media">
        <img
          className="topic-card-image"
          src={coverImageUrl ?? '/studying.png'}
          alt={title}
          loading="lazy"
        />
        <div className="topic-card-overlay">
          <div className="topic-card-copy">
            <p className="topic-kicker mb-1">{kicker}</p>
            <h2 className="topic-title mb-1">{title}</h2>
            <p className="topic-subtitle mb-0">{subtitle}</p>
          </div>
        </div>
      </div>

      <div className="topic-meta">
        <div className="topic-badge-row">
          {badges.map((badge) => (
            <span key={badge}>{badge}</span>
          ))}
        </div>
        {hasActions ? (
          <div className="topic-actions">
            {resolvedSecondaryActionTo ? (
              <Link
                to={resolvedSecondaryActionTo}
                className="topic-btn topic-btn--ghost"
              >
                {secondaryActionLabel}
              </Link>
            ) : null}
            <Link to={resolvedPrimaryActionTo} className="topic-btn topic-btn--solid">
              {primaryActionLabel}
            </Link>
          </div>
        ) : null}
      </div>
    </article>
  )
}
