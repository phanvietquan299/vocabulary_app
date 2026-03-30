import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Waiting for WebSocket messages...')

  useEffect(() => {
    const socket = new WebSocket(`ws://${window.location.hostname}:8000/ws`)

    socket.onmessage = (event) => {
      setMessage(event.data)
    }

    socket.onerror = () => {
      setMessage('Error connecting to WebSocket.')
    }

    socket.onclose = () => {
      setMessage('WebSocket connection closed.')
    }

    return () => {
      socket.close()
    }
  }, [])

  return (
    <main>
      <h1>WebSocket Viewer</h1>
      <p>{message}</p>
    </main>
  )
}

export default App
