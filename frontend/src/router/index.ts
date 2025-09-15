import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('@/views/AuthView.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    beforeEnter: () => {
      const auth = useAuthStore()
      if (auth.role === 'teacher') {
        return { name: 'dashboard-teacher' }
      }
      if (auth.role === 'student') {
        return { name: 'dashboard-student' }
      }
      return { name: 'auth' }
    },
    component: () => import('@/views/DashboardView.vue'),
  },
  {
    path: '/dashboard/teacher',
    name: 'dashboard-teacher',
    component: () => import('@/views/DashboardTeacherView.vue'),
    meta: { roles: ['teacher'] },
  },
  {
    path: '/dashboard/student',
    name: 'dashboard-student',
    component: () => import('@/views/DashboardStudentView.vue'),
    meta: { roles: ['student'] },
  },
  // Student endpoints under /dashboard/*
  {
    path: '/dashboard/home',
    name: 'dashboard-student-home',
    component: () => import('@/views/DashboardStudentView.vue'),
    meta: { roles: ['student'] },
  },
  {
    path: '/dashboard/schedule',
    name: 'dashboard-student-schedule',
    component: () => import('@/views/ScheduleView.vue'),
    meta: { roles: ['student'] },
  },
  {
    path: '/dashboard/grades',
    name: 'dashboard-student-grades',
    component: () => import('@/views/GradesView.vue'),
    meta: { roles: ['student'] },
  },
  {
    path: '/dashboard/teacher/calendar',
    name: 'dashboard-teacher-calendar',
    component: () => import('@/views/ScheduleView.vue'),
    meta: { roles: ['teacher'] },
  },
  {
    path: '/dashboard/teacher/grades',
    name: 'dashboard-teacher-grades',
    component: () => import('@/views/TeacherGradesView.vue'),
    meta: { roles: ['teacher'] },
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: () => import('@/views/ScheduleView.vue'),
  },
  {
    path: '/grades',
    name: 'grades',
    component: () => import('@/views/GradesView.vue'),
  },
  {
    path: '/students',
    name: 'students',
    component: () => import('@/views/StudentsView.vue'),
    meta: { roles: ['student'] },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  
  // Check role-based access for protected routes only
  const roles = to.meta.roles as string[] | undefined
  if (roles && roles.length > 0) {
    if (!auth.isAuthenticated || !auth.role || !roles.includes(auth.role)) {
      return { name: 'auth' }
    }
  }
  
  return true
})

export default router
