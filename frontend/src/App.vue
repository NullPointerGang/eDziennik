<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isAuthed = computed(() => auth.isAuthenticated)
const dashboardTarget = computed(() => (auth.role === 'student' ? { name: 'dashboard-student-home' } : { name: 'dashboard' }))
</script>

<template>
  <header class="header">
    <div class="container header-inner">
      <strong>ePińczów</strong>
      <nav class="nav">
        <RouterLink class="button" to="/">Główna</RouterLink>
        <RouterLink v-if="!isAuthed" class="button" to="/auth">LogIn</RouterLink>
        <RouterLink v-else class="button" :to="dashboardTarget">Dashboard</RouterLink>
      </nav>
    </div>
  </header>
  <main class="container main">
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>
</template>

<style scoped>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
