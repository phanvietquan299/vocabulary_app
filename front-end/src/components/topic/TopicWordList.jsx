import WordListCard from './WordListCard'

export default function TopicWordList({ words }) {
  return (
    <section className="topic-word-list">
      {words.map((word, index) => (
        <WordListCard key={word.id} word={word} index={index} />
      ))}
    </section>
  )
}
