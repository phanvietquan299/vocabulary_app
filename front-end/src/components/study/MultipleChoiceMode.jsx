const LETTERS = ['A', 'B', 'C', 'D']

export default function MultipleChoiceMode({
  examData,
  selectedOption,
  onSelectOption,
}) {
  const options = (examData?.answers ?? []).map((answer) => ({
    id: answer,
    label: answer,
    correct: answer === examData?.correct_answer,
  }))
  const selectedChoice = options.find((option) => option.id === selectedOption)
  const answerState = selectedChoice
    ? selectedChoice.correct
      ? 'Dung roi'
      : `Chua dung. Dap an la "${examData?.correct_answer}".`
    : 'Chon mot dap an de kiem tra.'

  return (
    <div className="study-mode-content">
      <p className="study-question-label mb-2">Trac nghiem</p>
      <h2 className="study-word mb-3">Tu "{examData?.word}" co nghia la gi?</h2>

      <div className="study-options">
        {options.map((option, index) => {
          const isSelected = option.id === selectedOption
          const extraClass = isSelected
            ? option.correct
              ? ' study-option-correct'
              : ' study-option-wrong'
            : ''

          return (
            <button
              key={option.id}
              type="button"
              className={`study-option${extraClass}`}
              onClick={() => onSelectOption(option.id)}
            >
              <span className="study-option-letter">{LETTERS[index]}</span>
              <span>{option.label}</span>
            </button>
          )
        })}
      </div>

      <p className="study-feedback mb-0">{answerState}</p>
    </div>
  )
}
