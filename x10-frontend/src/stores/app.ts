import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useAppStore = defineStore('app', () => {
  const systemName = ref('X10增长引擎')
  const companyName = ref('让目标清晰，让过程可见，让增长可复制')

  function loadConfig() {
    api.get('/config').then((res) => {
      if (res.data) {
        systemName.value = res.data.systemName || 'X10增长引擎'
        companyName.value = res.data.companyName || '让目标清晰，让过程可见，让增长可复制'
      }
    }).catch(() => {
      // 使用默认值
    })
  }

  return { systemName, companyName, loadConfig }
})
