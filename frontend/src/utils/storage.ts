const NAMESPACE = 'edziennik:'

function getStorage(): Storage | null {
  try {
    if (typeof window === 'undefined') return null
    return window.localStorage
  } catch {
    return null
  }
}

function withKey(key: string): string {
  return `${NAMESPACE}${key}`
}

export function setItem(key: string, value: string): void {
  const storage = getStorage()
  if (!storage) return
  storage.setItem(withKey(key), value)
}

export function getItem(key: string): string | null {
  const storage = getStorage()
  if (!storage) return null
  return storage.getItem(withKey(key))
}

export function removeItem(key: string): void {
  const storage = getStorage()
  if (!storage) return
  storage.removeItem(withKey(key))
}

export function clearNamespace(): void {
  const storage = getStorage()
  if (!storage) return
  const keys: string[] = []
  for (let i = 0; i < storage.length; i++) {
    const k = storage.key(i)
    if (k && k.startsWith(NAMESPACE)) keys.push(k)
  }
  keys.forEach((k) => storage.removeItem(k))
}

export function setJSON<T>(key: string, value: T): void {
  setItem(key, JSON.stringify(value))
}

export function getJSON<T>(key: string): T | null {
  const raw = getItem(key)
  if (!raw) return null
  try {
    return JSON.parse(raw) as T
  } catch {
    return null
  }
}

// Optional: small helper to bind a ref to localStorage
import { ref, watch, type Ref } from 'vue'

export function useLocalStorageRef<T>(key: string, initial: T): Ref<T> {
  const stored = getJSON<T>(key)
  const state = ref<T>(stored ?? initial) as Ref<T>

  watch(
    state,
    (val) => {
      try {
        setJSON<T>(key, val)
      } catch {
        // ignore write errors
      }
    },
    { deep: true }
  )

  return state
} 