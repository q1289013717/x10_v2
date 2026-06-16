<template>
  <AppLayout current-page="training" title="X10成长中心" subtitle="知识库、BD自查手册与刷题系统">
    <template #actions>
      <button v-if="isAdmin" @click="showAddDoc = true" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700 transition-colors">➕ 新增文档</button>
      <router-link to="/training-quiz" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">📝 刷题</router-link>
      <router-link to="/training-problem" class="px-4 py-2 bg-amber-600 text-white rounded-xl text-sm hover:bg-amber-700">📋 难题库</router-link>
    </template>
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 搜索 -->
      <div class="mb-6"><div class="relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索知识条目..." class="w-full pl-11 pr-4 h-12 bg-white rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" /></div></div>

      <!-- 分类 -->
      <div class="mb-6 flex flex-wrap gap-2">
        <button v-for="cat in categories" :key="cat.id" @click="activeCat = cat.id" :class="['px-4 py-2 rounded-xl text-sm transition-all', activeCat === cat.id ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50']">{{ cat.name }}</button>
      </div>

      <!-- 文档列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="doc in filteredDocs" :key="doc.id" @click="goDetail(doc.id)" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all cursor-pointer relative group">
          <div class="flex items-start gap-3">
            <span class="text-3xl">{{ doc.icon }}</span>
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-slate-800 truncate">{{ doc.title }}</h3>
              <p class="text-sm text-slate-500 mt-1 line-clamp-2">{{ doc.desc }}</p>
            </div>
            <!-- 管理员删除按钮 -->
            <button v-if="isAdmin" @click.stop="confirmDelete(doc)" class="opacity-0 group-hover:opacity-100 transition-opacity w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 flex-shrink-0" title="删除文档">
              🗑
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredDocs.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📚</span><p>暂无相关文档</p></div>

      <!-- 新增文档弹窗 -->
      <div v-if="showAddDoc" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAddDoc = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
          <h2 class="text-lg font-bold text-slate-900 mb-4">新增知识文档</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">文档标题</label>
              <input v-model="newDoc.title" placeholder="请输入文档标题" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">分类</label>
              <select v-model="newDoc.category" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
                <option value="bd">BD自查手册</option>
                <option value="sop">SOP流程</option>
                <option value="product">产品知识</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">简要描述</label>
              <input v-model="newDoc.desc" placeholder="请输入简要描述" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">图标</label>
              <input v-model="newDoc.icon" placeholder="如 📖、🔍、💡" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">内容（Markdown）</label>
              <textarea v-model="newDoc.content" rows="6" placeholder="请输入文档内容..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none" />
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showAddDoc = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="addDoc" :disabled="!newDoc.title" class="px-5 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50">创建</button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()
const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

const search = ref('')
const activeCat = ref('all')
const showAddDoc = ref(false)
const newDoc = ref({ title: '', category: 'bd', desc: '', icon: '📖', content: '' })

const categories = [
  { id: 'all', name: '全部' },
  { id: 'bd', name: 'BD自查手册' },
  { id: 'sop', name: 'SOP流程' },
  { id: 'product', name: '产品知识' },
  { id: 'other', name: '其他' }
]

const docs = ref([
  { id: 'c1', cat: 'bd', title: '赵宜主品牌核心信息', desc: '品牌定位、实力、核心优势、介绍口径', icon: '🏷' },
  { id: 'c2', cat: 'bd', title: '赵宜主产品体系信息', desc: '产品线、核心卖点、适配达人类型', icon: '📦' },
  { id: 'c3', cat: 'bd', title: '赵宜主达人合作政策体系', desc: '佣金体系、合作模式、福利政策', icon: '💰' },
  { id: 'c4', cat: 'bd', title: '达人BD基础常识', desc: '行业术语、平台规则、粉丝画像', icon: '📖' },
  { id: 'c5', cat: 'sop', title: '达人筛选标准SOP', desc: '获客渠道、判定标准、筛选动作', icon: '🔍' },
  { id: 'c6', cat: 'sop', title: '达人首次触达开发SOP', desc: '事前准备、沟通要点、跟进时效', icon: '📞' },
  { id: 'c7', cat: 'sop', title: '达人需求挖掘SOP', desc: '挖需求话术、信息登记、意向判定', icon: '💡' },
  { id: 'c8', cat: 'sop', title: '达人合作方案报价SOP', desc: '方案制作、审核流程、时效约束', icon: '📋' },
  { id: 'c9', cat: 'product', title: '产品卖点速查手册', desc: '各产品核心卖点、对比优势', icon: '🎯' },
  { id: 'c10', cat: 'other', title: '常见问题FAQ', desc: '达人常见疑问和标准回答', icon: '❓' }
])

const filteredDocs = computed(() => {
  let result = docs.value
  if (activeCat.value !== 'all') result = result.filter(d => d.cat === activeCat.value)
  if (search.value) result = result.filter(d => d.title.includes(search.value) || d.desc.includes(search.value))
  return result
})

function goDetail(id: string) {
  router.push(`/training-detail/${id}`)
}

// 加载后端文档列表
onMounted(async () => {
  try {
    const res = await api.get('/training/docs')
    if (res.data?.length) {
      // 合并后端数据到 docs
      const backendDocs = res.data.map((d: any) => ({
        id: d.id,
        cat: d.category || 'other',
        title: d.title,
        desc: d.content?.slice(0, 50) || '',
        icon: '📄',
        content: d.content || '',
      }))
      // 替换为后端数据（如果后端有数据的话）
      // 如果后端为空则保留硬编码默认数据
      docs.value = [...backendDocs, ...docs.value.filter(d => !backendDocs.find((b: any) => b.id === d.id))]
    }
  } catch {
    // 后端不可用时保留本地数据
  }
})

async function addDoc() {
  if (!newDoc.value.title) return
  try {
    await api.post('/training/docs', {
      title: newDoc.value.title,
      category: newDoc.value.category,
      content: newDoc.value.content || newDoc.value.desc,
      source_type: 'knowledge',
    })
    // 刷新列表
    const res = await api.get('/training/docs')
    if (res.data?.length) {
      docs.value = res.data.map((d: any) => ({
        id: d.id,
        cat: d.category || 'other',
        title: d.title,
        desc: d.content?.slice(0, 50) || '',
        icon: '📄',
      }))
    }
    showAddDoc.value = false
    newDoc.value = { title: '', category: 'bd', desc: '', icon: '📖', content: '' }
  } catch (e: any) {
    alert('创建失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function confirmDelete(doc: any) {
  if (!confirm(`确定要删除「${doc.title}」吗？此操作不可撤销。`)) return
  try {
    await api.delete(`/training/docs/${doc.id}`)
    docs.value = docs.value.filter(d => d.id !== doc.id)
  } catch (e: any) {
    alert('删除失败: ' + (e.response?.data?.detail || e.message))
  }
}
</script>
