import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getJSON, setJSON, removeItem } from '@/utils/storage'
import type { Role } from '@/services/authService'
import * as authService from '@/services/authService'

type User = {
  id: string
  first_name: string
  last_name: string
  email: string
  role: Role
}

type Session = {
  token: string
  user: User
  userId: string
}

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'
const USER_ID_KEY = 'auth_user_id'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getJSON<string>(TOKEN_KEY))
  const user = ref<User | null>(getJSON<User>(USER_KEY))
  const userId = ref<string | null>(getJSON<string>(USER_ID_KEY))

  const isAuthenticated = computed(() => !!token.value)
  const role = computed<Role | null>(() => user.value?.role ?? null)

  function setSession(session: Session) {
    token.value = session.token
    user.value = session.user
    userId.value = session.userId
    setJSON(TOKEN_KEY, session.token)
    setJSON(USER_KEY, session.user)
    setJSON(USER_ID_KEY, session.userId)
  }

  function clearSession() {
    token.value = null
    user.value = null
    userId.value = null
    removeItem(TOKEN_KEY)
    removeItem(USER_KEY)
    removeItem(USER_ID_KEY)
  }

  async function login(email: string, password: string, rememberMe = false) {
    const session = await authService.login({ email, password }, rememberMe)
    setSession(session)
  }

  async function register(firstName: string, lastName: string, email: string, password: string, role: Role) {
    const session = await authService.register({ first_name: firstName, last_name: lastName, email, password, role })
    setSession(session)
  }

  async function logout() {
    await authService.logout()
    clearSession()
  }

  return {
    token,
    user,
    userId,
    role,
    isAuthenticated,
    setSession,
    clearSession,
    login,
    register,
    logout,
  }
}) 