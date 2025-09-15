<script setup lang="ts"></script>

<template>
  <header class="header">
    <div class="container header-inner">
      <strong>ePińczów</strong>
      <nav class="nav">
        <RouterLink class="button" to="/">Główna</RouterLink>
        <RouterLink class="button" to="/about">O projekcie</RouterLink>
        <RouterLink class="button" to="/auth">LogIn</RouterLink>
      </nav>
    </div>
  </header>
  <main class="container main">
    <RouterView />
  </main>
</template>

<style scoped></style>
