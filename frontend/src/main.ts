import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { getJSON } from './utils/storage'
import './styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize auth state from localStorage
const auth = useAuthStore()
if (getJSON<string>('auth_token') && !auth.isAuthenticated) {
  // Token exists but user data is missing - redirect to login
  router.push({ name: 'auth' })
}

app.mount('#app')
