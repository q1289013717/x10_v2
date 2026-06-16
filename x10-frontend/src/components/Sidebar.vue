<template>
  <aside class="w-64 bg-gradient-to-b from-[#1a1f2e] via-[#1e2533] to-[#1a1f2e] text-white h-full flex flex-col shadow-2xl relative overflow-hidden">
    <!-- 装饰背景 -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-0 right-0 w-40 h-40 bg-blue-500/5 rounded-full blur-3xl" />
      <div class="absolute bottom-0 left-0 w-32 h-32 bg-cyan-500/5 rounded-full blur-3xl" />
    </div>

    <!-- Logo区域 -->
    <div class="p-5 border-b border-white/5 relative z-10">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 via-blue-600 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
          <span class="text-white text-base">⚡</span>
        </div>
        <div class="flex-1 min-w-0">
          <template v-if="isAdmin && editingSystemName">
            <input
              v-model="editSystemNameValue"
              @blur="saveSystemName"
              @keyup.enter="saveSystemName"
              class="font-bold text-base text-white tracking-tight w-full bg-transparent border-b border-blue-400 outline-none"
            />
          </template>
          <h1 v-else
            class="font-bold text-base text-white tracking-tight truncate flex items-center gap-2"
            :class="{ 'cursor-pointer': isAdmin }"
            @dblclick="isAdmin && startEditSystemName()"
          >
            {{ systemName }}
            <span class="text-blue-400 text-xs">✨</span>
            <button v-if="isAdmin" @click="startEditSystemName()" class="opacity-50 hover:opacity-100 text-[10px]">✎</button>
          </h1>
          <template v-if="isAdmin && editingSubtitle">
            <input
              v-model="editSubtitleValue"
              @blur="saveSubtitle"
              @keyup.enter="saveSubtitle"
              class="text-xs text-slate-400 truncate w-full bg-transparent border-b border-blue-400/50 outline-none mt-0.5"
            />
          </template>
          <p v-else class="text-xs text-slate-400 truncate">{{ subtitle }}</p>
        </div>
      </div>
    </div>

    <!-- 菜单区域 -->
    <nav class="flex-1 p-3 space-y-1 overflow-y-auto relative z-10">
      <div class="px-3 py-2">
        <template v-if="isAdmin && editingSectionTitle">
          <input
            v-model="editSectionValue"
            @blur="saveSectionTitle"
            @keyup.enter="saveSectionTitle"
            class="text-xs font-semibold text-slate-500 uppercase tracking-wider bg-transparent border-b border-blue-400/50 outline-none w-full"
          />
        </template>
        <span
          v-else
          class="text-xs font-semibold text-slate-500 uppercase tracking-wider"
          :class="{ 'cursor-pointer': isAdmin }"
          @dblclick="isAdmin && (editingSectionTitle = true, editSectionValue = menuSectionTitle)"
        >{{ menuSectionTitle }}
          <button v-if="isAdmin" @click="editingSectionTitle = true; editSectionValue = menuSectionTitle" class="ml-1 text-[10px] opacity-50 hover:opacity-100">✎</button>
        </span>
      </div>

      <button
        v-for="(item, index) in menuItems"
        :key="item.id"
        @click="handleNavigate(item.id)"
        :class="[
          'w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 text-left group relative',
          currentPage === item.id
            ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-600/30'
            : 'text-slate-300 hover:bg-white/8 hover:text-white'
        ]"
        :style="{ animationDelay: `${index * 50}ms` }"
      >
        <div v-if="currentPage === item.id" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-white/30 rounded-r-full" />

        <div :class="[
          'w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-200',
          currentPage === item.id ? 'bg-white/20 backdrop-blur-sm' : 'bg-white/5 group-hover:bg-white/10'
        ]">
          <span :class="currentPage === item.id ? 'text-white' : 'text-slate-400 group-hover:text-white'">{{ item.emoji }}</span>
        </div>

        <div class="flex-1 min-w-0">
          <template v-if="isAdmin && editingMenuId === item.id">
            <input
              v-model="editingMenuLabel"
              @blur="saveMenuLabel"
              @keyup.enter="saveMenuLabel"
              @keyup.escape="cancelEditMenu"
              class="font-medium text-sm bg-white/10 border border-white/20 rounded px-2 py-0.5 w-full outline-none focus:border-blue-400"
            />
          </template>
          <div v-else class="flex items-center gap-1" @dblclick.stop>
            <p :class="['font-medium text-sm', currentPage === item.id ? 'text-white' : 'text-slate-200 group-hover:text-white']">
              {{ item.label }}
            </p>
            <button
              v-if="isAdmin"
              @click.stop="startEditMenu(item.id, item.label)"
              class="text-xs opacity-0 group-hover:opacity-50 hover:!opacity-100 text-slate-500 hover:text-blue-400 transition-opacity p-0.5 rounded"
              title="编辑菜单名称（双击也可）">✎</button>
          </div>
          <p class="text-xs text-slate-500 truncate mt-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
            {{ item.description }}
          </p>
        </div>

        <!-- 首页告警角标 -->
        <span v-if="item.id === 'home' && alertCount > 0" class="min-w-[20px] h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center px-1.5 animate-pulse">
          {{ alertCount }}
        </span>

        <div :class="['transition-all duration-200', currentPage === item.id ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-2 group-hover:opacity-50 group-hover:translate-x-0']">
          <span class="text-sm">›</span>
        </div>
      </button>
    </nav>

    <!-- 底部用户区域 -->
    <div class="p-4 border-t border-white/5 relative z-10 bg-gradient-to-b from-transparent to-[#1a1f2e]">
      <!-- 快捷统计 -->
      <div class="bg-white/5 backdrop-blur-sm rounded-xl p-3 mb-3">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">今日概览</span>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-white/5 rounded-lg p-2 text-center">
            <p class="text-lg font-bold text-white">{{ stats.pendingTasks }}</p>
            <p class="text-[10px] text-slate-400">待办任务</p>
          </div>
          <div class="bg-white/5 rounded-lg p-2 text-center">
            <p class="text-lg font-bold text-emerald-400">{{ stats.completionRate }}%</p>
            <p class="text-[10px] text-slate-400">完成率</p>
          </div>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="bg-white/5 backdrop-blur-sm rounded-xl p-3 mb-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 via-cyan-500 to-teal-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-blue-500/20">
            {{ currentUser?.name?.charAt(0) || 'U' }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-sm text-white truncate">{{ currentUser?.name || '未登录' }}</p>
            <p class="text-xs text-slate-400">
              <template v-if="isAdmin">
                <span class="flex items-center gap-1">
                  <span class="text-amber-400 text-xs">✨</span>
                  管理员账号
                </span>
              </template>
              <template v-else>员工账号</template>
            </p>
          </div>
        </div>
      </div>

      <!-- 激励语录 -->
      <div class="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 backdrop-blur-sm rounded-xl p-3 mb-3 border border-blue-500/20">
        <div class="flex items-start gap-2">
          <span class="text-blue-400 text-xs mt-0.5 flex-shrink-0">✨</span>
          <div class="flex-1 min-w-0">
            <template v-if="isEditing">
              <div class="space-y-2">
                <input
                  v-model="editValue"
                  placeholder="输入激励语录"
                  maxlength="50"
                  class="w-full bg-white/10 border border-white/20 text-white text-xs placeholder:text-slate-500 rounded-lg px-2 py-1.5 outline-none"
                  @keyup.enter="saveMotivation"
                />
                <div class="flex gap-2">
                  <button @click="saveMotivation" class="px-3 py-0.5 text-xs bg-blue-500 hover:bg-blue-600 rounded text-white">保存</button>
                  <button @click="cancelEdit" class="px-3 py-0.5 text-xs text-slate-400 hover:text-white hover:bg-white/10 rounded">取消</button>
                </div>
              </div>
            </template>
            <template v-else>
              <p class="text-xs text-slate-300 italic">"{{ motivation }}"</p>
              <div class="flex items-center justify-between mt-1">
                <p class="text-[10px] text-slate-500">— X10增长引擎</p>
                <button v-if="isAdmin" class="w-5 h-5 p-0 text-slate-500 hover:text-blue-400 hover:bg-white/10 rounded flex items-center justify-center" @click="startEdit">
                  <span class="text-[10px]">✎</span>
                </button>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- 退出按钮 -->
      <button
        class="w-full text-slate-400 hover:text-white hover:bg-white/8 justify-start rounded-xl py-2.5 transition-all duration-200 group flex items-center gap-3 px-3"
        @click="handleLogout"
      >
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-white/5 group-hover:bg-white/10 transition-colors">
          <span class="text-sm">🚪</span>
        </div>
        <span class="text-sm font-medium">退出登录</span>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const props = defineProps<{
  currentPage: string
}>()

const emit = defineEmits<{ navigate: [pageId: string] }>()

const router = useRouter()
const authStore = useAuthStore()

function handleNavigate(pageId: string) {
  emit('navigate', pageId)
  router.push({ name: pageId }).catch(() => {})
}

const currentUser = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)

