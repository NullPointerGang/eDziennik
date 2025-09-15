import { httpClient } from '@/utils/http'

export type Message = {
  id: number
  from_id: number
  to_id?: number
  class_name?: string
  content: string
  created_at: string
}

export type CreateMessageInput = {
  from_id?: number
  to_id?: number
  class_name?: string
  content: string
}

export async function getMessages(fromId?: number, toId?: number): Promise<Message[]> {
  const params = new URLSearchParams()
  if (fromId) params.append('from_id', fromId.toString())
  if (toId) params.append('to_id', toId.toString())
  
  const queryString = params.toString()
  return await httpClient.get<Message[]>(`/messages/${queryString ? '?' + queryString : ''}`)
}

export async function sendMessage(input: CreateMessageInput): Promise<Message> {
  return await httpClient.post<Message>('/messages/', input)
}