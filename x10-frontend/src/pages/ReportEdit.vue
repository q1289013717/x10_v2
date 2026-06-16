<template>
  <AppLayout current-page="reports" :show-back="true">
    <template #title>
      <h1 class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight truncate">{{ editId ? '编辑报告' : '填写报告' }}</h1>
      <p class="text-xs text-slate-400 mt-0.5 truncate flex items-center gap-1">🏢 {{ currentUser }}</p>
    </template>
    <template #actions>
      <button @click="handleSubmit" :disabled="loading" class="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-5 py-2.5 text-sm font-medium disabled:opacity-50">
        <template v-if="loading"><span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block mr-2" />保存中...</template>
        <template v-else>💾 {{ editId ? '更新' : '提交' }}</template>
      </button>
    </template>

    <main class="max-w-4xl mx-auto p-4 lg:p-6 pb-24">
      <div class="space-y-6">
        <!-- 报告类型 -->
        <div v-if="!editId" class="bg-white rounded-xl shadow-sm p-4">
          <label class="text-sm font-medium text-slate-700 mb-3 block">报告类型</label>
          <div class="grid grid-cols-3 gap-3">
            <button v-for="t in typeList" :key="t.value" @click="reportType = t.value" :class="['flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all', reportType === t.value ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-slate-300']">
              <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', t.color]"><span>{{ t.icon }}</span></div>
              <span :class="['font-medium', reportType === t.value ? 'text-blue-700' : 'text-slate-600']">{{ t.label }}</span>
            </button>
          </div>
        </div>

        <!-- 基本信息 -->
        <div class="bg-white rounded-xl shadow-sm p-4 space-y-4">
          <div class="flex items-center gap-2 mb-2"><span class="text-blue-600">📄</span><h2 class="font-bold text-slate-800">{{ typeLabel }}信息</h2><span class="px-2 py-0.5 rounded text-xs bg-blue-100 text-blue-700">{{ getPeriodLabel() }}</span></div>
          <div>
            <label class="text-sm font-medium text-slate-700 mb-2 block">报告标题 <span class="text-red-500">*</span></label>
            <input v-model="title" :placeholder="`请输入${typeLabel}标题`" class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none text-sm" />
          </div>
          <div>
            <label class="text-sm font-medium text-slate-700 mb-2 block">报告日期</label>
            <input v-model="date" type="date" class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-blue-500 outline-none text-sm" />
          </div>
        </div>

        <!-- 工作内容 -->
        <div class="bg-white rounded-xl shadow-sm p-4">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2"><span class="text-emerald-600">✅</span><h2 class="font-bold text-slate-800">工作内容</h2></div>
            <button @click="addWorkItem" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm hover:bg-slate-50">+ 添加工作项</button>
          </div>
          <div class="space-y-3">
            <div v-for="(item, idx) in workItems" :key="item.id" class="p-4 bg-slate-50 rounded-xl space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-slate-600">工作项 {{ idx + 1 }}</span>
                <button v-if="workItems.length > 1" @click="removeWorkItem(item.id)" class="text-red-500 text-sm hover:text-red-600">删除</button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <select v-model="item.type" class="h-10 px-3 rounded-lg border border-slate-200 bg-white text-sm outline-none">
                  <option value="">工作类型</option>
                  <option v-for="w in workTypes" :key="w.value" :value="w.value">{{ w.label }}</option>
                </select>
                <input v-model="item.duration" type="number" step="0.5" placeholder="工作时长（小时）" class="h-10 px-3 rounded-lg border border-slate-200 bg-white text-sm outline-none" />
                <input v-model="item.content" placeholder="工作内容描述" class="h-10 px-3 rounded-lg border border-slate-200 bg-white text-sm outline-none md:col-span-3" />
              </div>
            </div>
          </div>
        </div>

        <!-- 数据指标 -->
        <div class="bg-white rounded-xl shadow-sm p-4">
          <div class="flex items-center gap-2 mb-4"><span class="text-purple-600">🎯</span><h2 class="font-bold text-slate-800">业绩数据</h2></div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label class="text-sm font-medium text-slate-700 mb-2 block">目标金额（万元）</label><input v-model="targetAmount" type="number" placeholder="0.00" class="w-full h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" /></div>
            <div><label class="text-sm font-medium text-slate-700 mb-2 block">完成金额（万元）</label><input v-model="completedAmount" type="number" placeholder="0.00" class="w-full h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" /></div>
            <div><label class="text-sm font-medium text-slate-700 mb-2 block">客户总数</label><input v-model="customerCount" type="number" placeholder="0" class="w-full h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" /></div>
            <div><label class="text-sm font-medium text-slate-700 mb-2 block">新增客户数</label><input v-model="newCustomerCount" type="number" placeholder="0" class="w-full h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" /></div>
          </div>
        </div>

        <!-- 总结与计划 -->
        <div class="bg-white rounded-xl shadow-sm p-4 space-y-4">
          <div class="flex items-center gap-2 mb-2"><span class="text-amber-600">📄</span><h2 class="font-bold text-slate-800">总结与计划</h2></div>
          <div>
            <div class="flex items-center justify-between mb-1">
              <div class="flex items-center gap-2">
                <template v-if="editingTitle === 'summary'">
                  <input v-model="sectionTitles.summary" @blur="editingTitle = ''" @keyup.enter="editingTitle = ''" class="text-sm font-medium text-slate-700 px-2 py-0.5 rounded border border-blue-300 outline-none focus:border-blue-500" ref="titleInputRef" />
                </template>
                <template v-else>
                  <span class="text-sm font-medium text-slate-700">{{ sectionTitles.summary }} <span class="text-red-500">*</span></span>
                  <button @click="startEditTitle('summary')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改标题">✎</button>
                </template>
              </div>
              <span :class="['text-xs px-2 py-0.5 rounded-full', summaryLen >= 50 ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-600']">
                {{ summaryLen }} / 50字
              </span>
            </div>
            <div class="flex items-center gap-2 mb-2">
              <template v-if="editingPlaceholder === 'summary'">
                <input v-model="sectionPlaceholders.summary" @blur="editingPlaceholder = ''" @keyup.enter="editingPlaceholder = ''" class="flex-1 text-xs text-slate-400 px-2 py-0.5 rounded border border-slate-200 outline-none focus:border-blue-400" placeholder="提示文本..." />
              </template>
              <template v-else>
                <span class="text-xs text-slate-400 italic">{{ sectionPlaceholders.summary }}</span>
                <button @click="startEditPlaceholder('summary')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改提示文本">✎</button>
              </template>
            </div>
            <textarea v-model="summary" :placeholder="sectionPlaceholders.summary" rows="4" :class="['w-full p-3 rounded-xl border resize-none outline-none text-sm', summaryLen > 0 && summaryLen < 50 ? 'border-red-300 bg-red-50' : 'border-slate-200 bg-slate-50']" /></div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <template v-if="editingTitle === 'achievements'">
                <input v-model="sectionTitles.achievements" @blur="editingTitle = ''" @keyup.enter="editingTitle = ''" class="text-sm font-medium text-slate-700 px-2 py-0.5 rounded border border-blue-300 outline-none focus:border-blue-500" />
              </template>
              <template v-else>
                <span class="text-sm font-medium text-slate-700">{{ sectionTitles.achievements }}</span>
                <button @click="startEditTitle('achievements')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改标题">✎</button>
              </template>
            </div>
            <div class="flex items-center gap-2 mb-2">
              <template v-if="editingPlaceholder === 'achievements'">
                <input v-model="sectionPlaceholders.achievements" @blur="editingPlaceholder = ''" @keyup.enter="editingPlaceholder = ''" class="flex-1 text-xs text-slate-400 px-2 py-0.5 rounded border border-slate-200 outline-none focus:border-blue-400" placeholder="提示文本..." />
              </template>
              <template v-else>
                <span class="text-xs text-slate-400 italic">{{ sectionPlaceholders.achievements }}</span>
                <button @click="startEditPlaceholder('achievements')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改提示文本">✎</button>
              </template>
            </div>
            <textarea v-model="achievements" :placeholder="sectionPlaceholders.achievements" rows="3" class="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 resize-none outline-none text-sm" /></div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <template v-if="editingTitle === 'problems'">
                <input v-model="sectionTitles.problems" @blur="editingTitle = ''" @keyup.enter="editingTitle = ''" class="text-sm font-medium text-slate-700 px-2 py-0.5 rounded border border-blue-300 outline-none focus:border-blue-500" />
              </template>
              <template v-else>
                <span class="text-sm font-medium text-slate-700">{{ sectionTitles.problems }}</span>
                <button @click="startEditTitle('problems')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改标题">✎</button>
              </template>
            </div>
            <div class="flex items-center gap-2 mb-2">
              <template v-if="editingPlaceholder === 'problems'">
                <input v-model="sectionPlaceholders.problems" @blur="editingPlaceholder = ''" @keyup.enter="editingPlaceholder = ''" class="flex-1 text-xs text-slate-400 px-2 py-0.5 rounded border border-slate-200 outline-none focus:border-blue-400" placeholder="提示文本..." />
              </template>
              <template v-else>
                <span class="text-xs text-slate-400 italic">{{ sectionPlaceholders.problems }}</span>
                <button @click="startEditPlaceholder('problems')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改提示文本">✎</button>
              </template>
            </div>
            <textarea v-model="problems" :placeholder="sectionPlaceholders.problems" rows="3" class="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 resize-none outline-none text-sm" /></div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <template v-if="editingTitle === 'plans'">
                <input v-model="sectionTitles.plans" @blur="editingTitle = ''" @keyup.enter="editingTitle = ''" class="text-sm font-medium text-slate-700 px-2 py-0.5 rounded border border-blue-300 outline-none focus:border-blue-500" />
              </template>
              <template v-else>
                <span class="text-sm font-medium text-slate-700">{{ sectionTitles.plans }}</span>
                <button @click="startEditTitle('plans')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改标题">✎</button>
              </template>
            </div>
            <div class="flex items-center gap-2 mb-2">
              <template v-if="editingPlaceholder === 'plans'">
                <input v-model="sectionPlaceholders.plans" @blur="editingPlaceholder = ''" @keyup.enter="editingPlaceholder = ''" class="flex-1 text-xs text-slate-400 px-2 py-0.5 rounded border border-slate-200 outline-none focus:border-blue-400" placeholder="提示文本..." />
              </template>
              <template v-else>
                <span class="text-xs text-slate-400 italic">{{ sectionPlaceholders.plans }}</span>
                <button @click="startEditPlaceholder('plans')" class="text-slate-300 hover:text-blue-500 text-xs" title="修改提示文本">✎</button>
              </template>
            </div>
            <textarea v-model="plans" :placeholder="sectionPlaceholders.plans" rows="3" class="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 resize-none outline-none text-sm" /></div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-4">
          <button @click="$router.back()" class="flex-1 h-12 border border-slate-200 rounded-xl hover:bg-slate-50 text-sm">取消</button>
          <button @click="handleSubmit" :disabled="loading" class="flex-1 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-medium disabled:opacity-50">💾 保存报告</button>
        </div>
      </div>
    </main>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const editId = ref(route.query.id as string || null)
