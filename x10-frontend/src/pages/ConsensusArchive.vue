<template>
  <AppLayout current-page="consensus-archive" title="共识档案" subtitle="会议纪要与共识管理">
    <template #actions>
      <button @click="openForm()" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 transition-colors">+ 新建会议记录</button>
    </template>
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <div class="mb-4 relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索会议记录..." class="w-full pl-11 pr-4 h-11 rounded-xl border border-slate-200 bg-white text-sm outline-none" /></div>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-16 text-slate-400"><span class="text-3xl block mb-3">⏳</span><p>加载中...</p></div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="a in filteredArchives" :key="a.id"
          @click="openDetail(a)"
          class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-blue-200 transition-all cursor-pointer group">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-slate-800 truncate group-hover:text-blue-600 transition-colors">{{ a.title }}</h3>
              <p class="text-xs text-slate-400 mt-1">📅 {{ formatDate(a) }} · 👤 {{ a.author || a.created_by || '未知' }}</p>
            </div>
            <div class="flex gap-1 flex-shrink-0 ml-2" @click.stop>
              <button @click="openForm(a)" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-blue-50 text-blue-500 hover:text-blue-600 text-sm">✎</button>
              <button @click="deleteArchive(a.id)" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-50 text-red-400 hover:text-red-600 text-sm">🗑</button>
            </div>
          </div>
          <p class="text-sm text-slate-600 line-clamp-3">{{ a.content }}</p>

          <!-- 附件列表 -->
          <div v-if="getAttachments(a).length" class="mt-3 flex flex-wrap gap-2">
            <span class="flex items-center gap-1 px-2.5 py-1 bg-blue-50 rounded-lg text-xs text-blue-600">
              📎 {{ getAttachments(a).length }} 个附件
            </span>
          </div>

          <div class="flex flex-wrap gap-1 mt-3">
            <span v-for="tag in (a.tags || [])" :key="tag" class="px-2 py-0.5 bg-slate-100 rounded text-xs text-slate-500">{{ tag }}</span>
          </div>
        </div>
      </div>

      <div v-if="!loading && filteredArchives.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📖</span><p>暂无会议记录</p></div>
    </div>

    <!-- ========== 详情弹窗 ========== -->
    <Teleport to="body">
      <div v-if="detailItem" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="detailItem = null">
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-auto">
          <div class="p-6 lg:p-8">
            <!-- 标题栏 -->
            <div class="flex items-start justify-between mb-6">
              <div class="flex-1 min-w-0">
                <h2 class="text-xl font-bold text-slate-900">{{ detailItem.title }}</h2>
                <p class="text-sm text-slate-400 mt-1">📅 {{ formatDate(detailItem) }} · 👤 {{ detailItem.author || detailItem.created_by || '未知' }}</p>
              </div>
              <button @click="detailItem = null" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400 flex-shrink-0 ml-4">✕</button>
            </div>

            <!-- 内容 -->
            <div class="mb-6">
              <h4 class="text-sm font-semibold text-slate-600 mb-3">会议内容</h4>
              <div class="bg-slate-50 rounded-xl p-4 text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">{{ detailItem.content || '暂无内容' }}</div>
            </div>

            <!-- 附件 -->
            <div v-if="getAttachments(detailItem).length" class="mb-6">
              <h4 class="text-sm font-semibold text-slate-600 mb-3">会议附件 ({{ getAttachments(detailItem).length }})</h4>
              <div class="space-y-2">
                <div v-for="att in getAttachments(detailItem)" :key="att.id"
                  @click="viewAttachment(att)"
                  class="flex items-center justify-between p-3 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors cursor-pointer group">
                  <div class="flex items-center gap-3 min-w-0">
                    <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                      <span class="text-blue-500 text-lg">{{ getFileIcon(att.type || att.name) }}</span>
                    </div>
                    <div class="min-w-0">
                      <p class="text-sm font-medium text-slate-700 group-hover:text-blue-600 transition-colors truncate">{{ att.name }}</p>
                      <p class="text-xs text-slate-400">{{ formatFileSize(att.size) }}</p>
                    </div>
                  </div>
                  <button class="px-3 py-1.5 bg-blue-500 text-white rounded-lg text-xs hover:bg-blue-600 transition-colors flex-shrink-0 ml-3">
                    查看/下载
                  </button>
                </div>
              </div>
            </div>

            <!-- 标签 -->
            <div v-if="(detailItem.tags || []).length" class="mb-6">
              <h4 class="text-sm font-semibold text-slate-600 mb-2">标签</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="tag in (detailItem.tags || [])" :key="tag" class="px-3 py-1 bg-slate-100 rounded-lg text-xs text-slate-600">{{ tag }}</span>
              </div>
            </div>

            <!-- 问题 -->
            <div v-if="detailItem.questions?.length">
              <h4 class="text-sm font-semibold text-slate-600 mb-3">会议问题</h4>
              <div class="space-y-2">
                <div v-for="(q, i) in detailItem.questions" :key="q.id"
                  class="flex items-start gap-3 p-3 bg-amber-50 rounded-xl">
                  <span class="text-amber-600 font-bold text-sm flex-shrink-0">{{ (i as number) + 1 }}.</span>
                  <span class="text-sm text-slate-700">{{ q.content }}</span>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-3 mt-8 pt-6 border-t border-slate-100">
              <button @click="openForm(detailItem); detailItem = null" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 transition-colors">编辑</button>
              <button @click="detailItem = null" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50">关闭</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ========== 新建/编辑弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showForm = false">
        <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingId ? '编辑会议记录' : '新建会议记录' }}</h3>
          <div class="space-y-4">
            <input v-model="form.title" placeholder="会议标题" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            <input v-model="form.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
            <textarea v-model="form.content" placeholder="会议内容/纪要" rows="5" class="w-full p-3 rounded-lg border border-slate-200 text-sm outline-none resize-none focus:border-blue-500"></textarea>

            <!-- 附件上传 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">会议附件</label>
              <div class="flex items-center gap-3">
                <label class="px-4 py-2 bg-blue-50 text-blue-700 rounded-xl text-sm cursor-pointer hover:bg-blue-100 transition-colors flex items-center gap-2">
                  <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  选择文件
                  <input type="file" multiple class="hidden" @change="handleFileUpload" />
                </label>
                <span class="text-xs text-slate-400">支持 PDF、Word、图片等格式（最大10MB）</span>
              </div>
              <!-- 已选文件列表 -->
              <div v-if="form.attachments.length > 0" class="mt-3 space-y-2">
                <div v-for="att in form.attachments" :key="att.id" class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg">
                  <div class="flex items-center gap-2 min-w-0">
                    <span class="text-lg flex-shrink-0">{{ getFileIcon(att.type || att.name) }}</span>
                    <span class="text-sm text-slate-700 truncate">{{ att.name }}</span>
                    <span class="text-xs text-slate-400 flex-shrink-0">{{ formatFileSize(att.size) }}</span>
                  </div>
                  <button @click="removeAttachment(att.id)" class="w-6 h-6 flex items-center justify-center rounded hover:bg-red-50 text-slate-400 hover:text-red-500 flex-shrink-0">✕</button>
                </div>
              </div>
            </div>

            <!-- 会议问题 -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm font-medium text-slate-700">会议问题</label>
                <button @click="addQuestion" class="text-xs text-blue-600 hover:text-blue-700">+ 添加问题</button>
              </div>
              <div class="space-y-2">
                <div v-for="(q, i) in form.questions" :key="q.id" class="flex items-center gap-2">
                  <span class="text-sm text-slate-400 w-6">{{ i + 1 }}.</span>
                  <input v-model="q.content" placeholder="输入问题内容..." class="flex-1 h-9 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                  <button @click="removeQuestion(i)" class="w-7 h-7 flex items-center justify-center rounded hover:bg-red-50 text-slate-400 hover:text-red-500">✕</button>
                </div>
              </div>
            </div>

            <input v-model="form.tagsStr" placeholder="标签（用逗号分隔）" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="saveArchive" :disabled="!form.title || saving" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50 transition-colors">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)
