import { TOPIC_LIBRARY } from './mockTopics'

const API_URL = import.meta.env.VITE_API_URL

const TOPIC_COVER_IMAGES = {
  animal: 'https://images.pexels.com/photos/18554901/pexels-photo-18554901.jpeg',
  travel: 'https://images.pexels.com/photos/7009831/pexels-photo-7009831.jpeg',
  family: 'https://images.pexels.com/photos/35929436/pexels-photo-35929436.jpeg',
  school: 'https://images.pexels.com/photos/8926405/pexels-photo-8926405.jpeg',
  work: 'https://images.pexels.com/photos/5686020/pexels-photo-5686020.jpeg',
  music: 'https://images.pexels.com/photos/15487609/pexels-photo-15487609.jpeg',
}

function mapLearnedWord(word) {
  return {
    id: word.id,
    word: word.word,
    meaning: word.meaning,
    example: word.example ?? `Vi du cho tu "${word.word}" se duoc them sau.`,
    topic: word.topic,
    learnAt: word.learn_at ?? word.learnAt ?? null,
    learned: Boolean(word.learn_at ?? word.learnAt),
    localUrl: word.local_url ?? word.localUrl ?? null,
    remoteUrl: word.remote_url ?? word.remoteUrl ?? null,
    imageUrl: word.local_url ?? word.image_url ?? word.remote_url ?? word.imageUrl ?? word.remoteUrl ?? null,
    audioUrl: word.audio_url ?? word.audioUrl ?? null,
    pronunciation: word.pronunciation ?? null,
  }
}

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
      coverImageUrl: TOPIC_COVER_IMAGES[topic.id] ?? TOPIC_COVER_IMAGES.school,
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
    learnAt: word.learn_at ?? null,
    topic: word.topic,
    localUrl: word.local_url ?? null,
    remoteUrl: word.remote_url ?? null,
    imageUrl: word.local_url ?? word.image_url ?? word.remote_url ?? null,
    audioUrl: word.audio_url ?? null,
    pronunciation: word.pronunciation ?? null,
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
  return (result.learned_words ?? []).map(mapLearnedWord)
}

export function normalizeLearnedWords(words) {
  return (words ?? []).map(mapLearnedWord)
}

export async function generateVocabularyMedia(wordId, sessionId = '') {
  const requestUrl = new URL(`${API_URL}/images/${encodeURIComponent(wordId)}`)

  if (sessionId) {
    requestUrl.searchParams.set('session_id', sessionId)
  }

  const response = await fetch(requestUrl.toString())

  if (!response.ok) {
    throw new Error('Failed to generate vocabulary media.')
  }

  return response.json()
}

export function getLearnedWordsWebSocketUrl(sessionId) {
  if (!API_URL || !sessionId) {
    return ''
  }

  const url = new URL(API_URL)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  url.pathname = '/ws'
  url.search = `session_id=${encodeURIComponent(sessionId)}`
  return url.toString()
}
