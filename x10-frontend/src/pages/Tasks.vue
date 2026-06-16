<template>
  <AppLayout current-page="calendar" title="任务列表" subtitle="管理所有任务">
    <template #actions>
      <button @click="$router.push('/task-edit')" class="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl px-5 h-11 shadow-lg shadow-blue-600/25 transition-all duration-200 flex items-center">
        <span class="mr-2">+</span> 新建任务
      </button>
    </template>

    <!-- 统计卡片 -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-slate-500 truncate">总任务</p>
              <p class="text-2xl font-bold text-slate-900 mt-2 truncate">{{ stats.total }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2">
              <span class="text-blue-600 text-lg">☑</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-slate-500 truncate">待处理</p>
              <p class="text-2xl font-bold text-amber-600 mt-2 truncate">{{ stats.pending + stats.inProgress }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2">
              <span class="text-amber-600 text-lg">⏰</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-slate-500 truncate">已完成</p>
              <p class="text-2xl font-bold text-emerald-600 mt-2 truncate">{{ stats.completed }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2">
              <span class="text-emerald-600 text-lg">✅</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-slate-500 truncate">风险任务</p>
              <p class="text-2xl font-bold text-red-600 mt-2 truncate">{{ stats.risk }}</p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-red-50 to-red-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2">
              <span class="text-red-600 text-lg">⚠</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 pb-6">
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="relative flex-1 min-w-0">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
            <input
              v-model="searchQuery"
              placeholder="搜索任务标题、负责人..."
              class="w-full pl-11 pr-4 h-11 bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-blue-500 focus:ring-blue-500/20 rounded-xl outline-none transition-all"
            />
          </div>
          <div class="flex gap-3">
            <select v-model="statusFilter" class="w-[150px] h-11 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 px-3 text-sm outline-none focus:border-blue-500">
              <option value="all">全部状态</option>
              <option value="pending">待处理</option>
              <option value="in_progress">进行中</option>
              <option value="completed">已完成</option>
              <option value="cancelled">已取消</option>
            </select>
            <select v-model="priorityFilter" class="w-[150px] h-11 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 px-3 text-sm outline-none focus:border-blue-500">
              <option value="all">全部优先级</option>
              <option value="high">高优先级</option>
              <option value="medium">中优先级</option>
              <option value="low">低优先级</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 pb-8">
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="p-4 border-b border-slate-100">
          <div class="grid grid-cols-4 bg-slate-50 rounded-xl p-1">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'rounded-lg py-2 text-sm font-medium transition-all',
                activeTab === tab.key ? 'bg-white shadow-sm text-slate-900' : 'text-slate-500 hover:text-slate-700'
              ]"
            >{{ tab.label }}</button>
          </div>
        </div>

        <div>
          <div v-if="loading" class="text-center py-16">
            <div class="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mx-auto mb-4" />
            <p class="text-slate-500">加载中...</p>
          </div>

          <div v-else-if="filteredTasks.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl text-slate-400">☑</span>
            </div>
            <p class="text-slate-500">暂无任务</p>
            <button @click="$router.push('/task-edit')" class="mt-4 px-4 py-2 border border-slate-200 rounded-xl hover:bg-slate-50 text-sm">
              + 新建任务
            </button>
          </div>

          <div v-else class="p-4 space-y-3">
            <div
              v-for="(task, index) in filteredTasks"
              :key="task.id"
              class="flex items-start gap-4 p-4 bg-white border border-slate-100 rounded-xl hover:border-slate-200 hover:shadow-sm transition-all duration-200"
              :style="{ animationDelay: `${index * 50}ms` }"
            >
              <button
                :class="[
                  'mt-1 flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-all',
                  task.status === 'completed' ? 'text-emerald-600 bg-emerald-50' : 'text-slate-300 hover:text-blue-600 hover:bg-blue-50'
                ]"
                @click="toggleStatus(task)"
              >
                <span>{{ task.status === 'completed' ? '✅' : '☑' }}</span>
              </button>

              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0 flex-1">
                    <h3 :class="['font-medium text-slate-900 truncate', task.status === 'completed' ? 'line-through text-slate-400' : '']">
                      {{ task.title || '未命名任务' }}
                    </h3>
                    <p class="text-sm text-slate-500 mt-1 truncate">{{ task.action || '' }}</p>
                  </div>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <span :class="getPriorityClass(task.priority)">{{ getPriorityLabel(task.priority) }}</span>
                    <span :class="getStatusClass(task.status)">{{ getStatusLabel(task.status) }}</span>
                  </div>
                </div>

                <div class="flex flex-wrap items-center gap-4 mt-3 text-sm text-slate-500">
                  <span class="flex items-center gap-1.5 flex-shrink-0">
                    <span>📅</span>
                    <span class="whitespace-nowrap">{{ task.date }}</span>
                  </span>
                  <span v-if="task.startTime" class="flex items-center gap-1.5 flex-shrink-0">
                    <span>⏰</span>
                    <span class="whitespace-nowrap">{{ task.startTime }} - {{ task.endTime }}</span>
                  </span>
                  <span v-if="task.responsible" class="flex items-center gap-1.5 min-w-0">
                    <span class="flex-shrink-0">👤</span>
                    <span class="truncate">{{ task.responsible }}</span>
                  </span>
                  <span v-if="task.risk && task.risk !== '无'" class="flex items-center gap-1.5 text-amber-600 flex-shrink-0 bg-amber-50 px-2 py-1 rounded-lg">
                    <span>⚠</span>
                    <span class="whitespace-nowrap">{{ task.risk }}</span>
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-1 flex-shrink-0">
                <button class="h-8 w-8 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-blue-600 flex items-center justify-center transition-all" @click="editTask(task)">
                  <span class="text-sm">✎</span>
                </button>
                <button class="h-8 w-8 rounded-lg hover:bg-red-50 text-slate-500 hover:text-red-600 flex items-center justify-center transition-all" @click="deleteTask(task)">
                  <span class="text-sm">🗑</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'

const router = useRouter()

const searchQuery = ref('')
const statusFilter = ref('all')
const priorityFilter = ref('all')
const activeTab = ref('all')
const loading = ref(false)
const allTasks = ref<any[]>([])

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'today', label: '今日' },
  { key: 'upcoming', label: '即将到来' },
  { key: 'risk', label: '风险' }
]

