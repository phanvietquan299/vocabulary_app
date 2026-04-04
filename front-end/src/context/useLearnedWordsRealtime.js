import { useContext } from 'react'
import { LearnedWordsRealtimeContext } from './learnedWordsRealtimeContext'

export function useLearnedWordsRealtime() {
  return useContext(LearnedWordsRealtimeContext)
}
