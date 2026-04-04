import FlashcardMode from './FlashcardMode'
import MultipleChoiceMode from './MultipleChoiceMode'

export default function StudyCard({
  word,
  mode,
  examData,
  isLearned,
  isSavingLearned,
  onToggleLearned,
  selectedOption,
  onSelectOption,
  metaText = '',
}) {
  return (
    <section className="study-card">
      <label className="study-check">
        <input
          type="checkbox"
          checked={isLearned}
          disabled={isSavingLearned}
          onChange={(event) => onToggleLearned(event.target.checked)}
        />
        <span>{isSavingLearned ? 'Dang luu...' : 'Da hoc'}</span>
      </label>

      {metaText ? <p className="study-meta-note mb-0">{metaText}</p> : null}

      {mode === 'flashcard' ? (
        <FlashcardMode examData={examData} fallbackWord={word} />
      ) : (
        <MultipleChoiceMode
          examData={examData}
          selectedOption={selectedOption}
          onSelectOption={onSelectOption}
        />
      )}
    </section>
  )
}