const reportType = ref((route.query.type as string) || 'daily')
const loading = ref(false)
const title = ref('')
const date = ref(new Date().toISOString().split('T')[0])
const summary = ref('')
const achievements = ref('')
const problems = ref('')
const plans = ref('')

// 可编辑的标题
const DEFAULT_TITLES = { summary: '工作总结', achievements: '主要成果', problems: '存在问题', plans: '下阶段计划' }
const sectionTitles = ref({ ...DEFAULT_TITLES })
const editingTitle = ref('')

function startEditTitle(key: string) {
  editingTitle.value = key
}

// 从 localStorage 读取自定义标题
const savedTitles = localStorage.getItem('report_section_titles')
if (savedTitles) { try { sectionTitles.value = { ...DEFAULT_TITLES, ...JSON.parse(savedTitles) } } catch {} }

// 监听标题变化并保存
watch(sectionTitles, (val) => { localStorage.setItem('report_section_titles', JSON.stringify(val)) }, { deep: true })

// 可编辑的提示文本
const DEFAULT_PLACEHOLDERS = {
  summary: '请总结本期的主要工作内容（至少50字）',
  achievements: '请描述取得的主要成绩和亮点',
  problems: '请描述遇到的问题和困难',
  plans: '请描述下阶段的工作计划'
}
const sectionPlaceholders = ref({ ...DEFAULT_PLACEHOLDERS })
const editingPlaceholder = ref('')

