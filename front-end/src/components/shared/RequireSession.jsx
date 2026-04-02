import { Navigate } from 'react-router-dom'
import { getStoredUserId } from '../../utils/session'

export default function RequireSession({ children }) {
  const userId = getStoredUserId()

  if (!userId) {
    return <Navigate to="/" replace />
  }

  return children
}
