export function DashboardTopicGroup({ title, subtitle, children }) {
  return (
    <section className="topic-group">
      <div className="topic-group-header">
        <div>
          <p className="topic-group-kicker mb-1">Central Hub</p>
          <h2 className="topic-group-title mb-1">{title}</h2>
          <p className="topic-group-subtitle mb-0">{subtitle}</p>
        </div>
      </div>
      <div className="topic-grid">{children}</div>
    </section>
  )
}