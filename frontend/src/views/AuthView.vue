<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

type Mode = 'login' | 'register'
const mode = ref<Mode>('login')

const loginForm = reactive({ email: '', password: '', rememberMe: false })
const registerForm = reactive({ firstName: '', lastName: '', email: '', password: '', confirm: '' })

// role selection for both flows
const role = ref<'student' | 'teacher'>('student')

const auth = useAuthStore()
const router = useRouter()

const error = ref('')

async function onLoginSubmit() {
  error.value = ''
  try {
    await auth.login(loginForm.email, loginForm.password, loginForm.rememberMe)
    if (auth.role === 'student') {
      router.push({ name: 'dashboard-student-home' })
    } else if (auth.role === 'teacher') {
      router.push({ name: 'dashboard-teacher' })
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (e: any) {
    error.value = e?.message || 'Login error'
  }
}

async function onRegisterSubmit() {
  error.value = ''
  if (registerForm.password !== registerForm.confirm) {
    error.value = 'Hasła nie są takie same'
    return
  }
  try {
    await auth.register(registerForm.firstName, registerForm.lastName, registerForm.email, registerForm.password, role.value)
    if (auth.role === 'student') {
      router.push({ name: 'dashboard-student-home' })
    } else if (auth.role === 'teacher') {
      router.push({ name: 'dashboard-teacher' })
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (e: any) {
    error.value = e?.message || 'Register error'
  }
}
</script>

<template>
  <section class="auth">
    <div class="tabs">
      <button
        class="button"
        :class="{ active: mode === 'login' }"
        @click="mode = 'login'"
      >LogIn</button>
      <button
        class="button"
        :class="{ active: mode === 'register' }"
        @click="mode = 'register'"
      >Rejestracja</button>
    </div>

    <div class="panel">
      <form v-if="mode === 'login'" @submit.prevent="onLoginSubmit" class="form">
        <div v-if="error" class="error">{{ error }}</div>
        <label>
          <span>Email</span>
          <input type="email" v-model="loginForm.email" required placeholder="you@example.com" />
        </label>
        <label>
          <span>Hasło</span>
          <input type="password" v-model="loginForm.password" required />
        </label>
        <label class="checkbox">
          <input type="checkbox" v-model="loginForm.rememberMe" />
          <span>Zapamiętaj mnie</span>
        </label>
        <button type="submit" class="button">LogIn</button>
      </form>

      <form v-else @submit.prevent="onRegisterSubmit" class="form">
        <div v-if="error" class="error">{{ error }}</div>
        <label>
          <span>Imię</span>
          <input type="text" v-model="registerForm.firstName" required />
        </label>
        <label>
          <span>Nazwisko</span>
          <input type="text" v-model="registerForm.lastName" required />
        </label>
        <label>
          <span>Email</span>
          <input type="email" v-model="registerForm.email" required placeholder="you@example.com" />
        </label>
        <label>
          <span>Hasło</span>
          <input type="password" v-model="registerForm.password" required />
        </label>
        <label>
          <span>Potwierdzenie hasła</span>
          <input type="password" v-model="registerForm.confirm" required />
        </label>
        <label>
          <span>Rola</span>
          <select v-model="role" required>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </label>
        <button type="submit" class="button">Rejestracja</button>
      </form>
    </div>
  </section>
</template>

<style scoped>
.auth { max-width: 480px; margin: 24px auto; }
.tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.tabs .active { outline: 2px solid var(--color-accent); }
.panel { background: var(--color-panel); border: 1px solid rgba(148,163,184,.2); border-radius: 12px; padding: 16px; }
.form { display: grid; gap: 12px; }
label { display: grid; gap: 6px; }
.checkbox { display: flex; align-items: center; gap: 8px; }
.checkbox input { width: auto; }
.error { color: #ef4444; background: rgba(239, 68, 68, 0.1); padding: 8px 12px; border-radius: 6px; font-size: 14px; }
input, select {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(148,163,184,.25);
  background: #0b1220;
  color: var(--color-text);
}
</style> 