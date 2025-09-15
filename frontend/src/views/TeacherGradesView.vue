<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { httpClient } from '@/utils/http'
import { getGrades, type Grade } from '@/services/gradesService'
import TeacherPanel from '@/components/TeacherPanel.vue'

const auth = useAuthStore()
const students = ref<Array<{ id: number; first_name: string; last_name: string }>>([])
const teacherGrades = ref<Grade[]>([])
const loading = ref(false)

const form = ref({
  student_id: '',
  subject: '',
  value: '',
  comment: ''
})

const gradesBySubject = computed(() => {
  const grouped = teacherGrades.value.reduce((acc, grade) => {
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

async function loadStudents() {
  try {
    const data = await httpClient.get<Array<{ id: number; first_name: string; last_name: string; roles: string[] }>>('/users/')
    students.value = data.filter(user => user.roles.includes('student'))
  } catch (error) {
    console.error('Failed to load students:', error)
  }
}

async function loadTeacherGrades() {
  try {
    const allGrades = await httpClient.get<Grade[]>('/grades/')
    teacherGrades.value = allGrades.filter(grade => grade.teacher_id.toString() === auth.userId)
  } catch (error) {
    console.error('Failed to load teacher grades:', error)
  }
}

async function submitGrade() {
  if (!form.value.student_id || !form.value.subject || !form.value.value) {
    alert('Wypełnij wszystkie wymagane pola')
    return
  }

  loading.value = true
  try {
    await httpClient.post('/grades/', {
      student_id: parseInt(form.value.student_id),
      teacher_id: parseInt(auth.userId!),
      subject: form.value.subject,
      value: parseInt(form.value.value),
      date: new Date().toISOString().split('T')[0],
      comment: form.value.comment || null
    })
    
    form.value = { student_id: '', subject: '', value: '', comment: '' }
    await loadTeacherGrades()
    alert('Ocena została dodana')
  } catch (error) {
    console.error('Failed to create grade:', error)
    alert('Błąd podczas dodawania oceny')
  } finally {
    loading.value = false
  }
}

function getStudentName(studentId: number) {
  const student = students.value.find(s => s.id === studentId)
  return student ? `${student.first_name} ${student.last_name}` : 'Nieznany uczeń'
}

onMounted(async () => {
  await Promise.all([loadStudents(), loadTeacherGrades()])
})
</script>

<template>
  <div>
    <div class="dashboard">
      <TeacherPanel/>
      <div class="teacher-grades">
        <h1>Dodawanie ocen</h1>
    
    <div class="form-section">
      <h2>Nowa ocena</h2>
      <form @submit.prevent="submitGrade" class="grade-form">
        <label>
          <span>Uczeń *</span>
          <select v-model="form.student_id" required>
            <option value="">Wybierz ucznia</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }}
            </option>
          </select>
        </label>
        
        <label>
          <span>Przedmiot *</span>
          <input type="text" v-model="form.subject" required placeholder="np. Matematyka" />
        </label>
        
        <label>
          <span>Ocena *</span>
          <select v-model="form.value" required>
            <option value="">Wybierz ocenę</option>
            <option v-for="grade in [1, 2, 3, 4, 5, 6]" :key="grade" :value="grade">{{ grade }}</option>
          </select>
        </label>
        
        <label>
          <span>Komentarz</span>
          <textarea v-model="form.comment" placeholder="Opcjonalny komentarz"></textarea>
        </label>
        
        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Dodawanie...' : 'Dodaj ocenę' }}
        </button>
      </form>
    </div>
    
    <div class="grades-section">
      <h2>Moje oceny</h2>
      <div v-if="gradesBySubject.length === 0" class="no-grades">
        Brak wystawionych ocen
      </div>
      <div v-else class="subjects">
        <div v-for="{ subject, grades } in gradesBySubject" :key="subject" class="subject-block">
          <h3>{{ subject }}</h3>
          <div class="grades-list">
            <div v-for="grade in grades" :key="grade.id" class="grade-entry">
              <span class="grade-value">{{ grade.value }}</span>
              <span class="student-name">{{ getStudentName(grade.student_id) }}</span>
              <span class="grade-date">{{ new Date(grade.date).toLocaleDateString('pl-PL') }}</span>
            </div>
          </div>
        </div>
      </div>
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

.teacher-grades {
  flex: 1;
  color: white;
}

.teacher-grades h1 {
  margin-bottom: 30px;
  font-size: 24px;
}

.form-section, .grades-section {
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-section h2, .grades-section h2 {
  margin: 0 0 20px 0;
  font-size: 18px;
}

.grade-form {
  display: grid;
  gap: 15px;
  max-width: 400px;
}

.grade-form label {
  display: grid;
  gap: 5px;
}

.grade-form span {
  font-weight: 600;
}

.grade-form input, .grade-form select, .grade-form textarea {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(148,163,184,.25);
  background: #0b1220;
  color: white;
}

.grade-form textarea {
  resize: vertical;
  min-height: 80px;
}

.submit-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.no-grades {
  text-align: center;
  color: #94a3b8;
  padding: 20px;
}

.subjects {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.subject-block {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
}

.subject-block h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.grades-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.grade-entry {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.grade-value {
  background: #3b82f6;
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

.student-name {
  flex: 1;
  font-weight: 500;
}

.grade-date {
  color: #94a3b8;
  font-size: 14px;
}
</style>