const search = ref('')
const showForm = ref(false)
const detailItem = ref<any>(null)
const editingId = ref<string | null>(null)
const saving = ref(false)
const loading = ref(true)
const form = ref({
  title: '',
  date: new Date().toISOString().split('T')[0],
  content: '',
  tagsStr: '',
  attachments: [] as Array<{ id: string; name: string; size: number; type: string; data?: string }>,
  questions: [] as Array<{ id: string; content: string }>
})
const archives = ref<any[]>([])

const filteredArchives = computed(() => {
  if (!search.value) return archives.value
  const q = search.value.toLowerCase()
  return archives.value.filter((a: any) =>
    a.title?.toLowerCase().includes(q) ||
    a.content?.toLowerCase().includes(q) ||
    (a.tags || []).some((t: string) => t.toLowerCase().includes(q))
  )
})

// ========== 附件存储（localStorage，后端暂不支持附件） ==========
function getAttachmentsKey(meetingId: string) {
  return `meeting_attachments_${meetingId}`
}

function getAttachments(item: any): any[] {
  if (!item?.id) return []
  // 优先从 localStorage 读取附件
  try {
    const saved = localStorage.getItem(getAttachmentsKey(item.id))
    if (saved) return JSON.parse(saved)
  } catch {}
  // 兼容旧数据格式
  if (item.attachments?.length) return item.attachments
  return []
}

