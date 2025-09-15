<script setup lang="ts">
import { Calendar1, House, BookPlus, Mail } from 'lucide-vue-next'

</script>

<template>
  <aside class="menu">
    <RouterLink class="button" to="/dashboard/home"><House /></RouterLink>
    <RouterLink class="button" to="/dashboard/calendar"><Calendar1 /></RouterLink>
    <RouterLink class="button" to="/dashboard/grades"><BookPlus /></RouterLink>
    <RouterLink class="button" to="/dashboard/messages"><Mail /></RouterLink>
  </aside>
  <RouterView />
</template>

<style scoped lang="scss">
.menu {
  display: flex;
  flex-direction: column;
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
  width: fit-content;
  .button {
    color: white;
    text-decoration: none;
    background: none;
    border: none;
    &:not(:first-child) {
      margin-top: 10px;
    }
  }
}
</style>