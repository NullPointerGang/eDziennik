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
        <RouterLink class="button" to="/about">O projekcie</RouterLink>
        <RouterLink v-if="!isAuthed" class="button" to="/auth">LogIn</RouterLink>
        <RouterLink v-else class="button" :to="dashboardTarget">Dashboard</RouterLink>
      </nav>
    </div>
  </header>
  <main class="container main">
    <RouterView />
  </main>
</template>

<style scoped></style>
