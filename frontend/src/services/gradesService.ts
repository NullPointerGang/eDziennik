import { httpClient } from '@/utils/http'

export type Grade = {
  id: number
  student_id: number
  teacher_id: number
  subject: string
  value: number
  date: string
  comment?: string
}

export async function getGrades(studentId?: number): Promise<Grade[]> {
  const params = studentId ? `?student_id=${studentId}` : ''
  return await httpClient.get<Grade[]>(`/grades${params}`)
}

export type CreateGradeInput = {
  student_id: number
  teacher_id: number
  subject: string
  value: number
  date: string
  comment?: string
}

export async function createGrade(input: CreateGradeInput): Promise<Grade> {
  return await httpClient.post<Grade>('/grades/', input)
}