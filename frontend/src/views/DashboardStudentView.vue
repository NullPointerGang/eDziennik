<script setup lang="ts">
import StudentPanel from '@/components/StudentPanel.vue'
</script>

<template>
 <StudentPanel/>
  <section class="container main">
    <h1 class="text-2xl font-semibold">Dashboard — Student</h1>
    <p class="text-muted">Twoje nadchodzące lekcje i ostatnie oceny.</p>
  </section>
</template>

<style scoped>
.text-muted { color: var(--color-muted); }
</style> 