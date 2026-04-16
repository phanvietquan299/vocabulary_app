import { VocabularyMediaDecorator } from '../media/VocabularyDecorators'

export default function TopicStepCard({ word, index, total }) {
  return (
    <VocabularyMediaDecorator
      word={word}
      imageUrl={word.imageUrl}
      audioUrl={word.audioUrl}
      pronunciation={word.pronunciation}
    >
      <article className="topic-step-card">
        <div className="topic-step-card__header">
          <div>
            <p className="topic-step-card__kicker mb-1">Step-by-step learning</p>
            <h2 className="topic-step-card__title mb-1">{word.word}</h2>
            <p className="topic-step-card__pronunciation mb-0">{word.pronunciation ?? 'No pronunciation yet'}</p>
          </div>

          <div className="topic-step-card__counter">
            <span>{String(index + 1).padStart(2, '0')}</span>
            <small>/ {total}</small>
          </div>
        </div>

        <div className="topic-step-card__body">
          <div>
            <p className="topic-step-card__label mb-1">Nghia</p>
            <p className="topic-step-card__meaning mb-0">{word.meaning}</p>
          </div>

          <div>
            <p className="topic-step-card__label mb-1">Vi du</p>
            <p className="topic-step-card__example mb-0">{word.example}</p>
          </div>
        </div>
      </article>
    </VocabularyMediaDecorator>
  )
}