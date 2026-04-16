import { VocabularyMediaDecorator } from '../media/VocabularyDecorators'

export default function WordListCard({ word, index }) {
  return (
    <VocabularyMediaDecorator
      word={word}
      imageUrl={word.imageUrl}
      audioUrl={word.audioUrl}
      pronunciation={word.pronunciation}
      compact
    >
      <article className="word-list-card">
        <div className="word-list-order">{String(index + 1).padStart(2, '0')}</div>
        <div className="word-list-main">
          <div className="d-flex flex-wrap align-items-center gap-2 mb-2">
            <h2 className="word-list-title mb-0">{word.word}</h2>
            <span className={`badge rounded-pill ${word.learned ? 'text-bg-success' : 'text-bg-light'}`}>
              {word.learned ? 'Da hoc' : 'Chua hoc'}
            </span>
          </div>
          <p className="word-list-meaning mb-2">{word.meaning}</p>
          <p className="word-list-example mb-0">{word.example}</p>
        </div>
      </article>
    </VocabularyMediaDecorator>
  )
}