function saveAttachments(meetingId: string, atts: any[]) {
  localStorage.setItem(getAttachmentsKey(meetingId), JSON.stringify(atts))
}

function formatDate(item: any) {
  return item.date || item.created_at?.split('T')[0] || ''
}

// ========== 文件操作 ==========
function getFileIcon(nameOrType: string) {
  const n = nameOrType.toLowerCase()
  if (n.includes('pdf') || n.includes('.pdf')) return '📄'
  if (n.includes('word') || n.includes('.doc')) return '📝'
  if (n.includes('image') || n.match(/\.(png|jpg|jpeg|gif|webp)/)) return '🖼'
  if (n.includes('excel') || n.includes('.xls') || n.includes('.csv')) return '📊'
  if (n.includes('video') || n.includes('.mp4')) return '🎬'
  if (n.includes('zip') || n.includes('.rar')) return '📦'
  return '📎'
}

function formatFileSize(size: number) {
  if (!size) return '0B'
  if (size < 1024) return size + 'B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + 'KB'
  return (size / (1024 * 1024)).toFixed(1) + 'MB'
}

function viewAttachment(att: any) {
  if (att.data) {
    // base64 data URL - open in new tab
    const win = window.open('', '_blank')
    if (win) {
      if (att.data.startsWith('data:image/')) {
        win.document.write(`<html><body style="margin:0;display:flex;align-items:center;justify-content:center;min-height:100vh;background:#f5f5f5"><img src="${att.data}" style="max-width:100%;max-height:100vh;object-fit:contain" /></body></html>`)
      } else {
        // 对于非图片文件，提供下载
        const a = document.createElement('a')
        a.href = att.data
        a.download = att.name
        a.click()
        win.close()
      }
    }
  } else {
    alert('该附件数据不可用，请重新上传')
  }
}

// ========== 数据加载（API + localStorage 降级） ==========
async function loadArchives() {
  loading.value = true
  try {
    const res = await api.get('/meetings', { params: { limit: 200 } })
    if (Array.isArray(res.data)) {
      // 合并 localStorage 中的 tags 和 attachments
      const merged = res.data.map((m: any) => {
        const saved = localStorage.getItem(`meeting_meta_${m.id}`)
        let meta: any = {}
        try { if (saved) meta = JSON.parse(saved) } catch {}
        return {
          ...m,
          date: m.created_at?.split('T')[0] || '',
          author: m.created_by || '未知',
          tags: meta.tags || [],
          questions: meta.questions || [],
        }
      })
      archives.value = merged
      return
    }
  } catch {
    console.warn('后端不可用，使用本地数据')
  }
  // 降级到 localStorage
  const saved = localStorage.getItem('consensus_archives')
  if (saved) {
    try { archives.value = JSON.parse(saved) } catch {}
  }
  loading.value = false
}

