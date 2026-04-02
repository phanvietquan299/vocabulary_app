import TopicCard from './TopicCard'

export default function TopicList({ topics }) {
  return (
    <div className="topics-panel">
      <div className="topic-list">
        {topics.map((topic) => (
          <TopicCard
            key={topic.id}
            topicId={topic.id}
            kicker="Topic"
            title={topic.title}
            subtitle={topic.subtitle}
            badges={[`${topic.learned}/${topic.total} tu`, `${topic.progress}%`]}
          />
        ))}

        <TopicCard
          kicker="Spaced Repetition"
          title="Review Session"
          subtitle="On tap cac the sap den han va giu nhip do ghi nho lau dai."
          badges={['SR', 'Ready']}
          review
        />
      </div>
    </div>
  )
}
