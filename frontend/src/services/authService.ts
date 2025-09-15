import { getJSON, setJSON } from '@/utils/storage'

export type Role = 'student' | 'teacher'

export type RegisterInput = {
  name: string
  email: string
  password: string
  role: Role
}

export type LoginInput = {
  email: string
  password: string
}

export type AuthUser = {
  id: string
  name: string
  email: string
  role: Role
}

export type AuthSession = {
  token: string
  user: AuthUser
}

const USERS_KEY = 'auth_users'

function readUsers(): Record<string, { id: string; name: string; email: string; role: Role; password: string }> {
  return getJSON(USERS_KEY) ?? {}
}

function writeUsers(users: Record<string, { id: string; name: string; email: string; role: Role; password: string }>): void {
  setJSON(USERS_KEY, users)
}

function uid(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36)
}

export async function register(input: RegisterInput): Promise<AuthSession> {
  // In future: replace with POST /api/auth/register
  const users = readUsers()
  if (users[input.email]) {
    throw new Error('User already exists')
  }
  const id = uid()
  users[input.email] = {
    id,
    name: input.name,
    email: input.email,
    role: input.role,
    password: input.password,
  }
  writeUsers(users)

  const session: AuthSession = {
    token: 'demo-' + uid(),
    user: { id, name: input.name, email: input.email, role: input.role },
  }
  return new Promise((resolve) => setTimeout(() => resolve(session), 300))
}

export async function login(input: LoginInput): Promise<AuthSession> {
  // In future: replace with POST /api/auth/login
  const users = readUsers()
  const existing = users[input.email]
  if (!existing || existing.password !== input.password) {
    throw new Error('Invalid credentials')
  }
  const session: AuthSession = {
    token: 'demo-' + uid(),
    user: { id: existing.id, name: existing.name, email: existing.email, role: existing.role },
  }
  return new Promise((resolve) => setTimeout(() => resolve(session), 250))
}

export async function logout(): Promise<void> {
  // In future: replace with POST /api/auth/logout or token revoke
  return new Promise((resolve) => setTimeout(() => resolve(), 100))
} 