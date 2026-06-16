<template>
  <AppLayout current-page="darensource" title="达人资源库" subtitle="资源录入、查询与统计">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Tab 切换 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-100 mb-6 flex flex-wrap gap-2">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" :class="['px-4 py-2 rounded-lg text-sm transition-all', activeTab === tab.id ? 'bg-blue-600 text-white' : 'bg-slate-50 text-slate-600 hover:bg-slate-100']">{{ tab.label }}</button>
      </div>

      <!-- +资源录入 -->
      <div v-if="activeTab === 'add'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-3xl">
        <h3 class="font-bold text-slate-800 text-lg mb-6">+ 达人资源录入</h3>

        <!-- 基本信息 -->
        <div class="mb-6">
          <h4 class="text-sm font-semibold text-slate-600 mb-4 pb-2 border-b border-slate-100">基本信息</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">姓名 <span class="text-red-400">*</span></label>
              <input v-model="resource.name" placeholder="请输入姓名" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">日期 <span class="text-red-400">*</span></label>
              <input v-model="resource.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">达人排号ID <span class="text-red-400">*</span></label>
              <input v-model="resource.code" placeholder="如: DB006" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
          </div>
        </div>

        <!-- 平台信息 -->
        <div class="mb-6">
          <h4 class="text-sm font-semibold text-slate-600 mb-4 pb-2 border-b border-slate-100">平台信息</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">达人账号名称 <span class="text-red-400">*</span></label>
              <input v-model="resource.accountName" placeholder="请输入达人账号名称" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">运营平台 <span class="text-red-400">*</span></label>
              <select v-model="resource.platform" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                <option value="">请选择运营平台</option>
                <option v-for="p in platforms" :key="p" :value="p">{{ p }}</option>
              </select>
              <input v-if="resource.platform === '其他'" v-model="resource.platformOther" placeholder="请填写具体平台名称..." class="w-full h-10 px-3 mt-2 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">联系方式 <span class="text-red-400">*</span></label>
              <input v-model="resource.phone" placeholder="请输入手机号" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">对接微信号 <span class="text-red-400">*</span></label>
              <input v-model="resource.wechat" placeholder="请输入对接微信号" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
          </div>
        </div>

        <!-- 达人数据 -->
        <div class="mb-6">
          <h4 class="text-sm font-semibold text-slate-600 mb-4 pb-2 border-b border-slate-100">达人数据</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">粉丝数量(万) <span class="text-red-400">*</span></label>
              <input v-model="resource.fansCount" type="number" step="0.1" placeholder="保留1位小数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">核心类目 <span class="text-red-400">*</span></label>
              <select v-model="resource.category" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                <option value="">请选择核心类目</option>
                <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
              </select>
              <input v-if="resource.category === '其他'" v-model="resource.categoryOther" placeholder="请填写具体类目..." class="w-full h-10 px-3 mt-2 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
          </div>
          <div class="mt-4">
            <label class="text-xs font-medium text-slate-500 mb-1 block">粉丝画像 <span class="text-red-400">*</span></label>
            <textarea v-model="resource.fansProfile" placeholder="请描述粉丝画像特征，如：年龄层、消费能力、兴趣爱好等" rows="3" class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none resize-none focus:border-blue-500" />
          </div>
          <div class="mt-4">
            <label class="text-xs font-medium text-slate-500 mb-1 block">同类目带货GMV(万/月) <span class="text-red-400">*</span></label>
            <input v-model="resource.gmv" type="number" step="0.01" placeholder="保留2位小数，空默认0" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
          </div>
        </div>

        <!-- 跟进信息 -->
        <div class="mb-6">
          <h4 class="text-sm font-semibold text-slate-600 mb-4 pb-2 border-b border-slate-100">跟进信息</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">触达渠道 <span class="text-red-400">*</span></label>
              <input v-model="resource.reachChannel" placeholder="请输入触达渠道" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">首次建联时间 <span class="text-red-400">*</span></label>
              <input v-model="resource.firstContactTime" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">最新跟进时间 <span class="text-red-400">*</span></label>
              <input v-model="resource.lastFollowTime" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="text-xs font-medium text-slate-500 mb-1 block">下次跟进时间 <span class="text-red-400">*</span></label>
              <input v-model="resource.nextFollowTime" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
          </div>
        </div>

        <!-- 提交 -->
        <button @click="saveResource" :disabled="!resource.name" class="px-8 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50 transition-colors font-medium">
          + 达人资源录入
        </button>
      </div>

      <!-- 我的资源 / 全量资源 -->
      <div v-if="activeTab === 'mine' || activeTab === 'all'">
        <div class="mb-4 relative max-w-md">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
          <input v-model="search" placeholder="搜索达人姓名、排号、类目..." class="w-full pl-11 pr-4 h-11 rounded-xl border border-slate-200 bg-white text-sm outline-none focus:border-blue-500" />
        </div>
        <!-- 列表 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="r in filteredResources" :key="r.id" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-slate-800 flex items-center gap-2">
                  {{ r.name }}
                  <span class="text-xs text-slate-400 font-normal">{{ r.code }}</span>
                </h3>
                <p class="text-sm text-slate-500 mt-0.5">{{ displayPlatform(r) }} · {{ displayCategory(r) }}</p>
              </div>
              <button @click="deleteResource(r.id)" class="text-slate-300 hover:text-red-500 text-sm transition-colors">🗑</button>
            </div>
            <div class="flex flex-wrap gap-2 text-xs">
              <span class="px-2 py-0.5 bg-slate-100 rounded text-slate-600">粉丝 {{ formatFans(r.fansCount) }}</span>
              <span v-if="r.gmv" class="px-2 py-0.5 bg-blue-50 text-blue-600 rounded">GMV ¥{{ r.gmv }}万</span>
              <span class="px-2 py-0.5 bg-green-50 text-green-600 rounded">{{ displayCategory(r) }}</span>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-50 text-xs text-slate-400 space-y-1">
              <p v-if="r.phone">📞 {{ r.phone }}</p>
              <p v-if="r.wechat">💬 {{ r.wechat }}</p>
              <p v-if="r.reachChannel">📡 {{ r.reachChannel }}</p>
              <p v-if="r.nextFollowTime" class="text-amber-500">⏰ 下次跟进: {{ r.nextFollowTime }}</p>
            </div>
          </div>
        </div>
        <div v-if="filteredResources.length === 0 && !search" class="text-center py-16 text-slate-400">
          <span class="text-5xl block mb-4">🗄</span>
          <p v-if="activeTab === 'mine'">暂无我的资源</p>
          <p v-else>暂无从各资源，点击上方"资源录入"添加</p>
        </div>
      </div>

      <!-- 数据汇总 -->
      <div v-if="activeTab === 'summary'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
        <h3 class="font-bold text-slate-800 text-lg mb-4">📊 数据汇总</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-blue-50 rounded-xl p-4 text-center">
            <p class="text-3xl font-bold text-blue-600">{{ resources.length }}</p>
            <p class="text-sm text-blue-500 mt-1">达人总数</p>
          </div>
          <div class="bg-emerald-50 rounded-xl p-4 text-center">
            <p class="text-3xl font-bold text-emerald-600">{{ platformStats.length }}</p>
            <p class="text-sm text-emerald-500 mt-1">覆盖平台</p>
          </div>
          <div class="bg-purple-50 rounded-xl p-4 text-center">
            <p class="text-3xl font-bold text-purple-600">{{ categoryStats.length }}</p>
            <p class="text-sm text-purple-500 mt-1">覆盖类目</p>
          </div>
          <div class="bg-amber-50 rounded-xl p-4 text-center">
            <p class="text-3xl font-bold text-amber-600">{{ totalFans }}</p>
            <p class="text-sm text-amber-500 mt-1">总粉丝量(万)</p>
          </div>
        </div>
        <!-- 平台分布 -->
        <div class="mb-6">
          <h4 class="text-sm font-semibold text-slate-600 mb-3">平台分布</h4>
          <div class="space-y-2">
            <div v-for="ps in platformStats" :key="ps.name" class="flex items-center gap-3">
              <span class="w-20 text-sm text-slate-600">{{ ps.name }}</span>
              <div class="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" :style="{ width: (ps.count / Math.max(1, resources.length) * 100) + '%' }" />
              </div>
              <span class="text-sm font-medium text-slate-700 w-10 text-right">{{ ps.count }}</span>
            </div>
          </div>
        </div>
        <!-- 类目分布 -->
        <div>
          <h4 class="text-sm font-semibold text-slate-600 mb-3">类目分布</h4>
          <div class="space-y-2">
            <div v-for="cs in categoryStats" :key="cs.name" class="flex items-center gap-3">
              <span class="w-20 text-sm text-slate-600">{{ cs.name }}</span>
              <div class="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full" :style="{ width: (cs.count / Math.max(1, resources.length) * 100) + '%' }" />
              </div>
              <span class="text-sm font-medium text-slate-700 w-10 text-right">{{ cs.count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'

const activeTab = ref('all')
const search = ref('')
const platforms = ['抖音', '快手', '小红书', '视频号', '淘宝直播', 'B站', '其他']
const categories = ['美妆护肤', '服饰穿搭', '食品零食', '家居日用', '母婴用品', '3C数码', '个护清洁', '运动户外', '教育培训', '其他']

const tabs = [
  { id: 'add', label: '+ 资源录入' },
  { id: 'mine', label: '我的资源' },
  { id: 'all', label: '全量资源' },
  { id: 'summary', label: '数据汇总' }
]

const EMPTY_RESOURCE = {
  name: '', date: new Date().toISOString().split('T')[0], code: '',
  accountName: '', platform: '', platformOther: '', phone: '', wechat: '',
  fansCount: '', category: '', categoryOther: '', fansProfile: '', gmv: '',
  reachChannel: '', firstContactTime: '', lastFollowTime: '', nextFollowTime: ''
}

const resource = ref({ ...EMPTY_RESOURCE })
const resources = ref<any[]>([])
const loading = ref(false)

const filteredResources = computed(() => {
  const all = activeTab.value === 'mine' ? resources.value.filter((r: any) => r.is_mine) : resources.value
  if (!search.value) return all
  return all.filter((r: any) =>
    r.name?.toLowerCase().includes(search.value.toLowerCase()) ||
    r.code?.toLowerCase().includes(search.value.toLowerCase()) ||
    r.category?.toLowerCase().includes(search.value.toLowerCase()) ||
    r.platform?.toLowerCase().includes(search.value.toLowerCase())
  )
})

const platformStats = computed(() => {
  const map: Record<string, number> = {}
  resources.value.forEach((r: any) => {
    const p = r.platform === '其他' && r.platformOther ? r.platformOther : r.platform
    if (p) map[p] = (map[p] || 0) + 1
  })
  return Object.entries(map).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count)
})

const categoryStats = computed(() => {
  const map: Record<string, number> = {}
  resources.value.forEach((r: any) => {
    const c = r.category === '其他' && r.categoryOther ? r.categoryOther : r.category
    if (c) map[c] = (map[c] || 0) + 1
  })
  return Object.entries(map).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count)
})

