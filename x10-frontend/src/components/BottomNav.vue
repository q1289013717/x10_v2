<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t border-slate-200/80 z-50">
    <div class="flex items-center justify-around px-2 py-1 max-w-lg mx-auto">
      <button
        v-for="item in navItems"
        :key="item.id"
        @click="handleNavigate(item.id)"
        class="flex flex-col items-center justify-center gap-0.5 px-3 py-2 rounded-2xl min-w-[64px] min-h-[56px] transition-all duration-150 ease-out active:scale-95"
        :class="currentPage === item.id ? 'text-blue-600 bg-blue-50/80' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-50'"
        :aria-label="item.label"
      >
        <div class="relative p-1.5 rounded-xl transition-all duration-200" :class="{ 'bg-blue-100': currentPage === item.id }">
          <component :is="item.icon" class="w-5 h-5 transition-all duration-200" :class="currentPage === item.id ? 'stroke-[2.5px]' : 'stroke-2'" />
          <!-- 首页告警角标 -->
          <span v-if="item.id === 'home' && alertCount > 0" class="absolute -top-1 -right-1 min-w-[16px] h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center px-1">
            {{ alertCount }}
          </span>
          <span v-if="currentPage === item.id" class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-blue-600 rounded-full" />
        </div>
        <span class="text-[11px] font-medium transition-all duration-200" :class="currentPage === item.id ? 'text-blue-600' : 'text-slate-400'">
          {{ item.label }}
        </span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { h } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()

defineProps<{ currentPage: string }>()
const emit = defineEmits<{ navigate: [pageId: string] }>()

function handleNavigate(pageId: string) {
  emit('navigate', pageId)
  router.push({ name: pageId }).catch(() => {})
}

// SVG icons as simple functional components
const HomeIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('path', { d: 'm3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }), h('polyline', { points: '9 22 9 12 15 12 15 22' })]) }
const CalendarIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('rect', { width: '18', height: '18', x: '3', y: '4', rx: '2', ry: '2' }), h('line', { x1: '16', y1: '2', x2: '16', y2: '6' }), h('line', { x1: '8', y1: '2', x2: '8', y2: '6' }), h('line', { x1: '3', y1: '10', x2: '21', y2: '10' })]) }
const DatabaseIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('ellipse', { cx: '12', cy: '5', rx: '9', ry: '3' }), h('path', { d: 'M21 12c0 1.66-4 3-9 3s-9-1.34-9-3' }), h('path', { d: 'M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5' })]) }
const GraduationIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('path', { d: 'M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z' }), h('path', { d: 'M22 10v6' }), h('path', { d: 'M6 12.5V16a6 3 0 0 0 12 0v-3.5' })]) }
const SettingsIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('path', { d: 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z' }), h('circle', { cx: '12', cy: '12', r: '3' })]) }

const ReportIcon = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'lucide' }, [h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }), h('polyline', { points: '14 2 14 8 20 8' }), h('line', { x1: '16', y1: '13', x2: '8', y2: '13' }), h('line', { x1: '16', y1: '17', x2: '8', y2: '17' }), h('polyline', { points: '10 9 9 9 8 9' })]) }

const navItems = [
  { id: 'home', label: '首页', icon: HomeIcon },
  { id: 'calendar', label: '日历', icon: CalendarIcon },
  { id: 'reports', label: '报告', icon: ReportIcon },
  { id: 'darensource', label: '资源库', icon: DatabaseIcon },
  { id: 'training', label: '成长中心', icon: GraduationIcon },
]

const authStore = useAuthStore()
const isAdmin = authStore.isAdmin
const alertCount = ref(0)
let alertTimer: ReturnType<typeof setInterval> | null = null

async function fetchAlertCount() {
  if (!isAdmin) return
  try {
    const res = await api.get('/admin/alerts')
    const data = res.data
    alertCount.value = (data.daily_missing?.length || 0) + (data.weekly_missing?.length || 0) + (data.task_quota_alert?.length || 0)
  } catch {
    // 静默
  }
}

onMounted(() => {
  fetchAlertCount()
  alertTimer = setInterval(fetchAlertCount, 60000)
})

onUnmounted(() => {
  if (alertTimer) {
    clearInterval(alertTimer)
    alertTimer = null
  }
})
</script>
