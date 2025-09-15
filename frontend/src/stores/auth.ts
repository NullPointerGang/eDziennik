import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getJSON, setJSON, removeItem } from '@/utils/storage'
import type { Role } from '@/services/authService'
import * as authService from '@/services/authService'

type User = {
  id: string
  name: string
  email: string
  role: Role
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
  const role = computed<Role | null>(() => user.value?.role ?? null)

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

  async function login(email: string, password: string) {
    const session = await authService.login({ email, password })
    setSession(session)
  }

  async function register(name: string, email: string, password: string, role: Role) {
    const session = await authService.register({ name, email, password, role })
    setSession(session)
  }

  async function logout() {
    await authService.logout()
    clearSession()
  }

  return {
    token,
    user,
    role,
    isAuthenticated,
    setSession,
    clearSession,
    login,
    register,
    logout,
  }
}) 