const priorityConfig: Record<string, { label: string; cls: string }> = {
  high: { label: '高', cls: 'bg-red-100 text-red-700 border border-red-200 rounded-lg px-2.5 py-1 text-xs font-medium' },
  medium: { label: '中', cls: 'bg-amber-100 text-amber-700 border border-amber-200 rounded-lg px-2.5 py-1 text-xs font-medium' },
  low: { label: '低', cls: 'bg-blue-100 text-blue-700 border border-blue-200 rounded-lg px-2.5 py-1 text-xs font-medium' }
}

const statusConfig: Record<string, { label: string; cls: string }> = {
  pending: { label: '待处理', cls: 'bg-slate-100 text-slate-700 rounded-lg px-2.5 py-1 text-xs font-medium' },
  in_progress: { label: '进行中', cls: 'bg-blue-100 text-blue-700 rounded-lg px-2.5 py-1 text-xs font-medium' },
  completed: { label: '已完成', cls: 'bg-emerald-100 text-emerald-700 rounded-lg px-2.5 py-1 text-xs font-medium' },
  cancelled: { label: '已取消', cls: 'bg-gray-100 text-gray-700 rounded-lg px-2.5 py-1 text-xs font-medium' }
}

const stats = computed(() => ({
  total: allTasks.value.length,
  pending: allTasks.value.filter((t: any) => t.status === 'pending').length,
  inProgress: allTasks.value.filter((t: any) => t.status === 'in_progress').length,
  completed: allTasks.value.filter((t: any) => t.status === 'completed').length,
  risk: allTasks.value.filter((t: any) => t.risk && t.risk !== '无').length
}))

const filteredTasks = computed(() => {
  let filtered = allTasks.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter((t: any) =>
      (t.title || '').toLowerCase().includes(q) ||
      (t.action || '').toLowerCase().includes(q) ||
      (t.responsible || '').toLowerCase().includes(q)
    )
  }
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter((t: any) => t.status === statusFilter.value)
  }
  if (priorityFilter.value !== 'all') {
    filtered = filtered.filter((t: any) => t.priority === priorityFilter.value)
  }
  if (activeTab.value === 'today') {
    const today = new Date().toISOString().split('T')[0]
    filtered = filtered.filter((t: any) => t.date === today)
  } else if (activeTab.value === 'upcoming') {
    const today = new Date().toISOString().split('T')[0]
    filtered = filtered.filter((t: any) => t.date >= today)
  } else if (activeTab.value === 'risk') {
    filtered = filtered.filter((t: any) => t.risk && t.risk !== '无')
  }
  return filtered
})

function getPriorityLabel(p: string) {
  return priorityConfig[p]?.label || '中'
}

function getPriorityClass(p: string) {
  return priorityConfig[p]?.cls || priorityConfig.medium.cls
}

function getStatusLabel(s: string) {
  return statusConfig[s]?.label || '待处理'
}

function getStatusClass(s: string) {
  return statusConfig[s]?.cls || statusConfig.pending.cls
}

async function toggleStatus(task: any) {
  const newStatus = task.status === 'completed' ? 'pending' : 'completed'
  try {
    await api.put(`/tasks/${task.id}`, { status: newStatus })
    task.status = newStatus
  } catch (e) {
    console.error('更新状态失败:', e)
  }
}

function editTask(task: any) {
  router.push({ path: '/task-edit', query: { date: task.date, taskId: String(task.id) } })
}

async function deleteTask(task: any) {
  if (!confirm('确定要删除这个任务吗？')) return
  try {
    await api.delete(`/tasks/${task.date}/${task.id}`)
    allTasks.value = allTasks.value.filter((t: any) => t.id !== task.id)
  } catch (e) {
    console.error('删除失败:', e)
  }
}

async function loadTasks() {
  loading.value = true
  try {
    const res = await api.get('/tasks')
    if (res.data) {
      // Flatten tasks from all dates
      const flat: any[] = []
      Object.entries(res.data).forEach(([date, dayData]: [string, any]) => {
        if (dayData.tasks) {
          dayData.tasks.forEach((t: any) => {
            flat.push({ ...t, date, targetAmount: dayData.targetAmount, completedAmount: dayData.completedAmount })
          })
        }
      })
      allTasks.value = flat
    }
  } catch (e) {
    console.error('加载任务失败:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTasks()
})
</script>
