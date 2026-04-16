import { useEffect, useState } from 'react'
import './HomePage.css'
import HomeHeader from '../components/home/HomeHeader'
import TopicList from '../components/home/TopicList'
import ProgressPanel from '../components/home/ProgressPanel'
import DashboardSidebar from '../components/home/DashboardSidebar'
import RequireSession from '../components/shared/RequireSession'
import { getTopicList, getDashboardData } from '../data/topicService'
import { useLearnedWordsRealtime } from '../context/useLearnedWordsRealtime'
import { getStoredUserId } from '../utils/session'

export default function HomePage() {
  const userId = getStoredUserId()
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { learnedWords } = useLearnedWordsRealtime()

  useEffect(() => {
    let ignore = false

    async function loadDashboard() {
      if (!userId) {
        setLoading(false)
        return
      }

      setLoading(true)
      setError('')

      try {
        const dashboardData = await getDashboardData(userId)

        if (!ignore) {
          setDashboard(dashboardData)
        }
      } catch (fetchError) {
        if (!ignore) {
          setError(fetchError.message || 'Cannot load dashboard data.')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      ignore = true
    }
  }, [userId])

  const baseOverallProgress = dashboard?.overall_progress ?? {
    total: 0,
    learned: 0,
    percentage: 0,
  }

  const topicSummaryMap = new Map(getTopicList().map((topic) => [topic.id, topic]))
  const learnedCountsByTopic = learnedWords.reduce((result, word) => {
    const topicId = String(word.topic)
    result.set(topicId, (result.get(topicId) ?? 0) + 1)
    return result
  }, new Map())

  const overallProgress = {
    ...baseOverallProgress,
    learned: learnedWords.length,
    percentage: baseOverallProgress.total > 0
      ? (learnedWords.length / baseOverallProgress.total) * 100
      : 0,
  }

  const topicRows = Object.entries(dashboard?.topic_progress ?? {}).map(([topicId, progressData]) => {
    const topicMeta = topicSummaryMap.get(topicId)
    const total = progressData.total ?? 0
    const learned = learnedCountsByTopic.get(String(topicId)) ?? 0

    return {
      id: topicId,
      title: topicMeta?.title ?? topicId,
      subtitle: topicMeta?.subtitle ?? 'Topic vocabulary',
      coverImageUrl: topicMeta?.coverImageUrl ?? null,
      total,
      learned,
      progress: total > 0 ? Math.round((learned / total) * 100) : 0,
    }
  })

  const progressStats = [
    {
      label: 'Tổng tiến độ',
      value: Number(overallProgress.percentage || 0),
      displayValue: `${Math.round(Number(overallProgress.percentage || 0))}%`,
      tone: 'ink',
    },
    {
      label: 'Tong tu da hoc',
      value: Number(overallProgress.percentage || 0),
      barValue: overallProgress.total > 0
        ? Math.round((overallProgress.learned / overallProgress.total) * 100)
        : 0,
      displayValue: `${overallProgress.learned} tu`,
      tone: 'gray',
    },
    {
      label: 'Tong so tu',
      value: 100,
      barValue: 100,
      displayValue: `${overallProgress.total} tu`,
      tone: 'paper',
    },
  ]

  return (
    <RequireSession>
      <main className="home-page">
        <div className="container-fluid py-4 py-lg-5">
          <div className="home-shell mx-auto">
            <div className="dashboard-layout">
              <DashboardSidebar />

              <section className="dashboard-main">
                <HomeHeader />

                {loading ? <div className="dashboard-feedback">Dang tai dashboard...</div> : null}
                {error ? <div className="dashboard-feedback dashboard-feedback-error">{error}</div> : null}

                <div id="topics-hub">
                  <TopicList topics={topicRows} />
                </div>
              </section>

              <ProgressPanel items={progressStats} overallProgress={overallProgress} />
            </div>
          </div>
        </div>
      </main>
    </RequireSession>
  )
}
