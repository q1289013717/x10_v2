<template>
  <AppLayout current-page="influencer-list">
    <template #title>
      <div class="flex items-center gap-2">
        <h1 v-if="!editingTitle" class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight truncate">{{ pageTitle }}</h1>
        <input v-else v-model="pageTitle" @blur="saveTitle" @keyup.enter="saveTitle" class="font-bold text-slate-900 text-lg lg:text-xl border-b-2 border-blue-500 outline-none bg-transparent w-48" />
        <button @click="editingTitle = true" class="text-slate-400 hover:text-blue-600 text-sm" title="编辑标题">✎</button>
      </div>
      <div class="flex items-center gap-2 mt-0.5">
        <p v-if="!editingSubtitle" class="text-xs text-slate-400 truncate">{{ pageSubtitle }}</p>
        <input v-else v-model="pageSubtitle" @blur="saveSubtitle" @keyup.enter="saveSubtitle" class="text-xs text-slate-400 border-b border-blue-500 outline-none bg-transparent w-64" />
        <button @click="editingSubtitle = true" class="text-slate-400 hover:text-blue-600 text-xs" title="编辑副标题">✎</button>
      </div>
    </template>
    <template #actions>
      <router-link to="/influencer-summary" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">📊 汇总统计</router-link>
      <button @click="openForm()" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">+ 新增记录</button>
    </template>
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 筛选 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-100 mb-6">
        <div class="flex flex-wrap gap-3">
          <input v-model="filters.influencerName" placeholder="搜索达人名称..." class="flex-1 min-w-[200px] h-10 px-4 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
          <select v-model="filters.platform" class="w-32 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none"><option value="all">全部平台</option><option v-for="p in platforms" :key="p" :value="p">{{ p }}</option></select>
          <select v-model="filters.payStatus" class="w-32 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none"><option value="all">全部状态</option><option value="已支付">已支付</option><option value="未支付">未支付</option><option value="部分支付">部分支付</option></select>
          <input v-model="filters.startDate" type="date" class="w-36 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
          <input v-model="filters.endDate" type="date" class="w-36 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
        </div>
      </div>

      <!-- 表格 -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead><tr class="border-b border-slate-100 bg-slate-50">
              <th class="px-3 py-3 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">日期</th>
              <th class="px-3 py-3 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">达人名称</th>
              <th class="px-3 py-3 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">平台</th>
              <th class="px-3 py-3 text-right text-sm font-semibold text-slate-600 whitespace-nowrap">粉丝数</th>
              <th class="px-3 py-3 text-right text-sm font-semibold text-slate-600 whitespace-nowrap">GMV(元)</th>
              <th class="px-3 py-3 text-right text-sm font-semibold text-slate-600 whitespace-nowrap">ROI</th>
              <th class="px-3 py-3 text-center text-sm font-semibold text-slate-600 whitespace-nowrap">支付状态</th>
              <th class="px-3 py-3 text-center text-sm font-semibold text-slate-600 whitespace-nowrap">操作</th>
            </tr></thead>
            <tbody>
              <tr v-for="r in paginatedRecords" :key="r.id" class="border-b border-slate-50 hover:bg-slate-50/50">
                <td class="px-3 py-3 text-sm whitespace-nowrap">{{ r.date }}</td>
                <td class="px-3 py-3"><span class="font-medium text-slate-800 text-sm">{{ r.influencerName }}</span></td>
                <td class="px-3 py-3"><span class="px-2 py-0.5 rounded text-xs bg-slate-100 text-slate-600">{{ r.platform === '其他' && (r.platformOther || r.platform_other) ? (r.platformOther || r.platform_other) : r.platform }}</span></td>
                <td class="px-3 py-3 text-right text-sm">{{ formatNum(r.fansCount) }}</td>
                <td class="px-3 py-3 text-right text-sm font-medium">¥{{ formatNum(r.gmv || 0) }}</td>
                <td class="px-3 py-3 text-right text-sm">{{ r.roi || '-' }}</td>
                <td class="px-3 py-3 text-center"><span :class="getPayStatusClass(r.pay_status || r.payStatus || '未支付')">{{ r.pay_status || r.payStatus || '未支付' }}</span></td>
                <td class="px-3 py-3 text-center">
                  <button @click="editRecord(r)" class="text-blue-600 hover:text-blue-700 text-sm mr-2" title="编辑">✎</button>
                  <button @click="deleteRecord(r.id)" class="text-red-500 hover:text-red-600 text-sm" title="删除">🗑</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="filteredRecords.length === 0" class="text-center py-16 text-slate-400"><span class="text-4xl block mb-4">📊</span><p>暂无记录</p></div>
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 p-4 border-t border-slate-100">
          <button :disabled="page <= 1" @click="page--" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-30">←</button>
          <span class="text-sm text-slate-500">{{ page }} / {{ totalPages }}</span>
          <button :disabled="page >= totalPages" @click="page++" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-30">→</button>
        </div>
      </div>
    </div>

    <!-- 新增/编辑弹窗 — 完整版 -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showForm = false">
        <div class="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto">
          <!-- 弹窗头部 -->
          <div class="sticky top-0 bg-white border-b border-slate-100 px-6 py-4 rounded-t-2xl z-10">
            <h3 class="font-bold text-slate-800 text-lg">{{ editingId ? '编辑达人合作记录' : '新增达人合作记录' }}</h3>
          </div>

          <div class="p-6 space-y-6">
            <!-- 基本信息 -->
            <div>
              <h4 class="text-sm font-semibold text-slate-700 mb-3 pb-2 border-b border-slate-100">📋 基本信息</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">日期 <span class="text-red-400">*</span></label>
                  <input v-model="form.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">达人名称 <span class="text-red-400">*</span></label>
                  <input v-model="form.influencerName" placeholder="请输入达人名称" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">达人ID <span class="text-red-400">*</span></label>
                  <input v-model="form.influencerId" placeholder="请输入达人ID" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">对接人及联系方式</label>
                  <input v-model="form.contactPerson" placeholder="格式：姓名-电话" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">主作平台 <span class="text-red-400">*</span></label>
                  <div class="flex gap-2">
                    <select v-model="form.platform" class="flex-1 h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                      <option value="">选择平台</option><option v-for="p in platforms" :key="p" :value="p">{{ p }}</option>
                    </select>
                  </div>
                  <input v-if="form.platform === '其他'" v-model="form.platformOther" placeholder="请填写具体平台..." class="w-full h-10 px-3 mt-2 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">平台UID</label>
                  <input v-model="form.platformUid" placeholder="平台UID" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">佣金比例(%) <span class="text-red-400">*</span></label>
                  <input v-model="form.commissionRate" type="number" step="0.01" placeholder="保留2位小数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">投流方式 <span class="text-red-400">*</span></label>
                  <select v-model="form.trafficType" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                    <option value="">请选择</option>
                    <option value="千川">千川</option>
                    <option value="随心推">随心推</option>
                    <option value="本地推">本地推</option>
                    <option value="自然流">自然流</option>
                    <option value="混合">混合</option>
                    <option value="其他">其他</option>
                  </select>
                  <input v-if="form.trafficType === '其他'" v-model="form.trafficTypeOther" placeholder="请填写具体投流方式..." class="w-full h-10 px-3 mt-2 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
              </div>
            </div>

            <!-- 合作信息 -->
            <div>
              <h4 class="text-sm font-semibold text-slate-700 mb-3 pb-2 border-b border-slate-100">🤝 合作信息</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">合作开始日期 <span class="text-red-400">*</span></label>
                  <input v-model="form.coopStartDate" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">合作结束日期 <span class="text-red-400">*</span></label>
                  <input v-model="form.coopEndDate" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">带货合规情况 <span class="text-red-400">*</span></label>
                  <select v-model="form.complianceStatus" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                    <option value="">请选择</option>
                    <option value="合规">合规</option>
                    <option value="需整改">需整改</option>
                    <option value="不合规">不合规</option>
                    <option value="待确认">待确认</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">支付状态 <span class="text-red-400">*</span></label>
                  <select v-model="form.payStatus" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                    <option value="">请选择</option>
                    <option value="已支付">已支付</option>
                    <option value="未支付">未支付</option>
                    <option value="部分支付">部分支付</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- 业绩数据 -->
            <div>
              <h4 class="text-sm font-semibold text-slate-700 mb-3 pb-2 border-b border-slate-100">📈 业绩数据</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">GMV(元) <span class="text-red-400">*</span></label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">¥</span>
                    <input v-model="form.gmv" type="number" step="0.01" placeholder="保留2位小数" class="w-full h-10 pl-8 pr-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                  </div>
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">ROI值</label>
                  <input v-model="form.roi" type="number" step="0.01" placeholder="保留2位小数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">转化率(%)</label>
                  <input v-model="form.conversionRate" type="number" step="0.01" placeholder="保留2位小数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">退货率(%)</label>
                  <input v-model="form.returnRate" type="number" step="0.01" placeholder="保留2位小数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
              </div>
            </div>

            <!-- 复播信息 -->
            <div>
              <h4 class="text-sm font-semibold text-slate-700 mb-3 pb-2 border-b border-slate-100">🔄 复播信息</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">复播意图 <span class="text-red-400">*</span></label>
                  <select v-model="form.rebroadcastIntent" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500">
                    <option value="">请选择</option>
                    <option value="有意向">有意向</option>
                    <option value="无意向">无意向</option>
                    <option value="待确认">待确认</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-medium text-slate-500 mb-1 block">复播时间 <span class="text-red-400">*</span></label>
                  <input v-model="form.rebroadcastTime" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
              </div>
            </div>

            <!-- 备注 -->
            <div>
              <h4 class="text-sm font-semibold text-slate-700 mb-3 pb-2 border-b border-slate-100">📝 备注</h4>
              <textarea v-model="form.remark" placeholder="请输入备注信息（选填）" rows="3" class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none resize-none focus:border-blue-500" />
            </div>
          </div>

          <!-- 底部按钮 -->
          <div class="sticky bottom-0 bg-white border-t border-slate-100 px-6 py-4 rounded-b-2xl flex gap-3">
            <button @click="showForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50 transition-colors">取消</button>
            <button @click="saveRecord" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 transition-colors font-medium">提交记录</button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'

