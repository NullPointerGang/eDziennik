import { httpClient } from '@/utils/http'

export type Role = 'student' | 'teacher'

export type RegisterInput = {
  first_name: string
  last_name: string
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
  first_name: string
  last_name: string
  email: string
  role: Role
}

export type AuthSession = {
  token: string
  user: AuthUser
  roles: string[]
  userId: string
}

function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function validatePassword(password: string): boolean {
  return password.length >= 6
}

function validateName(name: string): boolean {
  return name.trim().length >= 2
}

export async function register(input: RegisterInput): Promise<AuthSession> {
  if (!validateEmail(input.email)) {
    throw new Error('Invalid email format')
  }
  if (!validatePassword(input.password)) {
    throw new Error('Password must be at least 6 characters')
  }
  if (!validateName(input.first_name)) {
    throw new Error('First name must be at least 2 characters')
  }
  if (!validateName(input.last_name)) {
    throw new Error('Last name must be at least 2 characters')
  }

  const data = await httpClient.post<any>('/auth/register', input)
  
  return {
    token: data.access_token,
    user: {
      id: data.user.id.toString(),
      first_name: data.user.first_name,
      last_name: data.user.last_name,
      email: data.user.email,
      role: data.user.roles?.[0] as Role || 'student',
    },
    roles: data.roles || [],
    userId: data.user.id.toString()
  }
}

export async function login(input: LoginInput, rememberMe = false): Promise<AuthSession> {
  if (!validateEmail(input.email)) {
    throw new Error('Invalid email format')
  }
  if (!validatePassword(input.password)) {
    throw new Error('Password must be at least 6 characters')
  }

  const data = await httpClient.post<any>(`/auth/login?remember_me=${rememberMe}`, input)
  
  return {
    token: data.access_token,
    user: {
      id: data.user.id.toString(),
      first_name: data.user.first_name,
      last_name: data.user.last_name,
      email: data.user.email,
      role: data.user.roles?.[0] as Role || 'student',
    },
    roles: data.roles || [],
    userId: data.user.id.toString()
  }
}

export async function logout(): Promise<void> {
  await httpClient.post('/auth/logout')
}

export async function getUserData(userId: string): Promise<AuthUser> {
  const data = await httpClient.get<any>(`/users/${userId}`)
  return {
    id: data.id.toString(),
    first_name: data.first_name,
    last_name: data.last_name,
    email: data.email,
    role: data.roles?.[0] as Role || 'student',
  }
} 