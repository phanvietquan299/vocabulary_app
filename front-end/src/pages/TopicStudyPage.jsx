import { useEffect, useState } from 'react'
import { Navigate, useParams } from 'react-router-dom'
import RequireSession from '../components/shared/RequireSession'
import StudyCard from '../components/study/StudyCard'
import StudyNavigator from '../components/study/StudyNavigator'
import StudyToolbar from '../components/study/StudyToolbar'
import {
  getFlashcardExam,
  getMultipleChoiceExam,
  getTopicById,
  markWordAsLearned,
  removeWordAsLearned,
} from '../data/topicService'
import { useLearnedWordsRealtime } from '../context/useLearnedWordsRealtime'
import { formatRelativeLearnTime } from '../utils/relativeTime'
import { getStoredUserId } from '../utils/session'
import './TopicExperience.css'

function TopicStudyPageContent() {
  const { topicId } = useParams()
  const sessionId = getStoredUserId()
  const [topic, setTopic] = useState(null)
  const [mode, setMode] = useState('flashcard')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedOption, setSelectedOption] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [examData, setExamData] = useState(null)
  const [examLoading, setExamLoading] = useState(false)
  const [examError, setExamError] = useState('')
  const [savingLearned, setSavingLearned] = useState(false)
  const [saveLearnedError, setSaveLearnedError] = useState('')
  const { learnedWords, loading: learnedWordsLoading, error: learnedWordsError } = useLearnedWordsRealtime()

  useEffect(() => {
    let ignore = false

    async function loadTopic() {
      setLoading(true)
      setError('')

      try {
        const topicData = await getTopicById(topicId)

        if (!ignore) {
          setTopic(topicData)
          setCurrentIndex(0)
          setSelectedOption('')
          setExamData(null)
          setExamError('')
        }
      } catch (fetchError) {
        if (!ignore) {
          setError(fetchError.message || 'Cannot load topic vocabulary.')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadTopic()

    return () => {
      ignore = true
    }
  }, [topicId, sessionId])

  const learnedWordMap = new Map(learnedWords.map((word) => [word.id, word]))
  const resolvedTopic = topic
    ? {
        ...topic,
        words: topic.words.map((word) => {
          const learnedWord = learnedWordMap.get(word.id)

          if (!learnedWord) {
            return {
              ...word,
              learned: false,
              learnAt: null,
            }
          }

          return {
            ...word,
            learned: true,
            learnAt: learnedWord.learnAt,
          }
        }),
      }
    : null

  const currentWord = resolvedTopic?.words?.[currentIndex]
  const currentWordId = currentWord?.id ?? null

  useEffect(() => {
    let ignore = false

    async function loadExamData() {
      if (!currentWordId) {
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

  if (!loading && !resolvedTopic) {
    return <Navigate to="/home" replace />
  }

  if (!resolvedTopic || resolvedTopic.words.length === 0) {
    return (
      <main className="topic-page-shell">
        <div className="container-fluid py-4 py-lg-5">
          <div className="topic-page-frame mx-auto">
            {loading ? <div className="topic-feedback">Dang tai topic...</div> : null}
            {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}
          </div>
        </div>
      </main>
    )
  }

  const resolvedWord = currentWord ?? resolvedTopic.words[0]
  const totalLearned = resolvedTopic.words.filter((word) => word.learned).length

  function handleModeChange(nextMode) {
    setMode(nextMode)
  }

  function handlePrevious() {
    setCurrentIndex((index) => Math.max(index - 1, 0))
  }

  function handleNext() {
    setCurrentIndex((index) => Math.min(index + 1, topic.words.length - 1))
  }

  async function handleToggleLearned(checked) {
    setSaveLearnedError('')
    setSavingLearned(true)

    try {
      if (checked) {
        await markWordAsLearned(sessionId, resolvedWord.id)
      } else {
        await removeWordAsLearned(sessionId, resolvedWord.id)
      }
    } catch (saveError) {
      setSaveLearnedError(saveError.message || 'Cannot save learned progress.')
    } finally {
      setSavingLearned(false)
    }
  }

  return (
    <main className="topic-page-shell">
      <div className="container-fluid py-4 py-lg-5">
        <div className="topic-page-frame mx-auto">
          {loading ? <div className="topic-feedback">Dang tai topic...</div> : null}
          {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}
          {learnedWordsLoading ? <div className="topic-feedback">Dang dong bo tien do hoc...</div> : null}
          {learnedWordsError ? <div className="topic-feedback topic-feedback-error">{learnedWordsError}</div> : null}
          {examLoading ? <div className="topic-feedback">Dang tai noi dung bai hoc...</div> : null}
          {examError ? <div className="topic-feedback topic-feedback-error">{examError}</div> : null}
          {savingLearned ? <div className="topic-feedback">Dang cap nhat tien do hoc...</div> : null}
          {saveLearnedError ? <div className="topic-feedback topic-feedback-error">{saveLearnedError}</div> : null}

          <StudyToolbar
            mode={mode}
            onModeChange={handleModeChange}
            currentIndex={currentIndex}
            total={resolvedTopic.words.length}
            learned={Boolean(resolvedWord.learned)}
            totalLearned={totalLearned}
            subtitlePrefix={resolvedWord.learnAt ? `Hoc ${formatRelativeLearnTime(resolvedWord.learnAt)}` : ''}
          />

          <StudyCard
            word={resolvedWord}
            mode={mode}
            examData={examData}
            isLearned={Boolean(resolvedWord.learned)}
            isSavingLearned={savingLearned}
            onToggleLearned={handleToggleLearned}
            selectedOption={selectedOption}
            onSelectOption={setSelectedOption}
            metaText={resolvedWord.learnAt ? `Da hoc ${formatRelativeLearnTime(resolvedWord.learnAt)}` : ''}
          />

          <StudyNavigator
            topicId={resolvedTopic.id}
            currentIndex={currentIndex}
            total={resolvedTopic.words.length}
            onPrevious={handlePrevious}
            onNext={handleNext}
          />
        </div>
      </div>
    </main>
  )
}

export default function TopicStudyPage() {
  return (
    <RequireSession>
      <TopicStudyPageContent />
    </RequireSession>
  )
}
