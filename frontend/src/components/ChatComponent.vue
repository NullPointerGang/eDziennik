<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getMessages, sendMessage, type Message } from '@/services/messagesService'
import { httpClient } from '@/utils/http'

const auth = useAuthStore()
const messages = ref<Message[]>([])
const users = ref<Array<{ id: number; first_name: string; last_name: string; roles: string[] }>>([])
const selectedUserId = ref<number | null>(null)
const newMessage = ref('')
const loading = ref(false)
const chatContainer = ref<HTMLElement>()
const refreshInterval = ref<NodeJS.Timeout | null>(null)

const availableUsers = computed(() => {
  const currentUserRole = auth.role
  if (currentUserRole === 'student') {
    return users.value.filter(user => user.roles.includes('teacher'))
  } else {
    return users.value.filter(user => user.roles.includes('student'))
  }
})

const chatMessages = computed(() => {
  if (!selectedUserId.value) return []
  
  return messages.value
    .filter(msg => 
      (msg.from_id === parseInt(auth.userId!) && msg.to_id === selectedUserId.value) ||
      (msg.from_id === selectedUserId.value && msg.to_id === parseInt(auth.userId!))
    )
    .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
})

function getUserName(userId: number) {
  const user = users.value.find(u => u.id === userId)
  return user ? `${user.first_name} ${user.last_name}` : 'Nieznany użytkownik'
}

function formatTime(dateString: string) {
  return new Date(dateString).toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

async function loadUsers() {
  try {
    users.value = await httpClient.get<Array<{ id: number; first_name: string; last_name: string; roles: string[] }>>('/users/')
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

async function loadMessages() {
  try {
    console.log('Loading messages, auth token:', auth.token)
    if (!auth.token) {
      console.warn('No auth token available')
      return
    }
    messages.value = await getMessages()
  } catch (error) {
    console.error('Failed to load messages:', error)
  }
}

async function sendNewMessage() {
  if (!newMessage.value.trim() || !selectedUserId.value) return
  
  if (!auth.token) {
    console.warn('No auth token available for sending message')
    return
  }
  
  loading.value = true
  try {
    await sendMessage({
      from_id: parseInt(auth.userId!),
      to_id: selectedUserId.value,
      content: newMessage.value.trim()
    })
    
    newMessage.value = ''
    await loadMessages()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    loading.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

onMounted(async () => {
  await Promise.all([loadUsers(), loadMessages()])
  
  // Auto-refresh messages every 3 seconds
  refreshInterval.value = setInterval(async () => {
    if (selectedUserId.value) {
      await loadMessages()
    }
  }, 3000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<template>
  <div class="chat-component">
    <h3>Wiadomości</h3>
    
    <div class="user-selector">
      <select v-model="selectedUserId">
        <option :value="null">Wybierz rozmówcę</option>
        <option v-for="user in availableUsers" :key="user.id" :value="user.id">
          {{ user.first_name }} {{ user.last_name }}
        </option>
      </select>
    </div>
    
    <div v-if="selectedUserId" class="chat-container">
      <div ref="chatContainer" class="messages-list">
        <div v-if="chatMessages.length === 0" class="no-messages">
          Brak wiadomości
        </div>
        <div 
          v-for="message in chatMessages" 
          :key="message.id" 
          class="message"
          :class="{ 'own-message': message.from_id === parseInt(auth.userId!) }"
        >
          <div class="message-header">
            <span class="sender">{{ getUserName(message.from_id) }}</span>
            <span class="time">{{ formatTime(message.created_at) }}</span>
          </div>
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
      
      <div class="message-input">
        <input 
          v-model="newMessage" 
          @keyup.enter="sendNewMessage"
          placeholder="Napisz wiadomość..."
          :disabled="loading"
        />
        <button @click="sendNewMessage" :disabled="loading || !newMessage.trim()">
          Wyślij
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-component {
  border: 1px solid white;
  border-radius: 24px;
  padding: 20px;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-component h3 {
  margin: 0 0 15px 0;
  color: white;
}

.user-selector {
  margin-bottom: 15px;
}

.user-selector select {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(148,163,184,.25);
  background: #0b1220;
  color: white;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 15px;
  padding-right: 5px;
}

.no-messages {
  text-align: center;
  color: #94a3b8;
  padding: 20px;
}

.message {
  margin-bottom: 12px;
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
}

.message.own-message {
  background: #3b82f6;
  margin-left: 20px;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 12px;
}

.sender {
  font-weight: 600;
  color: white;
}

.time {
  color: #94a3b8;
}

.message-content {
  color: white;
  word-wrap: break-word;
}

.message-input {
  display: flex;
  gap: 8px;
}

.message-input input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(148,163,184,.25);
  background: #0b1220;
  color: white;
}

.message-input button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.message-input button:hover:not(:disabled) {
  background: #2563eb;
}

.message-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>