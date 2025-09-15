import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getJSON, setJSON, removeItem } from '@/utils/storage'

type User = {
  id: string
  name: string
  email: string
}

type Session = {
  token: string
  user: User
}

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getJSON<string>(TOKEN_KEY))
  const user = ref<User | null>(getJSON<User>(USER_KEY))

  const isAuthenticated = computed(() => !!token.value)

  function setSession(session: Session) {
    token.value = session.token
    user.value = session.user
    setJSON(TOKEN_KEY, session.token)
    setJSON(USER_KEY, session.user)
  }

  function clearSession() {
    token.value = null
    user.value = null
    removeItem(TOKEN_KEY)
    removeItem(USER_KEY)
  }

  return {
    token,
    user,
    isAuthenticated,
    setSession,
    clearSession,
  }
}) 