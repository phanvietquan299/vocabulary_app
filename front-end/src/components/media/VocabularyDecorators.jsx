import { useEffect, useMemo, useState } from 'react'
import {
  DEFAULT_VOCABULARY_IMAGE,
  resolveBackendMediaUrl,
  resolveVocabularyImageUrl,
} from '../../utils/vocabularyMedia'
import { BrowserSpeechStrategy, DictionaryApiStrategy } from './audioStrategies'

export function MangaImageDecorator({ imageUrl, children, wordLabel }) {
  const resolvedImageUrl = resolveVocabularyImageUrl(imageUrl)

  return (
    <section className="vocab-decorator vocab-image-decorator">
      <div className="vocab-media-frame">
        <img className="vocab-media-image" src={resolvedImageUrl || DEFAULT_VOCABULARY_IMAGE} alt={wordLabel} />
      </div>
      {children}
    </section>
  )
}

export function AudioIconDecorator({ audioUrl, onPlayAudio, children, loading }) {
  const resolvedAudioUrl = resolveBackendMediaUrl(audioUrl)

  return (
    <div className="vocab-audio-decorator">
      <div className="vocab-audio-actions">
        {resolvedAudioUrl ? null : <span className="vocab-audio-loading">{loading ? 'Dang tai audio...' : 'Audio se duoc ho tro bang browser speech'}</span>}
      </div>
      {resolvedAudioUrl ? <audio className="vocab-audio-player" controls src={resolvedAudioUrl} /> : null}
      {children}
    </div>
  )
}

export function VocabularyMediaDecorator({
  word,
  imageUrl,
  audioUrl,
  pronunciation,
  compact = false,
  children,
}) {
  const [currentImageUrl, setCurrentImageUrl] = useState(imageUrl)
  const [currentAudioUrl, setCurrentAudioUrl] = useState(audioUrl)
  const [audioLoading, setAudioLoading] = useState(false)
  const browserSpeech = useMemo(() => new BrowserSpeechStrategy(), [])
  const dictionaryStrategy = useMemo(() => new DictionaryApiStrategy(), [])

  useEffect(() => {
    setCurrentImageUrl(imageUrl)
    setCurrentAudioUrl(audioUrl)
  }, [audioUrl, imageUrl])

  useEffect(() => {
    let active = true

    async function loadDictionaryAudio() {
      if (currentAudioUrl || !word?.word) {
        return
      }

      setAudioLoading(true)

      try {
        const resolvedAudioUrl = await dictionaryStrategy.resolveAudioUrl(word.word)

        if (active && resolvedAudioUrl) {
          setCurrentAudioUrl(resolvedAudioUrl)
        }
      } finally {
        if (active) {
          setAudioLoading(false)
        }
      }
    }

    loadDictionaryAudio()

    return () => {
      active = false
    }
  }, [currentAudioUrl, dictionaryStrategy, pronunciation, word?.word])

  function handlePlayAudio() {
    const resolvedAudioUrl = resolveBackendMediaUrl(currentAudioUrl)

    if (resolvedAudioUrl) {
      const audio = new Audio(resolvedAudioUrl)
      audio.play().catch(() => {
        browserSpeech.speak(word.word, pronunciation)
      })
      return
    }

    browserSpeech.speak(word.word, pronunciation)
  }

  return (
    <div className={`vocab-decorator${compact ? ' vocab-decorator-compact' : ''}`}>
      <MangaImageDecorator
        imageUrl={currentImageUrl}
        wordLabel={word.word}
      >
        <AudioIconDecorator
          audioUrl={currentAudioUrl}
          onPlayAudio={handlePlayAudio}
          loading={audioLoading}
        >
          {children}
        </AudioIconDecorator>
      </MangaImageDecorator>
    </div>
  )
}