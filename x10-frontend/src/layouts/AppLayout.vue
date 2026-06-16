<template>
  <div class="min-h-screen bg-[#f5f6f7] flex">
    <!-- ==================== 桌面端侧边栏 ==================== -->
    <Sidebar v-if="!isMobile" :current-page="currentPage" @navigate="handleNavigate" />

    <!-- ==================== 主内容区 ==================== -->
    <div class="flex-1 flex flex-col min-h-screen min-w-0" :class="{ 'pb-16': isMobile }">
      <!-- 顶部导航栏 (有内容时才显示) -->
      <header v-if="showBack || title || subtitle || $slots.title || $slots.actions" class="bg-white/80 backdrop-blur-xl border-b border-slate-100 px-4 py-3 lg:px-6 sticky top-0 z-40">
        <div class="flex items-center gap-3 max-w-[1600px] mx-auto">
          <!-- 返回按钮 -->
          <button
            v-if="showBack"
            @click="goBack"
            class="flex items-center justify-center w-9 h-9 rounded-xl hover:bg-slate-100 text-slate-500 hover:text-slate-700 flex-shrink-0 transition-colors"
            title="返回"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>

          <!-- 标题区域 -->
          <div class="flex-1 min-w-0">
            <slot name="title">
              <h1 v-if="!editingTitle" class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight truncate cursor-pointer hover:text-blue-600 transition-colors" @click="startEditTitle" :title="titleEditable ? '点击编辑标题' : ''">{{ title }}</h1>
              <input v-else ref="titleInputRef" v-model="localTitle" @blur="saveTitle" @keyup.enter="saveTitle" @keyup.escape="cancelEditTitle" class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight bg-transparent border-b-2 border-blue-500 outline-none px-1 w-full" />
              <p v-if="subtitle && !editingSubtitle" class="text-xs text-slate-400 mt-0.5 truncate cursor-pointer hover:text-blue-500 transition-colors" @click="startEditSubtitle" :title="subtitleEditable ? '点击编辑副标题' : ''">{{ subtitle }}</p>
              <input v-else-if="editingSubtitle" ref="subtitleInputRef" v-model="localSubtitle" @blur="saveSubtitle" @keyup.enter="saveSubtitle" @keyup.escape="cancelEditSubtitle" class="text-xs bg-transparent border-b-2 border-blue-500 outline-none px-1 w-full mt-0.5 text-slate-600" />
            </slot>
          </div>

          <!-- 右侧操作区域 -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <slot name="actions" />
          </div>
        </div>
      </header>

      <!-- 内容区 -->
      <main class="flex-1">
        <slot />
      </main>

      <!-- ==================== 移动端底部导航 ==================== -->
      <BottomNav v-if="isMobile" :current-page="currentPage" @navigate="handleNavigate" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import BottomNav from '@/components/BottomNav.vue'

const props = withDefaults(defineProps<{
  currentPage: string
  title?: string
  subtitle?: string
  showBack?: boolean
  backFallback?: string
  titleEditable?: boolean
  subtitleEditable?: boolean
}>(), {
  title: '',
  subtitle: '',
  showBack: true,
  backFallback: 'home',
  titleEditable: true,
  subtitleEditable: true,
})

const emit = defineEmits<{
  (e: 'update:title', value: string): void
  (e: 'update:subtitle', value: string): void
}>()

const router = useRouter()
const isMobile = ref(false)

// 标题编辑状态
const editingTitle = ref(false)
const localTitle = ref(props.title)
const titleInputRef = ref<HTMLInputElement | null>(null)

// 副标题编辑状态
const editingSubtitle = ref(false)
const localSubtitle = ref(props.subtitle)
const subtitleInputRef = ref<HTMLInputElement | null>(null)

function startEditTitle() {
  if (!props.titleEditable) return
  localTitle.value = props.title
  editingTitle.value = true
  nextTick(() => {
    titleInputRef.value?.focus()
    titleInputRef.value?.select()
  })
}

function saveTitle() {
  if (!editingTitle.value) return
  const newVal = localTitle.value.trim()
  if (newVal && newVal !== props.title) {
    emit('update:title', newVal)
    // 持久化到 localStorage
    try {
      const key = `page_subtitle_${props.currentPage}`
      const saved = JSON.parse(localStorage.getItem(key) || '{}')
      saved.customTitle = newVal
      localStorage.setItem(key, JSON.stringify(saved))
    } catch {}
  }
  editingTitle.value = false
}

function cancelEditTitle() {
  localTitle.value = props.title
  editingTitle.value = false
}

function startEditSubtitle() {
  if (!props.subtitleEditable) return
  localSubtitle.value = props.subtitle
  editingSubtitle.value = true
  nextTick(() => {
    subtitleInputRef.value?.focus()
    subtitleInputRef.value?.select()
  })
}

function saveSubtitle() {
  if (!editingSubtitle.value) return
  const newVal = localSubtitle.value.trim()
  emit('update:subtitle', newVal)
  // 持久化到 localStorage（或发送到后端）
  try {
    const key = `page_subtitle_${props.currentPage}`
    const saved = JSON.parse(localStorage.getItem(key) || '{}')
    saved.customSubtitle = newVal
    localStorage.setItem(key, JSON.stringify(saved))
  } catch {}
  editingSubtitle.value = false
}

function cancelEditSubtitle() {
  localSubtitle.value = props.subtitle
  editingSubtitle.value = false
}

function checkMobile() {
  isMobile.value = window.innerWidth < 1024
}

function handleNavigate(pageId: string) {
  router.push({ name: pageId }).catch(() => {})
}

function goBack() {
  // 如果有浏览器历史就返回，否则跳到 fallback
  if (window.history.length > 2) {
    router.back()
  } else {
    router.push({ name: props.backFallback }).catch(() => {})
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>
