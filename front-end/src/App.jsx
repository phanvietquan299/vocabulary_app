import { useState } from 'react'
import './App.css'
import { Routes, Route } from "react-router-dom";
import { useNavigate } from "react-router-dom";

import FirstPage from './pages/FirstPage'
import HomePage from './pages/HomePage'
import ReviewSessionPage from './pages/ReviewSessionPage'
import TopicWordsPage from './pages/TopicWordsPage'
import TopicStudyPage from './pages/TopicStudyPage'

import { USER_ID_STORAGE_KEY } from './utils/session'

function createUserId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }

  return `user-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

function getUserId() {
  const savedUserId = localStorage.getItem(USER_ID_STORAGE_KEY)

  if (savedUserId) {
    return savedUserId
  }

  return null;
}

function resetUserId() {
  const newUserId = createUserId()
  localStorage.setItem(USER_ID_STORAGE_KEY, newUserId)
  return newUserId
}

function App() {
  const [userId, setUserId] = useState(() => getUserId() ?? '')
  const navigate = useNavigate()

  function handleReset() {
    const newUserId = resetUserId()
    setUserId(newUserId)
  }

  function handleContinue() {
    navigate('/home', {
      state: { userId : userId }
    })
  }

  function handleNew() {
    
    const newUserId = resetUserId()
    setUserId(newUserId)
    navigate('/home', {
      state: { userId: newUserId }
    })
  }

  return (
    // <FirstPage
    //   userId={userId}
    //   onContinue={handleContinue}
    //   onReset={handleReset}
    // />

    <Routes>
      <Route path="/" element={<FirstPage 
              userId={userId} 
              onContinue={handleContinue} 
              onReset={handleReset} 
              onNew={handleNew}/>} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/review" element={<ReviewSessionPage />} />
      <Route path="/topics/:topicId" element={<TopicWordsPage />} />
      <Route path="/topics/:topicId/study" element={<TopicStudyPage />} />
    </Routes>
  )
}

export default App
