<script setup lang="ts">
import TeacherPanel from '@/components/TeacherPanel.vue'
import ChatComponent from '@/components/ChatComponent.vue'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const auth = useAuthStore()

const currentMonth = computed(() => {
  return new Date().toLocaleDateString('pl-PL', { month: 'long', year: 'numeric' })
})

const today = new Date().getDate()
const days = Array.from({ length: 31 }, (_, i) => i + 1)
</script>

<template>
  <div>
    <div class="dashboard">
      <TeacherPanel/>
      <div class="content">
        <div class="user-info">
          <h1>{{ auth.user?.first_name }} {{ auth.user?.last_name }}</h1>
          <span class="role">{{ auth.role }}</span>
        </div>
        <div class="calendar">
          <h3>Календarz</h3>
          <div class="mini-calendar">
            <div class="month">{{ currentMonth }}</div>
            <div class="days">
              <div v-for="day in days" :key="day" class="day" :class="{ today: day === today }">{{ day }}</div>
            </div>
          </div>
        </div>
      </div>
      <ChatComponent />
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  gap: 20px;
  padding: 20px;
  height: 50vh;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-info {
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
}

.user-info h1 {
  margin: 0;
  font-size: 24px;
  color: white;
}

.role {
  color: #94a3b8;
  text-transform: capitalize;
}

.calendar {
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
}

.calendar h3 {
  margin: 0 0 15px 0;
  color: white;
}

.month {
  text-align: center;
  margin-bottom: 10px;
  color: white;
  font-weight: 600;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.day {
  padding: 8px;
  text-align: center;
  color: #94a3b8;
  border-radius: 8px;
  cursor: pointer;
}

.day:hover {
  background: rgba(255, 255, 255, 0.1);
}

.day.today {
  background: #3b82f6;
  color: white;
}
</style> 