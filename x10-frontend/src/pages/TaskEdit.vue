<template>
  <AppLayout current-page="calendar" :show-back="true" :title="pageTitle" :subtitle="'📅 ' + date + (isEdit ? ' · 编辑中' : '')">
    <template #actions>
      <button @click="$router.back()" class="px-4 py-2 border border-slate-200 rounded-xl hover:bg-slate-50 text-sm">✕ 取消</button>
      <button @click="handleSubmit" :disabled="loading" class="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-5 py-2.5 text-sm font-medium flex items-center gap-2 shadow-lg shadow-blue-600/25 transition-all disabled:opacity-50">
        <template v-if="loading"><span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />保存中...</template>
        <template v-else>💾 {{ isEdit ? '更新' : '保存' }}</template>
      </button>
    </template>

    <!-- 表单内容 -->
    <div class="p-4 lg:p-6 max-w-4xl mx-auto">
      <div class="space-y-6">
        <!-- 营业额目标 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
          <h2 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <span class="text-blue-600">🎯</span> 营业额目标
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-slate-700 mb-2 block">目标营业额 (元)</label>
              <input
                v-model="targetAmount"
                type="number"
                placeholder="请输入目标营业额"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
              />
            </div>
            <div>
              <label class="text-sm font-medium text-slate-700 mb-2 block">已完成营业额 (元)</label>
              <input
                v-model="completedAmount"
                type="number"
                placeholder="请输入已完成营业额"
                class="w-full h-12 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
              />
            </div>
          </div>
        </div>

        <!-- 任务列表 -->
        <div class="bg-white rounded-2xl p-4 lg:p-6 shadow-sm border border-slate-200">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-slate-800 flex items-center gap-2">
              <span class="text-emerald-600">📈</span>
              当日任务
              <span class="ml-2 bg-slate-100 text-slate-600 rounded-lg px-2 py-0.5 text-xs">{{ taskList.length }}个</span>
            </h2>
            <button type="button" @click="addTask" class="flex items-center gap-1 px-3 py-1.5 border border-slate-200 rounded-xl hover:bg-slate-50 text-sm">
              + 添加任务
            </button>
          </div>

          <div class="space-y-4">
            <div
              v-for="(task, index) in taskList"
              :key="task.id"
              :class="[
                'rounded-xl border transition-all',
                expandedTask === task.id ? 'bg-white border-blue-200 shadow-md' : 'bg-slate-50 border-slate-200 hover:border-slate-300'
              ]"
            >
              <!-- 任务头部 -->
              <div class="p-4 cursor-pointer" @click="toggleExpand(task.id)">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <div :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0',
                      task.priority === 'high' ? 'bg-red-100 text-red-700' :
                      task.priority === 'medium' ? 'bg-amber-100 text-amber-700' :
                      'bg-blue-100 text-blue-700'
                    ]">
                      {{ index + 1 }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2">
                        <h3 class="font-medium text-slate-800 truncate">
                          {{ task.title || '未命名任务' }}
                        </h3>
                        <span v-if="task.title && task.status === 'completed'" class="text-emerald-500 flex-shrink-0">✅</span>
                      </div>
                      <p class="text-sm text-slate-500 truncate mt-0.5">
                        {{ task.action || '暂无动作描述' }}
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <span :class="getPriorityClass(task.priority) + ' hidden sm:inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded'">
                      🚩 {{ getPriorityLabel(task.priority) }}
                    </span>
                    <span :class="getStatusClass(task.status) + ' hidden sm:inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded'">
                      {{ getStatusLabel(task.status) }}
                    </span>
                    <button
                      v-if="taskList.length > 1"
                      type="button"
                      class="text-red-500 hover:text-red-600 hover:bg-red-50 p-1 rounded-lg"
                      @click.stop="removeTask(task.id)"
                    >
                      🗑
                    </button>
                  </div>
                </div>
              </div>

              <!-- 任务详情 - 展开时显示 -->
              <div v-if="expandedTask === task.id" class="px-4 pb-4 border-t border-slate-100">
                <div class="pt-4 space-y-4">
                  <!-- 任务标题 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block">
                      任务标题 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="task.title"
                      placeholder="请输入任务标题"
                      class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                    />
                  </div>

                  <!-- 当日动作 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block">
                      当日动作 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="task.action"
                      placeholder="如：客户拜访、产品演示、合同签订"
                      class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                    />
                  </div>

                  <!-- 时间选择 -->
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                        <span>⏰</span> 开始时间
                      </label>
                      <input
                        type="time"
                        v-model="task.startTime"
                        class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                      />
                    </div>
                    <div>
                      <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                        <span>⏰</span> 结束时间
                      </label>
                      <input
                        type="time"
                        v-model="task.endTime"
                        class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                      />
                    </div>
                  </div>

                  <!-- 优先级和状态 -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                        <span>🚩</span> 优先级
                      </label>
                      <select
                        v-model="task.priority"
                        class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                      >
                        <option v-for="p in priorityOptions" :key="p.value" :value="p.value">{{ p.label }}</option>
                      </select>
                    </div>
                    <div>
                      <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                        <span>✅</span> 任务状态
                      </label>
                      <select
                        v-model="task.status"
                        class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                      >
                        <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                      </select>
                    </div>
                  </div>

                  <!-- 负责人 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                      <span>👤</span> 负责人
                    </label>
                    <input
                      v-model="task.responsible"
                      placeholder="负责人姓名"
                      class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                    />
                  </div>

                  <!-- 提醒设置 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                      <span>🔔</span> 提醒设置
                    </label>
                    <select
                      v-model="task.reminder"
                      class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                    >
                      <option v-for="r in reminderOptions" :key="r.value" :value="r.value">{{ r.label }}</option>
                    </select>
                  </div>

                  <!-- 风险备注 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                      <span>⚠</span> 风险备注
                    </label>
                    <input
                      v-model="task.risk"
                      placeholder="无风险可不填，如有风险请描述具体情况"
                      class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all"
                    />
                    <p v-if="task.risk && task.risk !== '无'" class="text-xs text-amber-600 mt-1 flex items-center gap-1">
                      <span>⚠</span> 已标记风险
                    </p>
                  </div>

                  <!-- 详细描述 -->
                  <div>
                    <label class="text-sm font-medium text-slate-700 mb-2 block flex items-center gap-1">
                      <span>📄</span> 详细描述
                    </label>
                    <textarea
                      v-model="task.description"
                      placeholder="添加任务的详细描述、注意事项等..."
                      rows="4"
                      class="w-full min-h-[100px] p-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none transition-all resize-none"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 提示信息 -->
          <div class="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-700 flex items-start gap-2">
            <span class="mt-0.5">🔔</span>
            <div>
              <p class="font-medium">提示</p>
              <p class="text-blue-600 mt-1">点击任务卡片可展开/收起详情，带 * 号的为必填项</p>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-4">
          <button @click="$router.back()" class="flex-1 h-12 border border-slate-200 rounded-xl hover:bg-slate-50 text-sm font-medium">取消</button>
          <button @click="handleSubmit" :disabled="loading" class="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-medium flex items-center justify-center gap-2 shadow-lg shadow-blue-600/25 transition-all disabled:opacity-50">
            💾 保存任务
          </button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'
import { useTaskStore } from '@/stores/tasks'

const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()

const date = ref((route.query.date as string) || new Date().toISOString().split('T')[0])
const taskId = ref(route.query.taskId ? String(route.query.taskId) : null)
const isEdit = computed(() => !!taskId.value)
const pageTitle = computed(() => isEdit.value ? '编辑任务' : '新建任务')
const loading = ref(false)
const expandedTask = ref<number | null>(null)

const targetAmount = ref('')
const completedAmount = ref('')

interface TaskItem {
  id: number
  title: string
  action: string
  responsible: string
  risk: string
  startTime: string
  endTime: string
  priority: string
  reminder: string
  status: string
  description: string
}

const taskList = ref<TaskItem[]>([{
  id: 1,
  title: '',
  action: '',
  responsible: '',
  risk: '',
  startTime: '09:00',
  endTime: '10:00',
  priority: 'medium',
  reminder: '15',
  status: 'pending',
  description: ''
}])

const priorityOptions = [
  { value: 'high', label: '高优先级' },
  { value: 'medium', label: '中优先级' },
  { value: 'low', label: '低优先级' }
]

const statusOptions = [
  { value: 'pending', label: '待处理' },
  { value: 'in_progress', label: '进行中' },
  { value: 'completed', label: '已完成' },
  { value: 'cancelled', label: '已取消' }
]

const reminderOptions = [
  { value: '0', label: '不提醒' },
  { value: '5', label: '提前5分钟' },
  { value: '15', label: '提前15分钟' },
  { value: '30', label: '提前30分钟' },
  { value: '60', label: '提前1小时' },
  { value: '1440', label: '提前1天' }
]

function getPriorityLabel(p: string) {
  return priorityOptions.find(o => o.value === p)?.label || '中优先级'
}

function getPriorityClass(p: string) {
  if (p === 'high') return 'bg-red-100 text-red-700'
  if (p === 'medium') return 'bg-amber-100 text-amber-700'
  return 'bg-blue-100 text-blue-700'
}

function getStatusLabel(s: string) {
  return statusOptions.find(o => o.value === s)?.label || '待处理'
}

function getStatusClass(s: string) {
  if (s === 'completed') return 'bg-emerald-100 text-emerald-700'
  if (s === 'in_progress') return 'bg-blue-100 text-blue-700'
  if (s === 'cancelled') return 'bg-gray-100 text-gray-700'
  return 'bg-slate-100 text-slate-700'
}

function addTask() {
  const newTask: TaskItem = {
    id: Date.now(),
    title: '',
    action: '',
    responsible: '',
    risk: '',
    startTime: '09:00',
    endTime: '10:00',
    priority: 'medium',
    reminder: '15',
    status: 'pending',
    description: ''
  }
  taskList.value.push(newTask)
  expandedTask.value = newTask.id
}

function removeTask(id: number) {
  if (taskList.value.length === 1) {
    alert('至少保留一个任务')
    return
  }
  taskList.value = taskList.value.filter(t => t.id !== id)
  if (expandedTask.value === id) {
    expandedTask.value = null
  }
}

function toggleExpand(id: number) {
  expandedTask.value = expandedTask.value === id ? null : id
}

/** 从验证错误中提取可读消息 */
function extractErrorMsg(e: any): string {
  const detail = e?.response?.data?.detail
  if (!detail) return '保存失败'
  // FastAPI 422 验证错误：detail 是对象数组
  if (Array.isArray(detail)) {
    return detail.map((d: any) => d.msg || '未知错误').join('；')
  }
  // 普通字符串错误
  if (typeof detail === 'string') return detail
  return '保存失败'
}

async function handleSubmit() {
  // 验证必填字段
  const invalidTasks = taskList.value.filter(t => !t.title.trim() || !t.action.trim())
  if (invalidTasks.length > 0) {
    alert('请填写任务标题和当日动作')
    return
  }

  loading.value = true
  try {
    const dateKey = date.value

    // 1. 保存每日目标
    await api.put(`/tasks/target/${dateKey}`, {
      target_amount: parseFloat(targetAmount.value) || 0,
      completed_amount: parseFloat(completedAmount.value) || 0
    })

    // 2. 保存每个任务（逐个创建）
    for (const task of taskList.value) {
      const taskPayload = {
        date_key: dateKey,
        action: task.action,
        responsible: task.responsible,
        risk: task.risk || '无',
        status: task.status,
        amount: 0
      }
      await api.post('/tasks', taskPayload)
    }

    router.back()
  } catch (e: any) {
    console.error('保存失败:', e)
    alert(extractErrorMsg(e))
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // 从 localStorage 加载已有数据
  try {
    const savedTasks = localStorage.getItem('calendar_tasks')
    if (savedTasks) {
      const parsed = JSON.parse(savedTasks)
      if (typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)) {
        const dateTasks = parsed[date.value]
        if (dateTasks) {
          targetAmount.value = dateTasks.targetAmount || ''
          completedAmount.value = dateTasks.completedAmount || ''
          if (isEdit.value && taskId.value && dateTasks.tasks) {
            const found = dateTasks.tasks.find((t: any) => String(t.id) === String(taskId.value))
            if (found) {
              taskList.value = [{ ...found }]
            }
          } else if (dateTasks.tasks && dateTasks.tasks.length > 0) {
            taskList.value = dateTasks.tasks.map((t: any) => ({ ...t }))
          }
        }
      }
    }
  } catch (e) {
    console.error('加载失败:', e)
  }

  // 同时尝试从 API 加载
  try {
    const res = await api.get(`/tasks?date=${date.value}`)
    if (res.data && res.data.tasks) {
      targetAmount.value = String(res.data.targetAmount || '')
      completedAmount.value = String(res.data.completedAmount || '')
      if (!isEdit.value && res.data.tasks.length > 0) {
        taskList.value = res.data.tasks.map((t: any) => ({ ...t }))
      } else if (isEdit.value && taskId.value) {
        const found = res.data.tasks.find((t: any) => String(t.id) === String(taskId.value))
        if (found) {
          taskList.value = [{ ...found }]
        }
      }
    }
  } catch (e) {
    // API 不可用时回退到 localStorage
  }
})
</script>
