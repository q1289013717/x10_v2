<template>
  <AppLayout current-page="reports" :show-back="true">
    <template #title>
      <div class="flex items-center gap-2">
        <h1 class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight truncate">报告详情</h1>
        <span :class="['px-2 py-0.5 rounded text-xs font-medium', typeStyle.color]">{{ typeStyle.label }}</span>
      </div>
    </template>
    <template #actions>
      <button v-if="isOwner" @click="$router.push({ path: '/report-edit', query: { id: report.id } })" class="p-2 hover:bg-slate-100 rounded-lg text-slate-500" title="编辑">✎</button>
      <button v-if="isOwner" @click="showDeleteDialog = true" class="p-2 hover:bg-red-50 rounded-lg text-red-500" title="删除">🗑</button>
    </template>

    <div v-if="loading" class="flex items-center justify-center min-h-[50vh]">
      <div class="text-center"><div class="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4" /><p class="text-slate-500">加载中...</p></div>
    </div>

    <div v-else-if="!report" class="flex items-center justify-center min-h-[50vh]">
      <div class="text-center"><span class="text-5xl text-slate-300 block mb-4">📄</span><p class="text-slate-500 mb-4">报告不存在或已被删除</p><button @click="$router.back()" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm">← 返回列表</button></div>
    </div>

    <main v-else class="max-w-6xl mx-auto p-4 lg:p-6 pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <div :class="['rounded-xl p-4 shadow-sm', approvalBg]">
            <div class="flex items-center gap-3"><span class="text-2xl">{{ approvalEmoji }}</span><div><p class="font-bold">{{ approvalLabel }}</p><p class="text-sm opacity-80">{{ approvalDesc }}</p></div></div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="flex items-start gap-4">
              <div :class="['w-16 h-16 rounded-2xl flex items-center justify-center', typeStyle.color]"><span class="text-3xl">📄</span></div>
              <div class="flex-1">
                <h2 class="text-2xl font-bold text-slate-800">{{ report.title }}</h2>
                <p class="text-slate-500 mt-2">{{ report.summary }}</p>
                <div class="flex flex-wrap items-center gap-4 mt-4 text-sm text-slate-500">
                  <span>👤 {{ report.author }}</span><span>🏢 {{ report.department || '未分配' }}</span><span>⏰ {{ report.period }}</span>
                </div>
                <div v-if="report.approver" class="flex items-center gap-4 mt-3 pt-3 border-t border-slate-100 text-sm"><span class="text-emerald-600">🛡 批复人: {{ report.approver }}</span><span class="text-xs text-slate-400">{{ formatDate(report.approvedAt) }}</span></div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-4">
            <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2"><span class="text-emerald-600">✅</span> 工作内容</h3>
            <div class="space-y-3">
              <div v-for="(item, idx) in report.workItems" :key="item.id || idx" class="flex items-start gap-4 p-4 bg-slate-50 rounded-xl">
                <div class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm flex-shrink-0">{{ Number(idx) + 1 }}</div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1"><span class="text-xs bg-slate-200 rounded px-1.5 py-0.5">{{ item.type || '其他' }}</span><span class="text-xs text-slate-500">⏰ {{ item.duration }}小时</span></div>
                  <p class="text-slate-700">{{ item.content }}</p>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-slate-200"><p class="text-sm text-slate-500">总工作时长: <span class="font-medium text-slate-700">{{ totalHours }}小时</span></p></div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-4 space-y-6">
            <h3 class="font-bold text-slate-800 flex items-center gap-2"><span class="text-amber-600">📄</span> 总结与计划</h3>
            <div v-if="report.achievements"><div class="flex items-center gap-2 mb-2"><span class="text-emerald-500">✅</span><h4 class="font-medium text-slate-800">主要成果</h4></div><p class="text-slate-600 bg-emerald-50 p-4 rounded-xl">{{ report.achievements }}</p></div>
            <div v-if="report.problems"><div class="flex items-center gap-2 mb-2"><span class="text-amber-500">⚠</span><h4 class="font-medium text-slate-800">存在问题</h4></div><p class="text-slate-600 bg-amber-50 p-4 rounded-xl">{{ report.problems }}</p></div>
            <div v-if="report.plans"><div class="flex items-center gap-2 mb-2"><span class="text-blue-500">📅</span><h4 class="font-medium text-slate-800">下阶段计划</h4></div><p class="text-slate-600 bg-blue-50 p-4 rounded-xl">{{ report.plans }}</p></div>
          </div>

          <div v-if="report.approvalComments && report.approvalComments.length" class="bg-white rounded-xl shadow-sm p-4">
            <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2"><span class="text-blue-600">💬</span> 批复记录</h3>
            <div class="space-y-4">
              <div v-for="c in report.approvalComments" :key="c.id" class="flex items-start gap-3 p-4 bg-slate-50 rounded-xl">
                <div :class="['w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0', c.type === 'approved' ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600']"><span>{{ c.type === 'approved' ? '✅' : '✕' }}</span></div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1"><span class="font-medium text-slate-800">{{ c.createdBy }}</span><span :class="['text-xs px-1.5 py-0.5 rounded', c.type === 'approved' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">{{ c.type === 'approved' ? '通过' : '驳回' }}</span><span class="text-xs text-slate-400">{{ formatDate(c.createdAt) }}</span></div>
                  <p class="text-slate-600">{{ c.content }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="canApprove" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow-sm p-6">
            <div class="flex items-center gap-3 mb-4"><span class="text-blue-600 text-xl">🛡</span><div><h3 class="font-bold text-slate-800">管理者批复</h3><p class="text-sm text-slate-500">请审核此工作报告并给出批复意见</p></div></div>
            <div class="flex gap-3">
              <button @click="openApproval('approved')" class="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm">✅ 通过报告</button>
              <button @click="openApproval('rejected')" class="flex-1 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm">✕ 驳回报告</button>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="bg-white rounded-xl shadow-sm p-4">
            <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2"><span class="text-purple-600">🎯</span> 业绩数据</h3>
            <div class="space-y-4">
              <div class="p-4 bg-slate-50 rounded-xl"><p class="text-sm text-slate-500 mb-1">目标金额</p><p class="text-2xl font-bold text-slate-800">{{ report.data?.targetAmount || 0 }}万</p></div>
              <div class="p-4 bg-emerald-50 rounded-xl"><p class="text-sm text-emerald-600 mb-1">完成金额</p><p class="text-2xl font-bold text-emerald-700">{{ report.data?.completedAmount || 0 }}万</p></div>
              <div class="p-4 bg-blue-50 rounded-xl"><p class="text-sm text-blue-600 mb-1">达成率</p>
                <p :class="['text-2xl font-bold', completionRate >= 100 ? 'text-emerald-600' : completionRate >= 80 ? 'text-amber-600' : 'text-red-600']">{{ completionRate }}%</p>
                <div class="mt-2 h-2 bg-slate-200 rounded-full overflow-hidden"><div :class="['h-full rounded-full', completionRate >= 100 ? 'bg-emerald-500' : completionRate >= 80 ? 'bg-amber-500' : 'bg-red-500']" :style="{ width: Math.min(completionRate, 100) + '%' }" /></div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="p-3 bg-slate-50 rounded-xl text-center"><span class="text-2xl block mb-1">👥</span><p class="text-lg font-bold text-slate-800">{{ report.data?.customerCount || 0 }}</p><p class="text-xs text-slate-500">客户总数</p></div>
                <div class="p-3 bg-slate-50 rounded-xl text-center"><span class="text-2xl block mb-1">📈</span><p class="text-lg font-bold text-emerald-600">+{{ report.data?.newCustomerCount || 0 }}</p><p class="text-xs text-slate-500">新增客户</p></div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-4">
            <h3 class="font-bold text-slate-800 mb-4">报告信息</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between"><span class="text-slate-500">提交人</span><span class="text-slate-800">{{ report.author }}</span></div>
              <div class="flex justify-between"><span class="text-slate-500">所属部门</span><span class="text-slate-800">{{ report.department || '未分配' }}</span></div>
              <div class="flex justify-between"><span class="text-slate-500">报告类型</span><span :class="['px-2 py-0.5 rounded text-xs font-medium', typeStyle.color]">{{ typeStyle.label }}</span></div>
              <div class="flex justify-between"><span class="text-slate-500">批复状态</span><span :class="['px-2 py-0.5 rounded text-xs font-medium', approvalStyle.color]">{{ approvalStyle.label }}</span></div>
              <div class="flex justify-between"><span class="text-slate-500">报告周期</span><span class="text-slate-800">{{ report.period }}</span></div>
              <div class="flex justify-between"><span class="text-slate-500">提交时间</span><span class="text-slate-800">{{ formatDate(report.createdAt) }}</span></div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 删除确认 -->
    <Teleport to="body">
      <div v-if="showDeleteDialog" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showDeleteDialog = false">
        <div class="bg-white rounded-xl shadow-xl max-w-sm w-full p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-2">确认删除</h3>
          <p class="text-slate-500 text-sm mb-4">确定要删除这份报告吗？此操作无法撤销。</p>
          <div class="flex gap-3"><button @click="showDeleteDialog = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="handleDelete" class="flex-1 py-2.5 bg-red-600 text-white rounded-xl text-sm">🗑 删除</button></div>
        </div>
      </div>
    </Teleport>

    <!-- 批复对话框 -->
    <Teleport to="body">
      <div v-if="showApprovalDialog" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showApprovalDialog = false">
        <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-2 flex items-center gap-2"><span v-if="approvalAction === 'approved'">✅ 通过报告</span><span v-else>✕ 驳回报告</span></h3>
          <p class="text-slate-500 text-sm mb-4">{{ report?.title }}</p>
          <label class="text-sm font-medium text-slate-700 mb-2 block">批复意见</label>
          <textarea v-model="approvalComment" :placeholder="approvalAction === 'approved' ? '请输入通过意见（可选）' : '请输入驳回原因（必填）'" rows="4" class="w-full p-3 border border-slate-200 rounded-xl outline-none resize-none text-sm" />
          <div class="flex gap-3 mt-4">
            <button @click="showApprovalDialog = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button>
            <button @click="submitApproval" :disabled="approvalAction === 'rejected' && !approvalComment.trim()" :class="['flex-1 py-2.5 text-white rounded-xl text-sm disabled:opacity-50', approvalAction === 'approved' ? 'bg-emerald-600' : 'bg-emerald-700']">✅ 确认通过</button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const reportId = route.query.id as string

const report = ref<any>(null)
const loading = ref(true)
const showDeleteDialog = ref(false)
const showApprovalDialog = ref(false)
const approvalAction = ref('')
const approvalComment = ref('')

const isManager = computed(() => authStore.isAdmin)
const isOwner = computed(() => report.value && (authStore.user?.id === report.value.authorId || authStore.user?.name === report.value.author))
const canApprove = computed(() => isManager.value && report.value?.approvalStatus === 'pending')

const typeStyle = computed(() => {
  const map: any = { daily: { label: '日报', color: 'bg-blue-100 text-blue-700' }, weekly: { label: '周报', color: 'bg-emerald-100 text-emerald-700' }, monthly: { label: '月报', color: 'bg-purple-100 text-purple-700' } }
  return map[report.value?.type] || map.daily
})

const approvalMap: any = {
  pending: { label: '待批复', color: 'bg-amber-100 text-amber-700', bg: 'bg-amber-50', emoji: '⏰', desc: '报告已提交，等待管理者审核' },
  approved: { label: '已通过', color: 'bg-emerald-100 text-emerald-700', bg: 'bg-emerald-50', emoji: '✅', desc: '报告已通过审核' },
  rejected: { label: '已驳回', color: 'bg-red-100 text-red-700', bg: 'bg-red-50', emoji: '✕', desc: '报告已被驳回，请修改后重新提交' }
}
const approvalStyle = computed(() => approvalMap[report.value?.approvalStatus] || approvalMap.pending)
const approvalBg = computed(() => approvalStyle.value.bg)
const approvalEmoji = computed(() => approvalStyle.value.emoji)
const approvalLabel = computed(() => approvalStyle.value.label)
const approvalDesc = computed(() => approvalStyle.value.desc)

const completionRate = computed(() => {
  if (!report.value?.data?.targetAmount) return 0
  return Math.round(report.value.data.completedAmount / report.value.data.targetAmount * 100)
})

const totalHours = computed(() => {
  if (!report.value?.workItems) return 0
  return report.value.workItems.reduce((sum: number, item: any) => sum + (parseFloat(item.duration) || 0), 0)
})

function formatDate(d: string) { if (!d) return ''; return new Date(d).toLocaleString() }

function openApproval(action: string) { approvalAction.value = action; approvalComment.value = ''; showApprovalDialog.value = true }

async function submitApproval() {
  if (!report.value) return
  try {
    await api.put(`/reports/${report.value.id}`, {
      approvalStatus: approvalAction.value,
      approver: authStore.user?.name,
      approvalComment: approvalComment.value || (approvalAction.value === 'approved' ? '已通过' : '已驳回')
    })
    report.value.approvalStatus = approvalAction.value
    report.value.approver = authStore.user?.name
    if (!report.value.approvalComments) report.value.approvalComments = []
    report.value.approvalComments.push({ id: Date.now(), type: approvalAction.value, content: approvalComment.value, createdBy: authStore.user?.name, createdAt: new Date().toISOString() })
    showApprovalDialog.value = false
  } catch (e) { console.error('批复失败:', e) }
}

async function handleDelete() {
  try {
    await api.delete(`/reports/${report.value.id}`)
    showDeleteDialog.value = false
    router.back()
  } catch (e) { console.error('删除失败:', e) }
}

onMounted(async () => {
  if (!reportId) { router.back(); return }
  try {
    const res = await api.get(`/reports/${reportId}`)
    report.value = res.data
  } catch (e) { console.error('加载报告详情失败:', e) }
  loading.value = false
})
</script>
