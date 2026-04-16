import { useEffect, useMemo, useState } from 'react'
import { Link, Navigate, useParams } from 'react-router-dom'
import RequireSession from '../components/shared/RequireSession'
import TopicPageHeader from '../components/topic/TopicPageHeader'
import TopicStepCard from '../components/topic/TopicStepCard'
import TopicStepNavigator from '../components/topic/TopicStepNavigator'
import { getTopicById, markWordAsLearned } from '../data/topicService'
import { useLearnedWordsRealtime } from '../context/useLearnedWordsRealtime'
import { getStoredUserId } from '../utils/session'
import './TopicExperience.css'

function TopicWordsPageContent() {
  const { topicId } = useParams()
  const sessionId = getStoredUserId()
  const [topic, setTopic] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [completed, setCompleted] = useState(false)
  const [saving, setSaving] = useState(false)
  const [actionError, setActionError] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { learnedWords } = useLearnedWordsRealtime()

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
          setCompleted(false)
          setSaving(false)
          setActionError('')
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
  }, [topicId])

  const learnedWordMap = useMemo(
    () => new Map(learnedWords.map((word) => [word.id, word])),
    [learnedWords]
  )

  const resolvedTopic = topic
    ? {
        ...topic,
        words: topic.words.map((word) => {
          const learnedWord = learnedWordMap.get(word.id)

          if (!learnedWord) {
            return word
          }

          return {
            ...word,
            learned: true,
            learnAt: learnedWord.learnAt,
          }
        }),
      }
    : null

  if (!loading && !resolvedTopic) {
    return <Navigate to="/home" replace />
  }

  if (!loading && resolvedTopic && resolvedTopic.words.length === 0) {
    return (
      <main className="topic-page-shell">
        <div className="container-fluid py-4 py-lg-5">
          <div className="topic-page-frame mx-auto">
            <TopicPageHeader title={resolvedTopic.title} subtitle={resolvedTopic.subtitle} topicId={resolvedTopic.id} />
            <div className="topic-feedback">Topic nay chua co tu vung nao de hoc.</div>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="topic-page-shell">
      <div className="container-fluid py-4 py-lg-5">
        <div className="topic-page-frame mx-auto">
          {resolvedTopic ? (
            <TopicPageHeader
              title={resolvedTopic.title}
              subtitle={resolvedTopic.subtitle}
              topicId={resolvedTopic.id}
            />
          ) : null}

          {loading ? <div className="topic-feedback">Dang tai danh sach tu...</div> : null}
          {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}
          {actionError ? <div className="topic-feedback topic-feedback-error">{actionError}</div> : null}

          {resolvedTopic ? (
            completed ? (
              <section className="topic-completion-card">
                <div className="topic-completion-card__badge">Hoan thanh</div>
                <h2 className="topic-completion-card__title">Chuc mung ban da hoan thanh topic nay</h2>
                <p className="topic-completion-card__text">
                  Ban da di qua {resolvedTopic.words.length} tu vung.
                </p>
                <div className="topic-completion-card__actions">
                  <button type="button" className="btn btn-dark" onClick={() => setCompleted(false)}>
                    Hoc lai
                  </button>
                  <Link to="/home" className="btn btn-outline-secondary">
                    Ve dashboard
                  </Link>
                </div>
              </section>
            ) : (
              <section className="topic-step-shell">
                <TopicStepCard
                  word={resolvedTopic.words[currentIndex]}
                  index={currentIndex}
                  total={resolvedTopic.words.length}
                />

                <TopicStepNavigator
                  onBack={() => setCurrentIndex((index) => Math.max(index - 1, 0))}
                  onNext={async () => {
                    const currentWord = resolvedTopic.words[currentIndex]

                    if (!currentWord || saving) {
                      return
                    }

                    setActionError('')
                    setSaving(true)

                    try {
                      await markWordAsLearned(sessionId, currentWord.id)

                      if (currentIndex === resolvedTopic.words.length - 1) {
                        setCompleted(true)
                      } else {
                        setCurrentIndex((index) => index + 1)
                      }
                    } catch (saveError) {
                      setActionError(saveError.message || 'Cannot save learned progress.')
                    } finally {
                      setSaving(false)
                    }
                  }}
                  backDisabled={currentIndex === 0 || saving}
                  nextDisabled={saving}
                  nextLabel={currentIndex === resolvedTopic.words.length - 1 ? 'Hoan thanh' : 'Tiep theo'}
                />
              </section>
            )
          ) : null}
        </div>
      </div>
    </main>
  )
}

export default function TopicWordsPage() {
  return (
    <RequireSession>
      <TopicWordsPageContent />
    </RequireSession>
  )
}
