<script setup lang="ts"></script>

<template>
  <section class="container main">
    <h1 class="text-2xl font-semibold">404</h1>
    <p class="text-muted">Strona nie znaleziona.</p>
    <RouterLink class="button" to="/">Wróć na główną</RouterLink>
  </section>
</template>

<style scoped>
.text-muted { color: var(--color-muted); }
</style> 