import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import RequireSession from '../components/shared/RequireSession'
import StudyCard from '../components/study/StudyCard'
import StudyNavigator from '../components/study/StudyNavigator'
import StudyToolbar from '../components/study/StudyToolbar'
import {
  getFlashcardExam,
  getMultipleChoiceExam,
  removeWordAsLearned,
} from '../data/topicService'
import { useLearnedWordsRealtime } from '../context/useLearnedWordsRealtime'
import { formatRelativeLearnTime } from '../utils/relativeTime'
import { getStoredUserId } from '../utils/session'
import './TopicExperience.css'

function ReviewSessionPageContent() {
  const sessionId = getStoredUserId()
  const [mode, setMode] = useState('flashcard')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedOption, setSelectedOption] = useState('')
  const [examData, setExamData] = useState(null)
  const [examLoading, setExamLoading] = useState(false)
  const [examError, setExamError] = useState('')
  const [savingLearned, setSavingLearned] = useState(false)
  const [saveLearnedError, setSaveLearnedError] = useState('')
  const { learnedWords, loading, error } = useLearnedWordsRealtime()

  const reviewWords = learnedWords
    .filter((word) => word.learned)
    .sort((left, right) => {
      const leftTime = left.learnAt ? new Date(left.learnAt).getTime() : 0
      const rightTime = right.learnAt ? new Date(right.learnAt).getTime() : 0
      return leftTime - rightTime
    })

  useEffect(() => {
    setCurrentIndex((index) => {
      if (reviewWords.length === 0) {
        return 0
      }

      return Math.min(index, reviewWords.length - 1)
    })
  }, [reviewWords.length])

  const currentWord = reviewWords[currentIndex] ?? null
  const currentWordId = currentWord?.id ?? null

  useEffect(() => {
    let ignore = false

    async function loadExamData() {
      if (!currentWordId) {
        setExamData(null)
        return
      }

      setExamLoading(true)
      setExamError('')

      try {
        const nextExamData = mode === 'flashcard'
          ? await getFlashcardExam(currentWordId)
          : await getMultipleChoiceExam(currentWordId)

        if (!ignore) {
          setExamData(nextExamData)
        }
      } catch (fetchError) {
        if (!ignore) {
          setExamError(fetchError.message || 'Cannot load exam data.')
          setExamData(null)
        }
      } finally {
        if (!ignore) {
          setExamLoading(false)
        }
      }
    }

    setSelectedOption('')
    loadExamData()

    return () => {
      ignore = true
    }
  }, [mode, currentWordId])

  async function handleToggleLearned(checked) {
    if (!currentWord) {
      return
    }

    setSaveLearnedError('')
    setSavingLearned(true)

    try {
      if (!checked) {
        await removeWordAsLearned(sessionId, currentWord.id)
        return
      }
    } catch (saveError) {
      setSaveLearnedError(saveError.message || 'Cannot save learned progress.')
    } finally {
      setSavingLearned(false)
    }
  }

  if (!sessionId) {
    return <Navigate to="/" replace />
  }

  if (!loading && reviewWords.length === 0) {
    return (
      <main className="topic-page-shell">
        <div className="container-fluid py-4 py-lg-5">
          <div className="topic-page-frame mx-auto">
            <header className="study-toolbar">
              <div>
                <p className="topic-page-eyebrow mb-2">Review session</p>
                <h1 className="study-toolbar-title mb-1">On tap tu da hoc</h1>
                <p className="study-toolbar-subtitle mb-0">
                  Chua co tu nao duoc danh dau la da hoc de dua vao review session.
                </p>
              </div>
            </header>

            {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}

            <div className="topic-feedback">
              Khi ban danh dau mot tu la <strong>Da hoc</strong> trong topic, tu do se xuat hien tai day de on tap lai.
            </div>

            <StudyNavigator
              currentIndex={0}
              total={1}
              onPrevious={() => {}}
              onNext={() => {}}
              backTo="/home"
              backLabel="Home"
            />
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="topic-page-shell">
      <div className="container-fluid py-4 py-lg-5">
        <div className="topic-page-frame mx-auto">
          {loading ? <div className="topic-feedback">Dang tai review session...</div> : null}
          {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}
          {examLoading ? <div className="topic-feedback">Dang tai noi dung on tap...</div> : null}
          {examError ? <div className="topic-feedback topic-feedback-error">{examError}</div> : null}
          {savingLearned ? <div className="topic-feedback">Dang cap nhat danh sach review...</div> : null}
          {saveLearnedError ? <div className="topic-feedback topic-feedback-error">{saveLearnedError}</div> : null}

          {currentWord ? (
            <>
              <StudyToolbar
                mode={mode}
                onModeChange={setMode}
                currentIndex={currentIndex}
                total={reviewWords.length}
                learned
                totalLearned={reviewWords.length}
                eyebrow="Review session"
                title="Practice learned words"
                subtitlePrefix={`Lan hoc truoc ${formatRelativeLearnTime(currentWord.learnAt)}`}
              />

              <StudyCard
                word={currentWord}
                mode={mode}
                examData={examData}
                isLearned
                isSavingLearned={savingLearned}
                onToggleLearned={handleToggleLearned}
                selectedOption={selectedOption}
                onSelectOption={setSelectedOption}
                metaText={`Da hoc ${formatRelativeLearnTime(currentWord.learnAt)}`}
              />

              <StudyNavigator
                currentIndex={currentIndex}
                total={reviewWords.length}
                onPrevious={() => setCurrentIndex((index) => Math.max(index - 1, 0))}
                onNext={() => setCurrentIndex((index) => Math.min(index + 1, reviewWords.length - 1))}
                backTo="/home"
                backLabel="Home"
              />
            </>
          ) : null}
        </div>
      </div>
    </main>
  )
}

export default function ReviewSessionPage() {
  return (
    <RequireSession>
      <ReviewSessionPageContent />
    </RequireSession>
  )
}
