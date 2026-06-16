<template>
  <AppLayout current-page="influencer-summary" title="达人汇总统计" subtitle="达人合作数据分析">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100"><p class="text-sm text-slate-500">总记录数</p><p class="text-2xl font-bold text-slate-900 mt-2">{{ stats.total }}</p></div>
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100"><p class="text-sm text-slate-500">合作中</p><p class="text-2xl font-bold text-blue-600 mt-2">{{ stats.cooperating }}</p></div>
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100"><p class="text-sm text-slate-500">已完成</p><p class="text-2xl font-bold text-emerald-600 mt-2">{{ stats.completed }}</p></div>
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100"><p class="text-sm text-slate-500">总合作金额</p><p class="text-2xl font-bold text-amber-600 mt-2">¥{{ formatNum(stats.totalAmount) }}</p></div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
        <h3 class="font-bold text-slate-800 mb-4">平台分布</h3>
        <div class="space-y-3">
          <div v-for="p in platformStats" :key="p.name" class="flex items-center gap-3">
            <span class="w-16 text-sm text-slate-600">{{ p.name }}</span>
            <div class="flex-1 h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-blue-500 rounded-full" :style="{ width: p.pct + '%' }" /></div>
            <span class="text-sm font-medium text-slate-700">{{ p.count }}条</span>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const records = ref<any[]>([])
const stats = computed(() => ({
  total: records.value.length,
  cooperating: records.value.filter(r => r.status === '已合作' || r.status === '洽谈中').length,
  completed: records.value.filter(r => r.status === '已完成').length,
  totalAmount: records.value.reduce((s, r) => s + (parseFloat(r.amount) || 0), 0)
}))
const platformStats = computed(() => {
  const map: any = {}
  records.value.forEach(r => { map[r.platform] = (map[r.platform] || 0) + 1 })
  return Object.entries(map).map(([name, count]: any) => ({ name, count, pct: stats.value.total > 0 ? Math.round(count / stats.value.total * 100) : 0 }))
})

function formatNum(n: number) { return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toLocaleString() }

onMounted(() => {
  const saved = localStorage.getItem('influencer_records')
  if (saved) { try { records.value = JSON.parse(saved) } catch {} }
})
</script>
