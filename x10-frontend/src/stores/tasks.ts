import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export interface Task {
  id?: number
  date: string
  title: string
  description?: string
  amount?: number
  status: 'pending' | 'completed' | 'cancelled'
  risk?: string
  category?: string
  priority?: string
  responsible?: string
  remarks?: string
  created_at?: string
  updated_at?: string
}

export interface DayData {
  date: string
  targetAmount: number
  completedAmount: number
  tasks: Task[]
}

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Record<string, DayData>>({})
  const loading = ref(false)

  async function fetchTasksByDate(date: string) {
    loading.value = true
    try {
      const res = await api.get(`/tasks?date=${date}`)
      if (res.data) {
        tasks.value = { ...tasks.value, [date]: res.data }
      }
    } catch (e) {
      console.error('获取任务失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchTasksByRange(start: string, end: string) {
    loading.value = true
    try {
      const res = await api.get(`/tasks/range?start=${start}&end=${end}`)
      if (res.data) {
        tasks.value = { ...tasks.value, ...res.data }
      }
    } catch (e) {
      console.error('获取任务范围失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function saveTask(date: string, dayData: DayData) {
    try {
      const { date: _d, ...rest } = dayData as any
      const res = await api.post('/tasks', { date, ...rest })
      tasks.value = { ...tasks.value, [date]: res.data }
      return res.data
    } catch (e) {
      console.error('保存任务失败:', e)
      throw e
    }
  }

  async function deleteTask(date: string, taskId: number) {
    try {
      await api.delete(`/tasks/${date}/${taskId}`)
      const day = tasks.value[date]
      if (day) {
        day.tasks = day.tasks.filter((t) => t.id !== taskId)
      }
    } catch (e) {
      console.error('删除任务失败:', e)
      throw e
    }
  }

  return { tasks, loading, fetchTasksByDate, fetchTasksByRange, saveTask, deleteTask }
})
