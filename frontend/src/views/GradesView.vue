<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getGrades, type Grade } from '@/services/gradesService'
import { httpClient } from '@/utils/http'
import StudentPanel from '@/components/StudentPanel.vue'
import ChatComponent from '@/components/ChatComponent.vue'

const auth = useAuthStore()
const grades = ref<Grade[]>([])
const teachers = ref<Record<number, { first_name: string; last_name: string }>>({})
const loading = ref(true)
const hoveredGrade = ref<Grade | null>(null)
const tooltipPosition = ref({ x: 0, y: 0 })

const gradesBySubject = computed(() => {
  const grouped = grades.value.reduce((acc, grade) => {
    if (!acc[grade.subject]) {
      acc[grade.subject] = []
    }
    acc[grade.subject].push(grade)
    return acc
  }, {} as Record<string, Grade[]>)
  
  return Object.keys(grouped)
    .sort()
    .map(subject => ({
      subject,
      grades: grouped[subject].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    }))
})

function showTooltip(grade: Grade, event: MouseEvent) {
  hoveredGrade.value = grade
  tooltipPosition.value = { x: event.clientX + 10, y: event.clientY + 10 }
}

function hideTooltip() {
  hoveredGrade.value = null
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('pl-PL')
}

async function loadTeachers() {
  try {
    const users = await httpClient.get<Array<{ id: number; first_name: string; last_name: string; roles: string[] }>>('/users/')
    const teacherUsers = users.filter(user => user.roles.includes('teacher'))
    teachers.value = teacherUsers.reduce((acc, teacher) => {
      acc[teacher.id] = { first_name: teacher.first_name, last_name: teacher.last_name }
      return acc
    }, {} as Record<number, { first_name: string; last_name: string }>)
  } catch (error) {
    console.error('Failed to load teachers:', error)
  }
}

function getTeacherName(teacherId: number) {
  const teacher = teachers.value[teacherId]
  return teacher ? `${teacher.first_name} ${teacher.last_name}` : 'Nieznany nauczyciel'
}

onMounted(async () => {
  try {
    if (auth.userId) {
      await Promise.all([
        getGrades(parseInt(auth.userId)).then(data => grades.value = data),
        loadTeachers()
      ])
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <div class="dashboard">
      <StudentPanel/>
      <div class="grades-container">
        <h1>Oceny</h1>
    
    <div v-if="loading" class="loading">Ładowanie...</div>
    
    <div v-else-if="gradesBySubject.length === 0" class="no-grades">
      Brak ocen
    </div>
    
    <div v-else class="subjects">
      <div v-for="{ subject, grades: subjectGrades } in gradesBySubject" :key="subject" class="subject-block">
        <h2>{{ subject }}</h2>
        <div class="grades-list">
          <div 
            v-for="grade in subjectGrades" 
            :key="grade.id" 
            class="grade-item"
            @mouseenter="showTooltip(grade, $event)"
            @mouseleave="hideTooltip"
          >
            {{ grade.value }}
          </div>
        </div>
      </div>
    </div>
    
        <div 
          v-if="hoveredGrade" 
          class="tooltip"
          :style="{ left: tooltipPosition.x + 'px', top: tooltipPosition.y + 'px' }"
        >
          <div><strong>Data:</strong> {{ formatDate(hoveredGrade.date) }}</div>
          <div><strong>Nauczyciel:</strong> {{ getTeacherName(hoveredGrade.teacher_id) }}</div>
          <div v-if="hoveredGrade.comment"><strong>Komentarz:</strong> {{ hoveredGrade.comment }}</div>
        </div>
        <ChatComponent />
      </div>
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

.grades-container {
  flex: 1;
  color: white;
}

.grades-container h1 {
  margin-bottom: 20px;
  font-size: 24px;
}

.loading, .no-grades {
  text-align: center;
  color: #94a3b8;
  padding: 40px;
}

.subjects {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.subject-block {
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
}

.subject-block h2 {
  margin: 0 0 15px 0;
  font-size: 18px;
  color: white;
}

.grades-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.grade-item {
  background: #3b82f6;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-weight: 600;
}

.grade-item:hover {
  background: #2563eb;
}

.tooltip {
  position: fixed;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  z-index: 1000;
  pointer-events: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.tooltip div {
  margin-bottom: 4px;
}

.tooltip div:last-child {
  margin-bottom: 0;
}
</style>
