export default function TopicStepNavigator({
  onBack,
  onNext,
  backDisabled,
  nextDisabled,
  nextLabel = 'Tiep theo',
}) {
  return (
    <div className="topic-step-nav">
      <button type="button" className="btn btn-outline-secondary topic-step-nav__button" onClick={onBack} disabled={backDisabled}>
        Quay lai
      </button>
      <button type="button" className="btn btn-dark topic-step-nav__button" onClick={onNext} disabled={nextDisabled}>
        {nextLabel}
      </button>
    </div>
  )
}