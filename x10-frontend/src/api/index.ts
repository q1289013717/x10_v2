import axios from 'axios'
import router from '@/router'

// 生产环境从环境变量读取，开发环境使用 Vite 代理
const apiBaseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: apiBaseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 — 自动添加 JWT Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 — 处理 401 自动跳转登录
let isRedirectingToLogin = false
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 避免重复跳转，且不在登录页跳转
      if (!isRedirectingToLogin && router.currentRoute.value.path !== '/login') {
        isRedirectingToLogin = true
        localStorage.removeItem('access_token')
        localStorage.removeItem('current_user')
        router.push('/login').finally(() => { isRedirectingToLogin = false })
      }
    }
    return Promise.reject(error)
  }
)

export default api