const showForm = ref(false)
const editingId = ref<string | null>(null)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

// 页面标题可编辑
const editingTitle = ref(false)
const editingSubtitle = ref(false)
const pageTitle = ref(localStorage.getItem('influencer_page_title') || '达人合作台账')
const pageSubtitle = ref(localStorage.getItem('influencer_page_subtitle') || '管理达人合作记录与数据')

function saveTitle() {
  localStorage.setItem('influencer_page_title', pageTitle.value)
  editingTitle.value = false
}
function saveSubtitle() {
  localStorage.setItem('influencer_page_subtitle', pageSubtitle.value)
  editingSubtitle.value = false
}

const platforms = ['抖音', '快手', '小红书', '视频号', '淘宝直播', '其他']

const filters = ref({ influencerName: '', platform: 'all', payStatus: 'all', startDate: '', endDate: '' })

const EMPTY_FORM = {
  date: new Date().toISOString().split('T')[0],
  influencerName: '',
  influencerId: '',
  contactPerson: '',
  platform: '',
  platformOther: '',
  platformUid: '',
  commissionRate: '',
  trafficType: '',
  trafficTypeOther: '',
  coopStartDate: '',
  coopEndDate: '',
  complianceStatus: '',
  payStatus: '',
  gmv: '',
  roi: '',
  conversionRate: '',
  returnRate: '',
  rebroadcastIntent: '',
  rebroadcastTime: '',
  remark: ''
}

