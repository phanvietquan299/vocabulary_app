import { useEffect, useMemo, useRef, useState } from 'react'
import {
  getLearnedWords,
  getLearnedWordsWebSocketUrl,
  normalizeLearnedWords,
} from '../data/topicService'
import { LearnedWordsRealtimeContext } from './learnedWordsRealtimeContext'

export function LearnedWordsRealtimeProvider({ sessionId, children }) {
  const [learnedWords, setLearnedWords] = useState([])
  const [loading, setLoading] = useState(Boolean(sessionId))
  const [error, setError] = useState('')
  const [connectionState, setConnectionState] = useState(sessionId ? 'connecting' : 'idle')
  const reconnectTimeoutRef = useRef(null)

  useEffect(() => {
    if (!sessionId) {
      setLearnedWords([])
      setLoading(false)
      setError('')
      setConnectionState('idle')
      return undefined
    }

    let active = true
    let socket = null

    function cleanupReconnect() {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
        reconnectTimeoutRef.current = null
      }
    }

    async function loadInitialWords() {
      setLoading(true)
      setError('')

      try {
        const initialWords = await getLearnedWords(sessionId)

        if (active) {
          setLearnedWords(initialWords)
        }
      } catch (fetchError) {
        if (active) {
          setError(fetchError.message || 'Cannot load learned words.')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    function connectWebSocket() {
      const url = getLearnedWordsWebSocketUrl(sessionId)

      if (!url || !active) {
        return
      }

      cleanupReconnect()
      setConnectionState('connecting')

      socket = new WebSocket(url)

      socket.onopen = () => {
        if (!active) {
          return
        }

        setConnectionState('connected')
      }

      socket.onmessage = (event) => {
        if (!active) {
          return
        }

        try {
          const payload = JSON.parse(event.data)

          if (
            payload?.type === 'initial_learned_words' ||
            payload?.type === 'learned_words_updated'
          ) {
            setLearnedWords(normalizeLearnedWords(payload.learned_words))
            setError('')
          }
        } catch {
          setError('Cannot process realtime learned-word updates.')
        }
      }

      socket.onerror = () => {
        if (!active) {
          return
        }

        setConnectionState('error')
      }

      socket.onclose = () => {
        if (!active) {
          return
        }

        setConnectionState('disconnected')
        reconnectTimeoutRef.current = setTimeout(() => {
          connectWebSocket()
        }, 2500)
      }
    }

    loadInitialWords()
    connectWebSocket()

    return () => {
      active = false
      cleanupReconnect()

      if (socket) {
        socket.close()
      }
    }
  }, [sessionId])

  const value = useMemo(
    () => ({
      learnedWords,
      loading,
      error,
      connectionState,
    }),
    [connectionState, error, learnedWords, loading]
  )

  return (
    <LearnedWordsRealtimeContext.Provider value={value}>
      {children}
    </LearnedWordsRealtimeContext.Provider>
  )
}
