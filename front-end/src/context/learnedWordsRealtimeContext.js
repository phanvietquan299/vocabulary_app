import { createContext } from 'react'

export const LearnedWordsRealtimeContext = createContext({
  learnedWords: [],
  loading: true,
  error: '',
  connectionState: 'idle',
  dashboardRefreshTick: 0,
})
