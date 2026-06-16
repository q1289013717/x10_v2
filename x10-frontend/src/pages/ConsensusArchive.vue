<template>
  <AppLayout current-page="consensus-archive" title="共识档案" subtitle="会议纪要与共识管理">
    <template #actions>
      <button @click="openForm()" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">+ 新建会议记录</button>
    </template>
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <div class="mb-4 relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索会议记录..." class="w-full pl-11 pr-4 h-11 rounded-xl border border-slate-200 bg-white text-sm outline-none" /></div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="a in filteredArchives" :key="a.id" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-slate-800 truncate">{{ a.title }}</h3>
              <p class="text-xs text-slate-400 mt-1">📅 {{ a.date }} · 👤 {{ a.author }}</p>
            </div>
            <div class="flex gap-1 flex-shrink-0">
              <button @click="openForm(a)" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-blue-50 text-blue-500 hover:text-blue-600 text-sm">✎</button>
              <button @click="deleteArchive(a.id)" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-50 text-red-400 hover:text-red-600 text-sm">🗑</button>
            </div>
          </div>
          <p class="text-sm text-slate-600 line-clamp-3">{{ a.content }}</p>

          <!-- 附件列表 -->
          <div v-if="a.attachments?.length" class="mt-3 flex flex-wrap gap-2">
            <div v-for="att in a.attachments" :key="att.id" class="flex items-center gap-1.5 px-2.5 py-1 bg-blue-50 rounded-lg text-xs text-blue-700">
              <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
              <span class="truncate max-w-[120px]">{{ att.name }}</span>
              <span class="text-blue-400">{{ formatFileSize(att.size) }}</span>
            </div>
          </div>

          <div class="flex flex-wrap gap-1 mt-3">
            <span v-for="tag in a.tags" :key="tag" class="px-2 py-0.5 bg-slate-100 rounded text-xs text-slate-500">{{ tag }}</span>
          </div>

          <!-- 会议问题 -->
          <div v-if="a.questions?.length" class="mt-3 pt-3 border-t border-slate-100">
            <p class="text-xs font-medium text-slate-500 mb-2">会议问题</p>
            <div v-for="(q, i) in a.questions" :key="q.id" class="text-sm text-slate-600 mb-1">
              {{ (i as number) + 1 }}. {{ q.content }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredArchives.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📖</span><p>暂无会议记录</p></div>
    </div>

    <!-- 新建/编辑弹窗 -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showForm = false">
        <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingId ? '编辑会议记录' : '新建会议记录' }}</h3>
          <div class="space-y-4">
            <input v-model="form.title" placeholder="会议标题" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <input v-model="form.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <textarea v-model="form.content" placeholder="会议内容/纪要" rows="5" class="w-full p-3 rounded-lg border border-slate-200 text-sm outline-none resize-none"></textarea>

            <!-- 附件上传 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">会议附件</label>
              <div class="flex items-center gap-3">
                <label class="px-4 py-2 bg-blue-50 text-blue-700 rounded-xl text-sm cursor-pointer hover:bg-blue-100 transition-colors flex items-center gap-2">
                  <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  选择文件
                  <input type="file" multiple class="hidden" @change="handleFileUpload" />
                </label>
                <span class="text-xs text-slate-400">支持 PDF、Word、图片等格式</span>
              </div>
              <!-- 已选文件列表 -->
              <div v-if="form.attachments.length > 0" class="mt-3 space-y-2">
                <div v-for="att in form.attachments" :key="att.id" class="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg">
                  <div class="flex items-center gap-2 min-w-0">
                    <svg class="w-4 h-4 text-slate-400 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
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
                  <input v-model="q.content" placeholder="输入问题内容..." class="flex-1 h-9 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
                  <button @click="removeQuestion(i)" class="w-7 h-7 flex items-center justify-center rounded hover:bg-red-50 text-slate-400 hover:text-red-500">✕</button>
                </div>
              </div>
            </div>

            <input v-model="form.tagsStr" placeholder="标签（用逗号分隔）" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="saveArchive" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">保存</button>
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

const authStore = useAuthStore()
const search = ref('')
const showForm = ref(false)
const editingId = ref<string | null>(null)
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
  return archives.value.filter(a => a.title.includes(search.value) || a.content.includes(search.value))
})

function openForm(a?: any) {
  if (a) {
    editingId.value = a.id
    form.value = {
      title: a.title,
      date: a.date,
      content: a.content,
      tagsStr: (a.tags || []).join(', '),
      attachments: a.attachments ? JSON.parse(JSON.stringify(a.attachments)) : [],
      questions: a.questions ? JSON.parse(JSON.stringify(a.questions)) : [{ id: Date.now().toString(), content: '' }]
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

function addQuestion() {
  form.value.questions.push({ id: Date.now().toString() + '_' + Math.random(), content: '' })
}
function removeQuestion(index: number) {
  form.value.questions.splice(index, 1)
}

// 文件上传处理
function handleFileUpload(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files) return
  Array.from(files).forEach(file => {
    const reader = new FileReader()
    reader.onload = () => {
      form.value.attachments.push({
        id: 'att_' + Date.now() + '_' + Math.random().toString(36).slice(2),
        name: file.name,
        size: file.size,
        type: file.type,
        data: reader.result as string // base64 for localStorage persistence
      })
    }
    reader.readAsDataURL(file)
  })
  input.value = '' // reset
}

function removeAttachment(id: string) {
  form.value.attachments = form.value.attachments.filter(a => a.id !== id)
}

function formatFileSize(size: number) {
  if (size < 1024) return size + 'B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + 'KB'
  return (size / (1024 * 1024)).toFixed(1) + 'MB'
}

function saveArchive() {
  if (!form.value.title) return
  const validQuestions = form.value.questions.filter(q => q.content.trim())
  const data = {
    ...form.value,
    tags: form.value.tagsStr.split(',').map((t: string) => t.trim()).filter(Boolean),
    questions: validQuestions,
    author: authStore.user?.name || '未知',
    authorId: authStore.user?.id
  }
  if (editingId.value) {
    const i = archives.value.findIndex(a => a.id === editingId.value)
    if (i >= 0) archives.value[i] = { ...data, id: editingId.value, updatedAt: new Date().toISOString() }
  } else {
    archives.value.unshift({ ...data, id: 'a_' + Date.now(), createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() })
  }
  save()
  showForm.value = false
  editingId.value = null
}

function deleteArchive(id: string) { if (!confirm('确定删除？')) return; archives.value = archives.value.filter(a => a.id !== id); save() }
function save() { localStorage.setItem('consensus_archives', JSON.stringify(archives.value)) }

onMounted(() => {
  const saved = localStorage.getItem('consensus_archives')
  if (saved) { try { archives.value = JSON.parse(saved) } catch {} }
})
</script>
