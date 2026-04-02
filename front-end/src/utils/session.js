export const USER_ID_STORAGE_KEY = 'vocabularyAppUserId'

export function getStoredUserId() {
  return localStorage.getItem(USER_ID_STORAGE_KEY)
}
