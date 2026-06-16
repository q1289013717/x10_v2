<template>
  <AppLayout current-page="reports" :title="pageTitle" :title-editable="true" @update:title="onTitleUpdate" :subtitle="pageSubtitle" :subtitle-editable="true" @update:subtitle="onSubtitleUpdate">
    <template #actions>
      <button v-if="isManager" @click="showTypeModal = true" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm hover:bg-slate-50 flex items-center gap-1">
        ✎ 管理类型
      </button>
      <button v-for="t in reportTypes.filter((x: any) => x.value !== 'all').slice(0, 2)" :key="t.value" @click="$router.push({ path: '/report-edit', query: { type: t.value } })" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm hover:bg-slate-50 flex items-center gap-1">
        + {{ t.label }}
      </button>
    </template>

    <div class="max-w-6xl mx-auto p-4 lg:p-6 pb-24">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow" @click="filterApprovalStatus = 'all'">
          <div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">📄</div><div><p class="text-2xl font-bold text-slate-800">{{ stats.total }}</p><p class="text-xs text-slate-500">全部报告</p></div></div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow" @click="filterApprovalStatus = 'pending'">
          <div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center text-amber-700">⏰</div><div><p class="text-2xl font-bold text-slate-800">{{ stats.pending }}</p><p class="text-xs text-slate-500">待批复</p></div></div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow" @click="filterApprovalStatus = 'approved'">
          <div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center text-emerald-700">✅</div><div><p class="text-2xl font-bold text-slate-800">{{ stats.approved }}</p><p class="text-xs text-slate-500">已通过</p></div></div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow" @click="filterApprovalStatus = 'rejected'">
          <div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center text-red-700">✕</div><div><p class="text-2xl font-bold text-slate-800">{{ stats.rejected }}</p><p class="text-xs text-slate-500">已驳回</p></div></div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
        <div class="flex flex-col md:flex-row gap-3">
          <div class="relative flex-1">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
            <input v-model="searchQuery" placeholder="搜索报告标题、作者..." class="w-full pl-9 pr-4 h-11 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 text-sm" />
          </div>
          <select v-if="isManager" v-model="filterDepartment" class="w-full md:w-40 h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-sm outline-none">
            <option value="all">全部部门</option>
            <option v-for="d in departments.filter((x: string) => x !== 'all')" :key="d" :value="d">{{ d }}</option>
          </select>
          <select v-model="filterApprovalStatus" class="w-full md:w-40 h-11 bg-slate-50 border border-slate-200 rounded-xl px-3 text-sm outline-none">
            <option value="all">全部状态</option>
            <option value="pending">待批复</option>
            <option value="approved">已通过</option>
            <option value="rejected">已驳回</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-4 md:w-fit bg-slate-50 rounded-xl p-1 mb-6">
        <button v-for="t in reportTypes" :key="t.value" @click="activeTab = t.value" :class="['rounded-lg px-4 py-2 text-sm font-medium transition-all flex items-center gap-1', activeTab === t.value ? 'bg-white shadow-sm text-slate-900' : 'text-slate-500 hover:text-slate-700']">
          <span>📄</span> {{ t.label }}
        </button>
      </div>

      <div class="space-y-4">
        <div v-if="filteredReports.length === 0" class="bg-white rounded-xl shadow-sm p-12 text-center">
          <span class="text-5xl text-slate-300 block mb-4">📄</span>
          <p class="text-slate-500 mb-4">暂无报告数据</p>
          <button @click="$router.push({ path: '/report-edit', query: { type: 'daily' } })" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm">+ 创建第一份报告</button>
        </div>
        <div v-for="report in filteredReports" :key="report.id" class="bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-shadow">
          <div class="flex items-start gap-4">
            <div :class="['w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0', getTypeStyle(report.type).color]">
              <span class="text-xl">📄</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <div><h3 class="font-bold text-slate-800 truncate">{{ report.title }}</h3><p class="text-sm text-slate-500 mt-1 line-clamp-2">{{ report.summary }}</p></div>
                <div class="flex flex-col gap-1">
                  <span :class="['px-2 py-0.5 rounded text-xs font-medium', getTypeStyle(report.type).color]">{{ getTypeStyle(report.type).label }}</span>
                  <span :class="['px-2 py-0.5 rounded text-xs font-medium', getApprovalStyle(report.approvalStatus).color]">{{ getApprovalStyle(report.approvalStatus).label }}</span>
                </div>
              </div>
              <div class="flex flex-wrap items-center gap-3 mt-3 text-xs text-slate-500">
                <span>👤 {{ report.author }}</span>
                <span>🏢 {{ report.department || '未分配' }}</span>
                <span>⏰ {{ report.period }}</span>
                <span v-if="report.approver" class="text-emerald-600">✅ 批复人: {{ report.approver }}</span>
              </div>
              <div v-if="report.data" class="flex flex-wrap items-center gap-4 mt-3 pt-3 border-t border-slate-100">
                <span class="text-sm"><span class="text-slate-500">目标:</span><span class="font-medium text-slate-700 ml-1">{{ report.data.targetAmount }}万</span></span>
                <span class="text-sm"><span class="text-slate-500">完成:</span><span class="font-medium text-emerald-600 ml-1">{{ report.data.completedAmount }}万</span></span>
              </div>
              <div class="flex items-center gap-2 mt-3 pt-3 border-t border-slate-100">
                <button @click="$router.push({ path: '/report-detail', query: { id: report.id } })" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm hover:bg-slate-50 flex items-center gap-1">👁 查看</button>
                <template v-if="isManager && report.approvalStatus === 'pending'">
                  <button @click="openApproval(report, 'approved')" class="px-3 py-1.5 border border-emerald-200 text-emerald-600 rounded-lg text-sm hover:bg-emerald-50 flex items-center gap-1">✅ 通过</button>
                  <button @click="openApproval(report, 'rejected')" class="px-3 py-1.5 border border-red-200 text-red-600 rounded-lg text-sm hover:bg-red-50 flex items-center gap-1">✕ 驳回</button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 批复对话框 -->
    <Teleport to="body">
      <div v-if="showApprovalDialog" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showApprovalDialog = false">
        <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-2 flex items-center gap-2">
            <span v-if="approvalAction === 'approved'">✅ 通过报告</span>
            <span v-else>✕ 驳回报告</span>
          </h3>
          <p class="text-slate-500 text-sm mb-4">{{ selectedReport?.title }}</p>
          <label class="text-sm font-medium text-slate-700 mb-2 block">批复意见</label>
          <textarea v-model="approvalComment" :placeholder="approvalAction === 'approved' ? '请输入通过意见（可选）' : '请输入驳回原因（必填）'" rows="4" class="w-full p-3 border border-slate-200 rounded-xl outline-none focus:border-blue-500 resize-none text-sm"></textarea>
          <div class="flex gap-3 mt-4">
            <button @click="showApprovalDialog = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button>
            <button @click="submitApproval" :disabled="approvalAction === 'rejected' && !approvalComment.trim()" :class="['flex-1 py-2.5 text-white rounded-xl text-sm disabled:opacity-50', approvalAction === 'approved' ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-red-600 hover:bg-red-700']">
              <span v-if="approvalAction === 'approved'">✅ 确认通过</span>
              <span v-else>✕ 确认驳回</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
</AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const router = useRouter()
const authStore = useAuthStore()
const isManager = computed(() => authStore.isAdmin)

const activeTab = ref('all')
const searchQuery = ref('')
const filterDepartment = ref('all')
const filterApprovalStatus = ref('all')
const pageTitle = ref('工作报告')
const pageSubtitle = ref('数据报告表格和员工工作日志')
const showTypeModal = ref(false)
const showApprovalDialog = ref(false)
const selectedReport = ref<any>(null)
const approvalAction = ref('')
const approvalComment = ref('')

const reportTypes = ref([
  { value: 'all', label: '全部', color: 'bg-slate-100 text-slate-700' },
  { value: 'daily', label: '每日复盘', color: 'bg-blue-100 text-blue-700' },
  { value: 'weekly', label: '每周复盘', color: 'bg-emerald-100 text-emerald-700' },
  { value: 'monthly', label: '月度复盘', color: 'bg-purple-100 text-purple-700' }
])

const allReports = ref<any[]>([])

const filteredReports = computed(() => {
  let filtered = allReports.value
  if (!isManager.value) {
    const user = authStore.user
    filtered = filtered.filter(r => r.authorId === user?.id || r.author === user?.name)
  }
  if (activeTab.value !== 'all') filtered = filtered.filter(r => r.type === activeTab.value)
  if (filterDepartment.value !== 'all') filtered = filtered.filter(r => r.department === filterDepartment.value)
  if (filterApprovalStatus.value !== 'all') filtered = filtered.filter(r => r.approvalStatus === filterApprovalStatus.value)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter(r => (r.title || '').toLowerCase().includes(q) || (r.author || '').toLowerCase().includes(q) || (r.summary || '').toLowerCase().includes(q))
  }
  return filtered.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const stats = computed(() => {
  let base = allReports.value
  if (!isManager.value) { const u = authStore.user; base = base.filter(r => r.authorId === u?.id || r.author === u?.name) }
  return {
    total: base.length,
    pending: base.filter(r => r.approvalStatus === 'pending').length,
    approved: base.filter(r => r.approvalStatus === 'approved').length,
    rejected: base.filter(r => r.approvalStatus === 'rejected').length
  }
})

const departments = computed(() => ['all', ...new Set(allReports.value.map(r => r.department).filter(Boolean))])

function getTypeStyle(type: string) { return reportTypes.value.find(t => t.value === type) || reportTypes.value[1] }
function getApprovalStyle(status: string) {
  const map: Record<string, any> = {
    pending: { label: '待批复', color: 'bg-amber-100 text-amber-700' },
    approved: { label: '已通过', color: 'bg-emerald-100 text-emerald-700' },
    rejected: { label: '已驳回', color: 'bg-red-100 text-red-700' }
  }
  return map[status] || map.pending
}

function openApproval(report: any, action: string) {
  selectedReport.value = report; approvalAction.value = action; approvalComment.value = ''; showApprovalDialog.value = true
}

async function submitApproval() {
  if (!selectedReport.value) return
  try {
    await api.put(`/reports/${selectedReport.value.id}`, {
      approvalStatus: approvalAction.value,
      approver: authStore.user?.name,
      approvalComment: approvalComment.value || (approvalAction.value === 'approved' ? '已通过' : '已驳回')
    })
    const idx = allReports.value.findIndex(r => r.id === selectedReport.value.id)
    if (idx >= 0) {
      allReports.value[idx] = { ...allReports.value[idx], approvalStatus: approvalAction.value, approver: authStore.user?.name }
    }
    showApprovalDialog.value = false
  } catch (e) { console.error('批复失败:', e) }
}

function onTitleUpdate(newVal: string) {
  pageTitle.value = newVal
}

function onSubtitleUpdate(newVal: string) {
  pageSubtitle.value = newVal
}

async function loadReports() {
  try {
    const res = await api.get('/reports')
    if (res.data && Array.isArray(res.data)) allReports.value = res.data
  } catch (e) { console.error('加载报告失败:', e) }
}

onMounted(() => {
  // 加载自定义标题和副标题
  try {
    const saved = JSON.parse(localStorage.getItem('page_subtitle_reports') || '{}')
    if (saved.customTitle) {
      pageTitle.value = saved.customTitle
    }
    if (saved.customSubtitle) {
      pageSubtitle.value = saved.customSubtitle
    }
  } catch {}
  loadReports()
})
</script>