// ========== 表单操作 ==========
function openForm(a?: any) {
  if (a) {
    editingId.value = a.id
    form.value = {
      title: a.title || '',
      date: a.date || a.created_at?.split('T')[0] || new Date().toISOString().split('T')[0],
      content: a.content || '',
      tagsStr: (a.tags || []).join(', '),
      attachments: structuredClone(getAttachments(a)),
      questions: a.questions?.length ? structuredClone(a.questions) : [{ id: Date.now().toString(), content: '' }]
    }
  } else {
    editingId.value = null
    form.value = {
      title: '',
      date: new Date().toISOString().split('T')[0],
      content: '',
      tagsStr: '',
      attachments: [],
      questions: [{ id: Date.now().toString(), content: '' }]
    }
  }
  showForm.value = true
}

function openDetail(item: any) {
  detailItem.value = item
}

function addQuestion() {
  form.value.questions.push({ id: Date.now().toString() + '_' + Math.random(), content: '' })
}

function removeQuestion(index: number) {
  form.value.questions.splice(index, 1)
}

// 文件上传处理（限制10MB）
function handleFileUpload(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files) return
  const MAX_SIZE = 10 * 1024 * 1024 // 10MB
  Array.from(files).forEach(file => {
    if (file.size > MAX_SIZE) {
      alert(`文件"${file.name}"超过10MB，请压缩后上传`)
      return
    }
    const reader = new FileReader()
    reader.onload = () => {
      form.value.attachments.push({
        id: 'att_' + Date.now() + '_' + Math.random().toString(36).slice(2),
        name: file.name,
        size: file.size,
        type: file.type,
        data: reader.result as string
      })
    }
    reader.readAsDataURL(file)
  })
  input.value = ''
}

function removeAttachment(id: string) {
  form.value.attachments = form.value.attachments.filter(a => a.id !== id)
}

async function saveArchive() {
  if (!form.value.title) return
  saving.value = true

  const validQuestions = form.value.questions.filter(q => q.content.trim())
  const tags = form.value.tagsStr.split(',').map((t: string) => t.trim()).filter(Boolean)

  try {
    // 尝试通过 API 保存
    const payload = {
      title: form.value.title,
      content: form.value.content,
      question: validQuestions.map(q => q.content).join('\n'),
    }

    let meetingId: string
    if (editingId.value) {
      await api.put(`/meetings/${editingId.value}`, payload)
      meetingId = editingId.value
    } else {
      const res = await api.post('/meetings', payload)
      meetingId = res.data.id
    }

    // 保存附件到 localStorage
    if (meetingId) {
      saveAttachments(meetingId, form.value.attachments)
      // 保存 tags 和 questions 元数据
      localStorage.setItem(`meeting_meta_${meetingId}`, JSON.stringify({
        tags,
        questions: validQuestions,
      }))
    }

    showForm.value = false
    editingId.value = null
    await loadArchives()
  } catch (e: any) {
    console.warn('API 保存失败，降级到本地', e)
    // 降级：保存到 localStorage
    const now = new Date().toISOString()
    const id = editingId.value || ('a_' + Date.now())
    const data = {
      id,
      title: form.value.title,
      date: form.value.date,
      content: form.value.content,
      tags,
      questions: validQuestions,
      author: authStore.user?.name || '未知',
      authorId: authStore.user?.id,
      created_at: now,
      updated_at: now,
    }
    if (editingId.value) {
      const i = archives.value.findIndex(a => a.id === editingId.value)
      if (i >= 0) archives.value[i] = { ...archives.value[i], ...data }
    } else {
      archives.value.unshift(data)
    }
    // 保存到 localStorage
    saveAttachments(id, form.value.attachments)
    localStorage.setItem('consensus_archives', JSON.stringify(archives.value))
    localStorage.setItem(`meeting_meta_${id}`, JSON.stringify({ tags, questions: validQuestions }))
    showForm.value = false
    editingId.value = null
  } finally {
    saving.value = false
  }
}

async function deleteArchive(id: string) {
  if (!confirm('确定删除？此操作不可撤销。')) return
  try {
    await api.delete(`/meetings/${id}`)
  } catch {
    // 降级：从本地删除
    archives.value = archives.value.filter(a => a.id !== id)
    localStorage.setItem('consensus_archives', JSON.stringify(archives.value))
  }
  // 清理附件和元数据
  localStorage.removeItem(getAttachmentsKey(id))
  localStorage.removeItem(`meeting_meta_${id}`)
  await loadArchives()
}

onMounted(async () => {
  await loadArchives()
})
</script>