const form = ref({ ...EMPTY_FORM })
const records = ref<any[]>([])

const filteredRecords = computed(() => {
  return records.value.filter(r => {
    const name = r.influencer_name || r.influencerName || ''
    if (filters.value.influencerName && !name.toLowerCase().includes(filters.value.influencerName.toLowerCase())) return false
    // 平台：处理"其他"选项
    const plat = (r.platform === '其他' && r.platformOther) ? r.platformOther : (r.platform || '')
    const filterPlat = filters.value.platform
    if (filterPlat !== 'all' && !plat.includes(filterPlat)) return false
    const pay = r.pay_status || r.payStatus || ''
    if (filters.value.payStatus !== 'all' && pay !== filters.value.payStatus) return false
    if (filters.value.startDate && (r.date || '') < filters.value.startDate) return false
    if (filters.value.endDate && (r.date || '') > filters.value.endDate) return false
    return true
  }).sort((a, b) => (b.date || '').localeCompare(a.date || ''))
})

const totalPages = computed(() => Math.ceil(filteredRecords.value.length / pageSize) || 1)
const paginatedRecords = computed(() => filteredRecords.value.slice((page.value - 1) * pageSize, page.value * pageSize))

function formatNum(n: number) { if (!n) return '0'; return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toLocaleString() }

function getPayStatusClass(status: string) {
  const map: any = {
    '已支付': 'px-2 py-0.5 rounded text-xs bg-emerald-100 text-emerald-700',
    '未支付': 'px-2 py-0.5 rounded text-xs bg-amber-100 text-amber-700',
    '部分支付': 'px-2 py-0.5 rounded text-xs bg-blue-100 text-blue-700'
  }
  return map[status] || 'px-2 py-0.5 rounded text-xs bg-slate-100 text-slate-600'
}

