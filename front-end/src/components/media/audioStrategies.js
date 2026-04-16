export class BrowserSpeechStrategy {
  speak(word, pronunciation = '') {
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
}

export class DictionaryApiStrategy {
  async resolveAudioUrl(word) {
    if (!word) {
      return ''
    }

    try {
      const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`)

      if (!response.ok) {
        return ''
      }

      const result = await response.json()

      for (const entry of result ?? []) {
        for (const phonetic of entry?.phonetics ?? []) {
          if (phonetic?.audio) {
            return phonetic.audio.startsWith('//') ? `https:${phonetic.audio}` : phonetic.audio
          }
        }
      }
    } catch {
      return ''
    }

    return ''
  }
}