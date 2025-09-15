<script setup lang="ts">
import { reactive, ref } from 'vue'

type Mode = 'login' | 'register'
const mode = ref<Mode>('login')

const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ name: '', email: '', password: '', confirm: '' })

function onLoginSubmit() {
  // TODO: replace with real API call
  alert(`Login: ${loginForm.email}`)
}

function onRegisterSubmit() {
  if (registerForm.password !== registerForm.confirm) {
    alert('Пароли не совпадают')
    return
  }
  // TODO: replace with real API call
  alert(`Register: ${registerForm.email}`)
}
</script>

<template>
  <section class="auth">
    <div class="tabs">
      <button
        class="button"
        :class="{ active: mode === 'login' }"
        @click="mode = 'login'"
      >Вход</button>
      <button
        class="button"
        :class="{ active: mode === 'register' }"
        @click="mode = 'register'"
      >Регистрация</button>
    </div>

    <div class="panel">
      <form v-if="mode === 'login'" @submit.prevent="onLoginSubmit" class="form">
        <label>
          <span>Email</span>
          <input type="email" v-model="loginForm.email" required placeholder="you@example.com" />
        </label>
        <label>
          <span>Пароль</span>
          <input type="password" v-model="loginForm.password" required />
        </label>
        <button type="submit" class="button">Войти</button>
      </form>

      <form v-else @submit.prevent="onRegisterSubmit" class="form">
        <label>
          <span>Имя</span>
          <input type="text" v-model="registerForm.name" required />
        </label>
        <label>
          <span>Email</span>
          <input type="email" v-model="registerForm.email" required placeholder="you@example.com" />
        </label>
        <label>
          <span>Пароль</span>
          <input type="password" v-model="registerForm.password" required />
        </label>
        <label>
          <span>Подтверждение пароля</span>
          <input type="password" v-model="registerForm.confirm" required />
        </label>
        <button type="submit" class="button">Зарегистрироваться</button>
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
input {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(148,163,184,.25);
  background: #0b1220;
  color: var(--color-text);
}
</style> 