const alertCount = ref(0)
let alertTimer: ReturnType<typeof setInterval> | null = null

async function fetchAlertCount() {
  if (!isAdmin.value) return
  try {
    const res = await api.get('/admin/alerts')
    const data = res.data
    alertCount.value = (data.daily_missing?.length || 0) + (data.weekly_missing?.length || 0) + (data.task_quota_alert?.length || 0)
  } catch {
    // 静默失败，不影响主界面
  }
}

const systemName = ref(localStorage.getItem('sidebar_system_name') || 'X10增长引擎')
const subtitle = ref(localStorage.getItem('sidebar_subtitle') || '让增长可复制')
const editingSystemName = ref(false)
const editSystemNameValue = ref('')
const editingSubtitle = ref(false)
const editSubtitleValue = ref('')

function startEditSystemName() {
  editSystemNameValue.value = systemName.value
  editingSystemName.value = true
}
function saveSystemName() {
  if (editSystemNameValue.value.trim()) {
    systemName.value = editSystemNameValue.value.trim()
    localStorage.setItem('sidebar_system_name', systemName.value)
  }
  editingSystemName.value = false
}

function startEditSubtitle() {
  editSubtitleValue.value = subtitle.value
  editingSubtitle.value = true
}
function saveSubtitle() {
  if (editSubtitleValue.value.trim()) {
    subtitle.value = editSubtitleValue.value.trim()
    localStorage.setItem('sidebar_subtitle', subtitle.value)
  }
  editingSubtitle.value = false
}

