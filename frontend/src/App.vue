<script setup lang="ts"></script>

<template>
  <header class="header">
    <div class="container header-inner">
      <strong>eDziennik</strong>
      <nav class="nav">
        <RouterLink class="button" to="/">Главная</RouterLink>
        <RouterLink class="button" to="/about">О проекте</RouterLink>
      </nav>
    </div>
  </header>
  <main class="container main">
    <RouterView />
  </main>
</template>

<style scoped></style>