const totalFans = computed(() => {
  return resources.value.reduce((sum: number, r: any) => sum + parseFloat(r.fansCount || r.fans_count || '0'), 0).toFixed(1)
})

function formatFans(n: number) { if (!n) return '0'; return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toLocaleString() }

// 显示平台时，如果是"其他"则显示自填内容
function displayPlatform(r: any) {
  return r.platform === '其他' && r.platformOther ? r.platformOther : (r.platform || '-')
}
function displayCategory(r: any) {
  return r.category === '其他' && r.categoryOther ? r.categoryOther : (r.category || '-')
}

async function saveResource() {
  if (!resource.value.name) return
  loading.value = true
  try {
    // 组装后端字段（snake_case）
    const payload: any = {
      name: resource.value.name,
      daren_id: resource.value.code,
      account_name: resource.value.accountName,
      platform: resource.value.platform === '其他' ? (resource.value.platformOther || '其他') : resource.value.platform,
      contact: resource.value.phone,
      wechat: resource.value.wechat,
      fans_count: parseFloat(resource.value.fansCount) || 0,
      category: resource.value.category === '其他' ? (resource.value.categoryOther || '其他') : resource.value.category,
      fans_profile: resource.value.fansProfile,
      gmv_monthly: parseFloat(resource.value.gmv) || 0,
      reach_channel: resource.value.reachChannel,
      first_contact_time: resource.value.firstContactTime || null,
      last_follow_time: resource.value.lastFollowTime || null,
      next_follow_time: resource.value.nextFollowTime || null,
      // 保存原始选择值和自填值（用extra_data扩展字段）
      platform_raw: resource.value.platform,
      platform_other: resource.value.platformOther,
      category_raw: resource.value.category,
      category_other: resource.value.categoryOther,
    }
    await api.post('/daren/resources', payload)
    resource.value = { ...EMPTY_RESOURCE, date: new Date().toISOString().split('T')[0] }
    activeTab.value = 'mine'
    await fetchResources()
    alert('录入成功！')
  } catch (e: any) {
    // 降级到本地存储
    const r = { ...resource.value, id: Date.now().toString() }
    resources.value.unshift(r)
    localStorage.setItem('daren_resources', JSON.stringify(resources.value))
    resource.value = { ...EMPTY_RESOURCE, date: new Date().toISOString().split('T')[0] }
    alert('后端暂不可用，已保存到本地')
  } finally {
    loading.value = false
  }
}

