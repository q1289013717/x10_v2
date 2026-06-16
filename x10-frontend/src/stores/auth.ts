import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'
import router from '@/router'

export interface User {
  id: string
  account: string
  name: string
  role: string
  company: string
  avatar: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)
  const error = ref('')

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role?.includes('管理员') ?? false)

  // 登录 — 对接后端 JWT API
  async function login(account: string, password: string) {
    loading.value = true
    error.value = ''
    try {
      const res = await api.post('/auth/login', { account, password })
      token.value = res.data.access_token
      user.value = res.data.user
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('current_user', JSON.stringify(res.data.user))
      return res.data
    } catch (e: any) {
      const msg = e.response?.data?.detail || '登录失败'
      error.value = msg
      throw new Error(msg)
    } finally {
      loading.value = false
    }
  }

  // 获取当前用户信息
  async function fetchCurrentUser() {
    try {
      const res = await api.get('/auth/me')
      user.value = res.data
      localStorage.setItem('current_user', JSON.stringify(res.data))
    } catch (e) {
      // Token 失效，清除状态
      logout(true)
    }
  }

  // 登出
  function logout(silent = false) {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
    if (!silent) {
      router.push('/login')
    }
  }

  // 初始化时从 localStorage 恢复
  function restore() {
    const saved = localStorage.getItem('current_user')
    if (saved) {
      try {
        user.value = JSON.parse(saved)
      } catch {
        user.value = null
      }
    }
  }

  return { user, token, loading, error, isLoggedIn, isAdmin, login, logout, fetchCurrentUser, restore }
})
