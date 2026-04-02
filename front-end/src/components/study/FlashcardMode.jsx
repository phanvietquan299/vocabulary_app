export default function FlashcardMode({ examData, fallbackWord }) {
  const displayWord = examData?.word ?? fallbackWord.word
  const displayMeaning = examData?.meaning ?? fallbackWord.meaning
  const displayExample = examData?.example ?? fallbackWord.example

  return (
    <div className="study-mode-content">
      <p className="study-question-label mb-2">Flash card</p>
      <h2 className="study-word mb-3">{displayWord}</h2>
      <div className="study-divider" />
      <p className="study-answer-label mt-3 mb-1">Nghia</p>
      <p className="study-answer mb-3">{displayMeaning}</p>
      <p className="study-example-label mb-1">Vi du</p>
      <p className="study-example mb-0">{displayExample}</p>
    </div>
  )
}
