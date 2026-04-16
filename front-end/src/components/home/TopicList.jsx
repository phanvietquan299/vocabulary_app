import TopicCard from './TopicCard'
import { DashboardTopicGroup } from './DashboardComposite'

export default function TopicList({ topics }) {
  const coreTopics = topics

  return (
    <div className="topics-panel">
      <DashboardTopicGroup
        title="Topic Collection"
      >
        {coreTopics.map((topic) => (
          <TopicCard
            key={topic.id}
            topicId={topic.id}
            kicker="Topic"
            title={topic.title}
            subtitle={topic.subtitle}
            badges={[`${topic.learned}/${topic.total} tu`, `${topic.progress}%`]}
            coverImageUrl={topic.coverImageUrl}
          />
        ))}
      </DashboardTopicGroup>
    </div>
  )
}
