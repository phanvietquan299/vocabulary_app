const API_URL = import.meta.env.VITE_API_URL

export const DEFAULT_VOCABULARY_IMAGE = '/studying.png'

export function resolveBackendMediaUrl(mediaUrl) {
  if (!mediaUrl) {
    return ''
  }

  if (mediaUrl.startsWith('http://') || mediaUrl.startsWith('https://')) {
    return mediaUrl
  }

  if ((mediaUrl.startsWith('/media/') || mediaUrl.startsWith('/static/')) && API_URL) {
    return `${API_URL}${mediaUrl}`
  }

  return mediaUrl
}

export function resolveVocabularyImageUrl(imageUrl) {
  return resolveBackendMediaUrl(imageUrl) || DEFAULT_VOCABULARY_IMAGE
}

export function speakVocabularyWord(word, pronunciation) {
  if (typeof window === 'undefined' || !window.speechSynthesis || !window.SpeechSynthesisUtterance) {
    return false
  }

  const utterance = new window.SpeechSynthesisUtterance(word)
  utterance.lang = 'en-US'
  utterance.rate = 0.95
  utterance.pitch = 1

  if (pronunciation) {
    utterance.text = word
  }

  window.speechSynthesis.cancel()
  window.speechSynthesis.speak(utterance)
  return true
}

export function playVocabularyAudio(audioUrl, word, pronunciation) {
  const resolvedAudioUrl = resolveBackendMediaUrl(audioUrl)

  if (resolvedAudioUrl) {
    const audio = new Audio(resolvedAudioUrl)
    audio.play().catch(() => {
      speakVocabularyWord(word, pronunciation)
    })
    return true
  }

  return speakVocabularyWord(word, pronunciation)
}