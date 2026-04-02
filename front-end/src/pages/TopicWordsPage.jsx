import { useEffect, useState } from 'react'
import { Navigate, useParams } from 'react-router-dom'
import RequireSession from '../components/shared/RequireSession'
import TopicPageHeader from '../components/topic/TopicPageHeader'
import TopicWordList from '../components/topic/TopicWordList'
import { getTopicById } from '../data/topicService'
import './TopicExperience.css'

function TopicWordsPageContent() {
  const { topicId } = useParams()
  const [topic, setTopic] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadTopic() {
      setLoading(true)
      setError('')

      try {
        const topicData = await getTopicById(topicId)

        if (!ignore) {
          setTopic(topicData)
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

  if (!loading && !topic) {
    return <Navigate to="/home" replace />
  }

  return (
    <main className="topic-page-shell">
      <div className="container-fluid py-4 py-lg-5">
        <div className="topic-page-frame mx-auto">
          {topic ? (
            <TopicPageHeader
              title={topic.title}
              subtitle={topic.subtitle}
              topicId={topic.id}
            />
          ) : null}

          {loading ? <div className="topic-feedback">Dang tai danh sach tu...</div> : null}
          {error ? <div className="topic-feedback topic-feedback-error">{error}</div> : null}

          {topic ? <TopicWordList words={topic.words} /> : null}
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