function openForm() { form.value = { ...EMPTY_FORM }; editingId.value = null; showForm.value = true }
function editRecord(r: any) { form.value = mapToFrontend(r); editingId.value = r.id; showForm.value = true }

// 映射前端字段到后端 snake_case
function mapToBackend(f: typeof form.value) {
  return {
    date: f.date,
    influencer_name: f.influencerName,
    influencer_id: f.influencerId,
    contact_person: f.contactPerson,
    platform: f.platform === '其他' ? (f.platformOther || '其他') : f.platform,
    platform_other: f.platformOther,
    platform_uid: f.platformUid,
    commission_rate: parseFloat(f.commissionRate) || 0,
    traffic_type: f.trafficType === '其他' ? (f.trafficTypeOther || '其他') : f.trafficType,
    traffic_type_other: f.trafficTypeOther,
    coop_start_date: f.coopStartDate || null,
    coop_end_date: f.coopEndDate || null,
    compliance_status: f.complianceStatus,
    pay_status: f.payStatus,
    gmv: parseFloat(f.gmv) || 0,
    roi: parseFloat(f.roi) || 0,
    conversion_rate: parseFloat(f.conversionRate) || 0,
    return_rate: parseFloat(f.returnRate) || 0,
    rebroadcast_intent: f.rebroadcastIntent,
    rebroadcast_time: f.rebroadcastTime || null,
    remark: f.remark,
  }
}

// 映射后端字段到前端 camelCase
function mapToFrontend(r: any) {
  return {
    id: r.id,
    date: r.date || '',
    influencerName: r.influencer_name || r.influencerName || '',
    influencerId: r.influencer_id || r.influencerId || '',
    contactPerson: r.contact_person || r.contactPerson || '',
    platform: r.platform_other ? '其他' : (r.platform || ''),
    platformOther: r.platform_other || '',
    platformUid: r.platform_uid || r.platformUid || '',
    commissionRate: r.commission_rate ?? r.commissionRate ?? '',
    trafficType: r.traffic_type_other ? '其他' : (r.traffic_type || r.trafficType || ''),
    trafficTypeOther: r.traffic_type_other || '',
    coopStartDate: r.coop_start_date || r.coopStartDate || '',
    coopEndDate: r.coop_end_date || r.coopEndDate || '',
    complianceStatus: r.compliance_status || r.complianceStatus || '',
    payStatus: r.pay_status || r.payStatus || '',
    gmv: r.gmv ?? '',
    roi: r.roi ?? '',
    conversionRate: r.conversion_rate ?? r.conversionRate ?? '',
    returnRate: r.return_rate ?? r.returnRate ?? '',
    rebroadcastIntent: r.rebroadcast_intent || r.rebroadcastIntent || '',
    rebroadcastTime: r.rebroadcast_time || r.rebroadcastTime || '',
    remark: r.remark || '',
  }
}

async function fetchRecords() {
  loading.value = true
  try {
    const res = await api.get('/influencers/records', { params: { limit: 200 } })
    records.value = (res.data || []).map(mapToFrontend)
  } catch {
    // 降级到 localStorage
    const saved = localStorage.getItem('influencer_records')
    if (saved) { try { records.value = JSON.parse(saved) } catch {} }
  } finally {
    loading.value = false
  }
}

async function saveRecord() {
  if (!form.value.influencerName) return
  loading.value = true
  try {
    const payload = mapToBackend(form.value)
    if (editingId.value) {
      await api.put(`/influencers/records/${editingId.value}`, payload)
    } else {
      await api.post('/influencers/records', payload)
    }
    await fetchRecords()
    showForm.value = false
    editingId.value = null
  } catch (e: any) {
    // 降级到本地存储
    const payload = { ...form.value }
    if (editingId.value) {
      const i = records.value.findIndex(r => r.id === editingId.value)
      if (i >= 0) records.value[i] = { ...payload, id: editingId.value }
    } else {
      records.value.unshift({ ...payload, id: Date.now().toString() })
    }
    localStorage.setItem('influencer_records', JSON.stringify(records.value))
    showForm.value = false
    editingId.value = null
    alert('后端暂不可用，已保存到本地')
  } finally {
    loading.value = false
  }
}

async function deleteRecord(id: string) {
  if (!confirm('确定删除？')) return
  loading.value = true
  try {
    await api.delete(`/influencers/records/${id}`)
    await fetchRecords()
  } catch {
    records.value = records.value.filter(r => r.id !== id)
    localStorage.setItem('influencer_records', JSON.stringify(records.value))
  } finally {
    loading.value = false
  }
}

onMounted(fetchRecords)
</script>
