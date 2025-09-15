<script setup lang="ts">
import { House, Calendar1, Plus } from 'lucide-vue-next'
</script>

<template>
  <aside class="menu">
    <RouterLink class="button" to="/dashboard/teacher"><House /></RouterLink>
    <RouterLink class="button" to="/dashboard/teacher/calendar"><Calendar1 /></RouterLink>
    <RouterLink class="button" to="/dashboard/teacher/grades"><Plus /></RouterLink>
  </aside>
</template>

<style scoped lang="scss">
.menu {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
  width: fit-content;
  height: auto;
  min-height: 300px;
  .button {
    color: white;
    text-decoration: none;
    background: none;
    border: none;
    padding: 15px;
    border-radius: 12px;
    transition: background 0.2s ease;
    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }
  }
}
</style>