function startEditPlaceholder(key: string) {
  editingPlaceholder.value = key
}

// 从 localStorage 读取自定义提示
const savedPlaceholders = localStorage.getItem('report_section_placeholders')
if (savedPlaceholders) { try { sectionPlaceholders.value = { ...DEFAULT_PLACEHOLDERS, ...JSON.parse(savedPlaceholders) } } catch {} }

// 监听提示变化并保存
watch(sectionPlaceholders, (val) => { localStorage.setItem('report_section_placeholders', JSON.stringify(val)) }, { deep: true })
const targetAmount = ref('')
const completedAmount = ref('')
const customerCount = ref('')
const newCustomerCount = ref('')

const workItems = ref([{ id: 1, type: '', content: '', duration: '' }])
const workTypes = ref([
  { value: 'sales', label: '销售拜访' },
  { value: 'meeting', label: '会议' },
  { value: 'customer', label: '客户维护' },
  { value: 'document', label: '文档处理' },
  { value: 'training', label: '培训学习' },
  { value: 'other', label: '其他' }
])

const typeList = [
  { value: 'daily', label: '日报', icon: '📅', color: 'bg-blue-100 text-blue-700' },
  { value: 'weekly', label: '周报', icon: '📊', color: 'bg-emerald-100 text-emerald-700' },
  { value: 'monthly', label: '月报', icon: '📈', color: 'bg-purple-100 text-purple-700' }
]