async function deleteResource(id: string) {
  if (!confirm('确定删除该达人资源？')) return
  try {
    await api.delete(`/daren/resources/${id}`)
    await fetchResources()
  } catch {
    resources.value = resources.value.filter((r: any) => r.id !== id)
    localStorage.setItem('daren_resources', JSON.stringify(resources.value))
  }
}

async function fetchResources() {
  loading.value = true
  try {
    const res = await api.get('/daren/resources', { params: { limit: 200 } })
    resources.value = (res.data || []).map((r: any) => ({
      ...r,
      // 映射字段
      code: r.daren_id || r.code,
      accountName: r.account_name || r.accountName,
      phone: r.contact || r.phone,
      fansCount: r.fans_count || r.fansCount,
      fansProfile: r.fans_profile || r.fansProfile,
      gmv: r.gmv_monthly || r.gmv,
      reachChannel: r.reach_channel || r.reachChannel,
      firstContactTime: r.first_contact_time || r.firstContactTime,
      lastFollowTime: r.last_follow_time || r.lastFollowTime,
      nextFollowTime: r.next_follow_time || r.nextFollowTime,
      platformOther: r.platform_other || '',
      categoryOther: r.category_other || '',
      is_mine: true, // 暂时标记，后端会返回created_by
    }))
  } catch {
    // 降级到本地
    const saved = localStorage.getItem('daren_resources')
    if (saved) { try { resources.value = JSON.parse(saved) } catch {} }
  } finally {
    loading.value = false
  }
}

onMounted(fetchResources)
</script>
