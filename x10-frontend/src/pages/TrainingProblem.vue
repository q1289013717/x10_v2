<template>
  <AppLayout current-page="training" title="难题库" subtitle="疑难问题收集">
    <div class="max-w-3xl mx-auto px-4 py-8">
      <div class="mb-6 flex gap-2">
        <input v-model="search" placeholder="搜索难题..." class="flex-1 h-11 px-4 rounded-xl border border-slate-200 bg-white text-sm outline-none focus:border-blue-500" />
        <button @click="showAdd = true" class="px-4 py-2 bg-amber-600 text-white rounded-xl text-sm hover:bg-amber-700">+ 添加难题</button>
      </div>
      <div class="space-y-4">
        <div v-if="filteredProblems.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📋</span><p>暂无难题记录</p></div>
        <div v-for="p in filteredProblems" :key="p.id" class="bg-white rounded-xl p-4 shadow-sm border border-slate-100">
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1"><h3 class="font-medium text-slate-800">{{ p.title }}</h3><p class="text-sm text-slate-500 mt-2">{{ p.answer }}</p></div>
            <button @click="removeProblem(p.id)" class="text-red-500 hover:text-red-600 text-sm">🗑</button>
          </div>
        </div>
      </div>
      <!-- 添加弹窗 -->
      <Teleport to="body">
        <div v-if="showAdd" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showAdd = false">
          <div class="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <h3 class="font-bold text-slate-800 mb-4">添加难题</h3>
            <input v-model="newTitle" placeholder="问题描述" class="w-full h-11 px-4 rounded-xl border border-slate-200 bg-slate-50 text-sm outline-none mb-3" />
            <textarea v-model="newAnswer" placeholder="解答" rows="4" class="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 text-sm outline-none resize-none mb-4" />
            <div class="flex gap-3"><button @click="showAdd = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="addProblem" :disabled="!newTitle.trim()" class="flex-1 py-2.5 bg-amber-600 text-white rounded-xl text-sm disabled:opacity-50">保存</button></div>
          </div>
        </div>
      </Teleport>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const search = ref('')
const showAdd = ref(false)
const newTitle = ref('')
const newAnswer = ref('')
const problems = ref<{ id: number; title: string; answer: string }[]>([])

const filteredProblems = computed(() => {
  if (!search.value) return problems.value
  return problems.value.filter(p => p.title.includes(search.value) || p.answer.includes(search.value))
})

function addProblem() {
  if (!newTitle.value.trim()) return
  problems.value.unshift({ id: Date.now(), title: newTitle.value, answer: newAnswer.value })
  save()
  newTitle.value = ''; newAnswer.value = ''; showAdd.value = false
}

function removeProblem(id: number) { problems.value = problems.value.filter(p => p.id !== id); save() }

function save() { localStorage.setItem('training_problems', JSON.stringify(problems.value)) }

onMounted(() => {
  const saved = localStorage.getItem('training_problems')
  if (saved) { try { problems.value = JSON.parse(saved) } catch {} }
})
</script>