const typeLabel = computed(() => typeList.find(t => t.value === reportType.value)?.label || '日报')
const currentUser = computed(() => authStore.user?.name || '未知用户')
const summaryLen = computed(() => summary.value.replace(/\s/g, '').length)

function getPeriodLabel() {
  const d = new Date(date.value)
  if (reportType.value === 'weekly') return `${date.value} 本周`
  if (reportType.value === 'monthly') return `${d.getFullYear()}年${d.getMonth() + 1}月`
  return date.value
}

function addWorkItem() { workItems.value.push({ id: Date.now(), type: '', content: '', duration: '' }) }
function removeWorkItem(id: number) { if (workItems.value.length > 1) workItems.value = workItems.value.filter(i => i.id !== id) }

async function handleSubmit() {
  if (!title.value.trim()) { alert('请填写报告标题'); return }
  if (summaryLen.value < 50) { alert(`工作总结至少需要50字，当前仅${summaryLen.value}字`); return }
  const validItems = workItems.value.filter(i => i.content.trim())
  if (validItems.length === 0) { alert('请至少添加一项工作内容'); return }

  loading.value = true
  try {
    const data = {
      type: reportType.value,
      title: title.value,
      date: date.value,
      period: getPeriodLabel(),
      summary: summary.value,
      achievements: achievements.value,
      problems: problems.value,
      plans: plans.value,
      work_items: JSON.stringify(validItems),
      target_amount: targetAmount.value || '0',
      completed_amount: completedAmount.value || '0',
      customer_count: customerCount.value || '0',
      new_customer_count: newCustomerCount.value || '0',
      department: '销售部',
      status: 'submitted',
      approval_status: 'pending',
    }

    if (editId.value) {
      await api.put(`/reports/${editId.value}`, data)
    } else {
      await api.post('/reports', data)
    }
    router.back()
  } catch (e: any) {
    alert(e.response?.data?.detail || '保存失败')
  } finally { loading.value = false }
}

onMounted(async () => {
  if (editId.value) {
    try {
      const res = await api.get(`/reports/${editId.value}`)
      if (res.data) {
        const r = res.data
        title.value = r.title; date.value = r.date; summary.value = r.summary || ''
        achievements.value = r.achievements || ''; problems.value = r.problems || ''; plans.value = r.plans || ''
        targetAmount.value = r.data?.targetAmount || ''; completedAmount.value = r.data?.completedAmount || ''
        customerCount.value = r.data?.customerCount || ''; newCustomerCount.value = r.data?.newCustomerCount || ''
        if (r.workItems) workItems.value = r.workItems
        reportType.value = r.type
      }
    } catch (e) { console.error('加载报告失败:', e) }
  }
})
</script>
