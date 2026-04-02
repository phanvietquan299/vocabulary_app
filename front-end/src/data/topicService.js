import { TOPIC_LIBRARY } from './mockTopics'

const API_URL = import.meta.env.VITE_API_URL

function getTopicMeta(topicId) {
  const topic = TOPIC_LIBRARY[topicId]

  if (!topic) {
    return null
  }

  return {
    id: topic.id,
    title: topic.title,
    subtitle: topic.subtitle,
  }
}

export function getTopicList() {
  return Object.values(TOPIC_LIBRARY).map((topic) => {
    const total = topic.words.length
    const learned = topic.words.filter((word) => word.learned).length

    return {
      id: topic.id,
      title: topic.title,
      subtitle: topic.subtitle,
      total,
      learned,
      progress: total > 0 ? Math.round((learned / total) * 100) : 0,
    }
  })
}

export async function getDashboardData(sessionId) {
  const response = await fetch(
    `${API_URL}/dashboard/user?session_id=${encodeURIComponent(sessionId)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch dashboard data.')
  }

  const result = await response.json()
  return result.dashboard_data
}

export async function getTopicById(topicId) {
  const topicMeta = getTopicMeta(topicId)

  if (!topicMeta) {
    return null
  }

  const response = await fetch(
    `${API_URL}/vocabulary?topic=${encodeURIComponent(topicId)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch topic vocabulary.')
  }

  const result = await response.json()
  const words = (result.vocabulary ?? []).map((word) => ({
    id: word.id,
    word: word.word,
    meaning: word.meaning,
    example: word.example ?? `Vi du cho tu "${word.word}" se duoc them sau.`,
    learned: Boolean(word.learn_at),
    topic: word.topic,
  }))

  return {
    ...topicMeta,
    words,
  }
}

export async function getFlashcardExam(wordId) {
  const response = await fetch(
    `${API_URL}/exam/exam-object-flashcard?word_id=${encodeURIComponent(wordId)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch flashcard exam.')
  }

  const result = await response.json()
  return result.exam_object
}

export async function getMultipleChoiceExam(wordId) {
  const response = await fetch(
    `${API_URL}/exam/exam-object-multiple-choices?word_id=${encodeURIComponent(wordId)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch multiple choice exam.')
  }

  const result = await response.json()
  return result.exam_object
}

export async function markWordAsLearned(sessionId, wordId) {
  const response = await fetch(
    `${API_URL}/learned/add?session_id=${encodeURIComponent(sessionId)}&word_id=${encodeURIComponent(wordId)}`,
    {
      method: 'POST',
    }
  )

  if (!response.ok) {
    throw new Error('Failed to mark word as learned.')
  }

  return response.text()
}

export async function removeWordAsLearned(sessionId, wordId) {
  const response = await fetch(
    `${API_URL}/learned/remove?session_id=${encodeURIComponent(sessionId)}&word_id=${encodeURIComponent(wordId)}`,
    {
      method: 'DELETE',
    }
  )

  if (!response.ok) {
    throw new Error('Failed to remove learned word.')
  }

  return response.json()
}

export async function getLearnedWords(sessionId) {
  const response = await fetch(
    `${API_URL}/learned/words?session_id=${encodeURIComponent(sessionId)}`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch learned words.')
  }

  const result = await response.json()
  return result.learned_words ?? []
}
