<template>
  <div class="min-h-screen bg-[#f5f6f7]">
    <header class="bg-white/80 backdrop-blur-md border-b border-slate-100 px-4 py-4 sticky top-0 z-10">
      <div class="max-w-[1600px] mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <button @click="$router.push('/reports')" class="p-2 hover:bg-slate-100 rounded-lg"><span class="text-slate-600">←</span></button>
          <div>
            <h1 class="text-xl font-bold text-slate-900 tracking-tight">数据统计</h1>
            <p class="text-sm text-slate-500">查看营业数据和任务统计</p>
          </div>
        </div>
        <select v-model="timeRange" class="w-[140px] h-11 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 px-3 text-sm outline-none">
          <option value="week">最近7天</option>
          <option value="month">最近30天</option>
          <option value="quarter">最近90天</option>
        </select>
      </div>
    </header>

    <div class="max-w-[1600px] mx-auto px-4 py-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gradient-to-br from-blue-600 via-blue-500 to-cyan-500 text-white shadow-lg rounded-2xl p-5 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
          <div class="relative flex items-center justify-between">
            <div><p class="text-blue-100 text-sm font-medium">目标营业额</p><p class="text-2xl font-bold mt-2">{{ formatMoney(stats.totalTarget) }}</p></div>
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center"><span>🎯</span></div>
          </div>
        </div>
        <div class="bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-500 text-white shadow-lg rounded-2xl p-5 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
          <div class="relative flex items-center justify-between">
            <div><p class="text-emerald-100 text-sm font-medium">已完成</p><p class="text-2xl font-bold mt-2">{{ formatMoney(stats.totalCompleted) }}</p></div>
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center"><span>💵</span></div>
          </div>
        </div>
        <div class="bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500 text-white shadow-lg rounded-2xl p-5 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
          <div class="relative flex items-center justify-between">
            <div><p class="text-purple-100 text-sm font-medium">完成率</p><p class="text-2xl font-bold mt-2">{{ stats.completionRate }}%</p></div>
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center"><span>📈</span></div>
          </div>
        </div>
        <div class="bg-gradient-to-br from-amber-600 via-amber-500 to-orange-500 text-white shadow-lg rounded-2xl p-5 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full blur-xl -translate-y-1/2 translate-x-1/2" />
          <div class="relative flex items-center justify-between">
            <div><p class="text-amber-100 text-sm font-medium">任务完成</p><p class="text-2xl font-bold mt-2">{{ stats.completedTasks }}/{{ stats.taskCount }}</p></div>
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center"><span>✅</span></div>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-[1600px] mx-auto px-4 pb-8">
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="px-5 pb-4 bg-gradient-to-r from-slate-50 to-transparent pt-5">
          <h2 class="text-lg font-bold text-slate-900">每日数据明细</h2>
        </div>
        <div class="px-5">
          <div v-if="dailyData.length === 0" class="text-center py-16">
            <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4"><span class="text-4xl">📈</span></div>
            <p class="text-slate-500">暂无数据</p>
          </div>
          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead><tr class="border-b border-slate-100"><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">日期</th><th class="px-4 py-3 text-right text-sm font-semibold text-slate-600">目标</th><th class="px-4 py-3 text-right text-sm font-semibold text-slate-600">完成</th><th class="px-4 py-3 text-right text-sm font-semibold text-slate-600">完成率</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">任务数</th></tr></thead>
              <tbody>
                <tr v-for="day in dailyData" :key="day.date" class="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                  <td class="px-4 py-4"><div class="flex items-center gap-3"><div class="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center"><span>📅</span></div><span class="font-medium text-slate-900">{{ day.date }}</span></div></td>
                  <td class="px-4 py-4 text-right"><span class="text-slate-700 font-medium">{{ formatMoney(day.target) }}</span></td>
                  <td class="px-4 py-4 text-right"><span :class="['font-medium', getRate(day) > 0 && getRateColor(day) === 'emerald' ? 'text-emerald-600' : getRateColor(day) === 'blue' ? 'text-blue-600' : 'text-slate-700']">{{ formatMoney(day.completed) }}</span></td>
                  <td class="px-4 py-4"><div class="flex items-center justify-end gap-3"><div class="w-20 h-2 bg-slate-100 rounded-full overflow-hidden"><div :class="['h-full rounded-full transition-all duration-500', getBarColor(getRate(day))]" :style="{ width: Math.min(getRate(day), 100) + '%' }" /></div><span :class="['font-semibold', getRate(day) >= 100 ? 'text-emerald-600' : getRate(day) >= 80 ? 'text-blue-600' : 'text-amber-600']">{{ getRate(day) }}%</span></div></td>
                  <td class="px-4 py-4 text-center"><span class="px-3 py-1 text-xs font-medium rounded-lg" :class="getRate(day) >= 100 ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-600'">{{ day.tasks }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/api'

const timeRange = ref('week')
const stats = ref({ totalTarget: 0, totalCompleted: 0, completionRate: 0, taskCount: 0, completedTasks: 0 })
const dailyData = ref<any[]>([])

function formatMoney(amount: number) {
  if (amount >= 10000) return `¥${(amount / 10000).toFixed(1)}万`
  return `¥${amount.toLocaleString()}`
}

function getRate(day: any) { return day.target > 0 ? Math.round(day.completed / day.target * 100) : 0 }
function getRateColor(day: any) { const r = getRate(day); return r >= 100 ? 'emerald' : r >= 80 ? 'blue' : 'default' }
function getBarColor(rate: number) { return rate >= 100 ? 'bg-emerald-500' : rate >= 80 ? 'bg-blue-500' : 'bg-amber-500' }

async function loadStatistics() {
  try {
    const res = await api.get('/tasks')
    if (!res.data) return
    const data = res.data
    const now = new Date()
    let startDate = new Date()
    if (timeRange.value === 'month') startDate.setMonth(now.getMonth() - 1)
    else if (timeRange.value === 'quarter') startDate.setMonth(now.getMonth() - 3)
    else startDate.setDate(now.getDate() - 7)

    const dates = Object.keys(data).sort().filter(d => new Date(d) >= startDate)
    let totalTarget = 0, totalCompleted = 0, taskCount = 0, completedTasks = 0
    const daily: any[] = []
    dates.forEach(date => {
      const dayData = data[date]
      if (dayData) {
        totalTarget += dayData.targetAmount || 0
        totalCompleted += dayData.completedAmount || 0
        if (dayData.tasks) {
          taskCount += dayData.tasks.length
          completedTasks += dayData.tasks.filter((t: any) => t.status === 'completed').length
        }
        daily.push({ date, target: dayData.targetAmount || 0, completed: dayData.completedAmount || 0, tasks: dayData.tasks?.length || 0 })
      }
    })
    stats.value = { totalTarget, totalCompleted, completionRate: totalTarget > 0 ? Math.round(totalCompleted / totalTarget * 100) : 0, taskCount, completedTasks }
    dailyData.value = daily
  } catch (e) { console.error('加载统计数据失败:', e) }
}

watch(timeRange, loadStatistics)
onMounted(loadStatistics)
</script>