const motivation = ref('每天进步一点点，终将成就非凡')

// 菜单分组标题可编辑
const menuSectionTitle = ref(localStorage.getItem('sidebar_section_title') || '核心功能')
const editingSectionTitle = ref(false)
const editSectionValue = ref('')

function saveSectionTitle() {
  if (editSectionValue.value.trim()) {
    menuSectionTitle.value = editSectionValue.value.trim()
    localStorage.setItem('sidebar_section_title', menuSectionTitle.value)
  }
  editingSectionTitle.value = false
}
const isEditing = ref(false)
const editValue = ref('')

const stats = ref({ pendingTasks: 0, completionRate: 0 })

// 侧边栏菜单可编辑（管理员权限）
const DEFAULT_MENU_ITEMS = [
  { id: 'home', label: '首页', emoji: '🏠', description: '控制台与数据概览' },
  { id: 'calendar', label: 'X10成长日程', emoji: '📅', description: '查看和管理每日任务' },
  { id: 'reports', label: 'X10成长复盘', emoji: '📝', description: '每日复盘/每周复盘/月度复盘' },
  { id: 'influencer-list', label: '达人合作台账', emoji: '📊', description: '管理达人合作记录' },
  { id: 'darensource', label: '达人资源库', emoji: '🗄', description: '资源录入/查询/统计' },
  { id: 'consensus-archive', label: '共识档案', emoji: '📖', description: '会议纪要与共识管理' },
  { id: 'training', label: 'X10成长中心', emoji: '🎓', description: '知识库与BD自查手册' },
  { id: 'settings', label: '设置', emoji: '⚙', description: '系统设置' }
]

function loadMenuItems(): any[] {
  const saved = localStorage.getItem('sidebar_menu_items')
  if (saved) {
    try { return JSON.parse(saved) } catch {}
  }
  return [...DEFAULT_MENU_ITEMS]
}

const menuItems = ref(loadMenuItems())
const editingMenuId = ref<string | null>(null)
const editingMenuLabel = ref('')

function startEditMenu(id: string, currentLabel: string) {
  editingMenuId.value = id
  editingMenuLabel.value = currentLabel
}

function saveMenuLabel() {
  if (!editingMenuLabel.value.trim()) return
  const idx = menuItems.value.findIndex(m => m.id === editingMenuId.value)
  if (idx >= 0) {
    menuItems.value[idx].label = editingMenuLabel.value.trim()
    localStorage.setItem('sidebar_menu_items', JSON.stringify(menuItems.value))
  }
  editingMenuId.value = null
}

function cancelEditMenu() {
  editingMenuId.value = null
}

function startEdit() {
  editValue.value = motivation.value
  isEditing.value = true
}

function saveMotivation() {
  if (editValue.value.trim()) {
    motivation.value = editValue.value.trim()
    localStorage.setItem('motivation_quote', editValue.value.trim())
  }
  isEditing.value = false
  editValue.value = ''
}

function cancelEdit() {
  isEditing.value = false
  editValue.value = ''
}

function handleLogout() {
  authStore.logout()
}

onMounted(() => {
  const saved = localStorage.getItem('motivation_quote')
  if (saved) motivation.value = saved
  fetchAlertCount()
  alertTimer = setInterval(fetchAlertCount, 60000) // 每分钟刷新
})

onUnmounted(() => {
  if (alertTimer) {
    clearInterval(alertTimer)
    alertTimer = null
  }
})
</script>
