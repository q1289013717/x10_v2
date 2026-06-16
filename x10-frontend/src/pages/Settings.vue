<template>
  <AppLayout current-page="settings" title="系统设置" subtitle="系统配置与管理">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <div class="flex gap-2 mb-6">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="['px-4 py-2 rounded-xl text-sm transition-all', activeTab === tab.key ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50']">{{ tab.label }}</button>
      </div>

      <!-- 账号管理 -->
      <div v-if="activeTab === 'accounts'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-4xl">
        <div class="flex items-center justify-between mb-4">
          <h2 class="font-bold text-slate-800">账号管理</h2>
          <button @click="showAccountForm = true" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm">+ 添加账号</button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full"><thead><tr class="border-b border-slate-100"><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">账号</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">姓名</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">角色</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">公司</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">状态</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">操作</th></tr></thead>
            <tbody>
              <tr v-for="a in accounts" :key="a.id" class="border-b border-slate-50"><td class="px-4 py-3 text-sm font-medium">{{ a.account }}</td><td class="px-4 py-3 text-sm">{{ a.name }}</td><td class="px-4 py-3 text-sm"><span :class="['px-2 py-0.5 rounded text-xs', a.role === '管理员' || a.role === 'admin' || a.role === '集团管理员' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-600']">{{ a.role }}</span></td><td class="px-4 py-3 text-sm">{{ a.company }}</td><td class="px-4 py-3 text-center"><span :class="['px-2 py-0.5 rounded text-xs', a.status === 'active' || a.status === 'enabled' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">{{ a.status === 'active' || a.status === 'enabled' ? '正常' : '禁用' }}</span></td><td class="px-4 py-3 text-center"><button @click="editAccount(a)" class="text-blue-600 text-sm mr-2">✎</button><button @click="deleteAccount(a.id)" class="text-red-500 text-sm">🗑</button></td></tr>
            </tbody></table>
        </div>
      </div>

      <!-- 数据管理 -->
      <div v-if="activeTab === 'data'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-2xl">
        <h2 class="font-bold text-slate-800 mb-4">数据管理</h2>
        <div class="space-y-4">
          <div class="p-4 bg-slate-50 rounded-xl">
            <h3 class="font-medium text-slate-800 mb-2">数据操作</h3>
            <div class="flex flex-wrap gap-3">
              <button @click="exportData" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">📥 导出数据 (JSON)</button>
              <button @click="clearAllData" class="px-4 py-2 bg-red-600 text-white rounded-xl text-sm hover:bg-red-700">🗑 清除所有数据</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 账号弹窗 -->
      <Teleport to="body">
        <div v-if="showAccountForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showAccountForm = false">
          <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingAccountId ? '编辑账号' : '添加账号' }}</h3>
          <div class="space-y-3">
            <select v-model="accountForm.role" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none"><option value="集团管理员">集团管理员</option><option value="分公司管理员">分公司管理员</option><option value="员工">员工</option></select>
              <input v-model="accountForm.name" placeholder="姓名" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.account" placeholder="账号" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.password" type="password" placeholder="密码" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
              <input v-model="accountForm.company" placeholder="所属公司" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            </div>
            <div class="flex gap-3 mt-6"><button @click="showAccountForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="saveAccount" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm">保存</button></div>
          </div>
        </div>
      </Teleport>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'

const activeTab = ref('accounts')
const tabs = [
  { key: 'accounts', label: '账号管理' },
  { key: 'data', label: '数据管理' }
]

const accounts = ref<any[]>([])
const showAccountForm = ref(false)
const editingAccountId = ref<string | null>(null)
const accountForm = ref({ role: '员工', name: '', account: '', password: '', company: '' })
const loadingAccounts = ref(false)

function editAccount(a: any) {
  accountForm.value = { role: a.role, name: a.name, account: a.account, password: '', company: a.company || '' }
  editingAccountId.value = a.id
  showAccountForm.value = true
}

async function saveAccount() {
  if (!accountForm.value.name || !accountForm.value.account) { alert('请填写账号和姓名'); return }
  if (!editingAccountId.value && !accountForm.value.password) { alert('新建账号需要填写密码'); return }

  try {
    if (editingAccountId.value) {
      const payload: any = { name: accountForm.value.name, role: accountForm.value.role, company: accountForm.value.company }
      if (accountForm.value.password) payload.password = accountForm.value.password
      await api.put(`/auth/users/${editingAccountId.value}`, payload)
      alert('更新成功')
    } else {
      await api.post('/auth/users', {
        account: accountForm.value.account,
        name: accountForm.value.name,
        password: accountForm.value.password,
        role: accountForm.value.role,
        company: accountForm.value.company,
      })
      alert('创建成功')
    }
    showAccountForm.value = false
    editingAccountId.value = null
    accountForm.value = { role: '员工', name: '', account: '', password: '', company: '' }
    await fetchAccounts()
  } catch (e: any) {
    const msg = e.response?.data?.detail || '操作失败'
    alert(msg)
  }
}

async function deleteAccount(id: string) {
  if (!confirm('确定删除该账号？')) return
  try {
    await api.delete(`/auth/users/${id}`)
    await fetchAccounts()
  } catch (e: any) {
    alert(e.response?.data?.detail || '删除失败')
  }
}

async function fetchAccounts() {
  loadingAccounts.value = true
  try {
    const res = await api.get('/auth/users')
    accounts.value = res.data || []
  } catch (e) {
    console.error('获取账号列表失败', e)
  } finally {
    loadingAccounts.value = false
  }
}

function exportData() {
  const data: any = {}
  const keys = ['calendar_tasks', 'work_reports', 'influencer_records', 'daren_resources', 'consensus_archives', 'training_problems', 'system_config', 'company_name']
  keys.forEach(k => { const v = localStorage.getItem(k); if (v) data[k] = JSON.parse(v) })
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = `x10_backup_${new Date().toISOString().split('T')[0]}.json`; a.click()
  URL.revokeObjectURL(url)
}

function clearAllData() {
  if (!confirm('⚠️ 此操作将清除所有本地数据，不可恢复！确定继续？')) return
  if (!confirm('再次确认：清除所有数据？')) return
  const keys = ['calendar_tasks', 'work_reports', 'influencer_records', 'daren_resources', 'consensus_archives', 'training_problems']
  keys.forEach(k => localStorage.removeItem(k))
  alert('数据已清除')
}

onMounted(() => {
  fetchAccounts()
})
</script>
