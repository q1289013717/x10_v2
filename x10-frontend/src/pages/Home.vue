<template>
  <AppLayout current-page="home" :show-back="false">
    <div>
      <!-- 顶部欢迎区域 — 巨量引擎风格 -->
      <div class="bg-gradient-to-br from-[#1a1f2e] via-[#1e3a5f] to-[#1a1f2e] text-white relative overflow-hidden">
        <div class="absolute inset-0">
          <div class="absolute top-10 left-10 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl" />
          <div class="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] border border-white/5 rounded-full" />
        </div>
        <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 class="text-2xl md:text-3xl font-bold tracking-tight">
                {{ greeting }}，{{ currentUser?.name || currentUser?.account || '管理员' }}
              </h1>
              <p class="text-slate-300 mt-2">{{ todayStr }}</p>
            </div>
            <div class="flex gap-3">
              <button @click="$router.push({ name: 'calendar' })" class="border border-white/20 text-white hover:bg-white/10 hover:border-white/30 h-11 px-5 rounded-xl transition-all flex items-center gap-2">
                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                查看日历
              </button>
              <button @click="$router.push({ name: 'task-edit', query: { date: todayDate } })" class="bg-blue-600 hover:bg-blue-700 h-11 px-5 rounded-xl font-medium shadow-lg shadow-blue-600/30 transition-all flex items-center gap-2">
                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                新建任务
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 统计卡片 — 大厂风格 -->
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <!-- 今日目标 — 同步成长日程数据 -->
          <div class="bg-white rounded-2xl shadow-lg border border-slate-100 hover:shadow-xl hover:border-slate-200 transition-all duration-200 group min-w-0">
            <div class="p-5">
              <div class="flex items-center justify-between mb-4">
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-slate-500 truncate">今日目标</p>
                  <p class="text-2xl font-bold text-slate-900 mt-2 truncate">¥{{ formatMoney(stats.todayTarget) }}</p>
                </div>
                <div class="w-12 h-12 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2 group-hover:scale-105 transition-transform">
                  <svg class="w-6 h-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                </div>
              </div>
              <div class="mt-2">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs text-slate-500">完成进度</span>
                  <span :class="['text-xs font-medium', todayPercent >= 100 ? 'text-emerald-600' : todayPercent >= 70 ? 'text-cyan-600' : todayPercent >= 40 ? 'text-amber-600' : 'text-red-600']">{{ todayPercent }}%</span>
                </div>
                <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div :class="['h-full rounded-full transition-all duration-500', todayPercent >= 100 ? 'bg-emerald-500' : todayPercent >= 70 ? 'bg-cyan-500' : todayPercent >= 40 ? 'bg-amber-500' : 'bg-red-500']" :style="{ width: `${todayPercent}%` }" />
                </div>
                <p class="text-xs text-slate-500 mt-1 truncate">已完成 ¥{{ formatMoney(stats.todayCompleted) }}</p>
                <p v-if="stats.monthlyTarget > 0 && todayPercent < 100" class="text-xs font-medium text-red-500 mt-0.5 truncate">未完成 {{ 100 - todayPercent }}%</p>
                <!-- 月度汇总 -->
                <div class="mt-3 pt-3 border-t border-slate-100">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-slate-400">本月目标</span>
                    <span class="text-xs font-semibold text-slate-700">¥{{ formatMoney(stats.monthlyTarget) }}</span>
                  </div>
                  <div class="flex items-center justify-between mt-1">
                    <span class="text-xs text-slate-400">日均目标</span>
                    <span class="text-xs font-medium text-blue-600">¥{{ formatMoney(stats.dailyAvgTarget) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 本周进度 -->
          <div class="bg-white rounded-2xl shadow-lg border border-slate-100 hover:shadow-xl hover:border-slate-200 transition-all duration-200 group min-w-0">
            <div class="p-5">
              <div class="flex items-center justify-between mb-4">
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-slate-500 truncate">本周进度</p>
                  <p class="text-2xl font-bold text-emerald-600 mt-2 truncate">{{ weekPercent }}%</p>
                </div>
                <div class="w-12 h-12 bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2 group-hover:scale-105 transition-transform">
                  <svg class="w-6 h-6 text-emerald-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
                </div>
              </div>
              <div class="mt-2">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs text-slate-500">目标完成</span>
                  <span class="text-xs font-medium text-emerald-600">¥{{ (stats.weekCompleted / 10000).toFixed(1) }}万</span>
                </div>
                <div class="h-2 bg-emerald-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-full transition-all duration-500" :style="{ width: `${weekPercent}%` }" />
                </div>
                <p class="text-xs text-slate-500 mt-2 truncate">目标 ¥{{ (stats.weekTarget / 10000).toFixed(1) }}万</p>
              </div>
            </div>
          </div>

          <!-- 待办任务 -->
          <div class="bg-white rounded-2xl shadow-lg border border-slate-100 hover:shadow-xl hover:border-slate-200 transition-all duration-200 group min-w-0">
            <div class="p-5">
              <div class="flex items-center justify-between mb-4">
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-slate-500 truncate">待办任务</p>
                  <p class="text-2xl font-bold text-amber-600 mt-2 truncate">{{ stats.pendingTasks }}</p>
                </div>
                <div class="w-12 h-12 bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2 group-hover:scale-105 transition-transform">
                  <svg class="w-6 h-6 text-amber-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                </div>
              </div>
              <div class="mt-4 flex items-center justify-between">
                <span class="inline-flex items-center px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-medium gap-1">
                  <svg class="w-3 h-3 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  已完成 {{ stats.completedTasks }}
                </span>
                <button @click="$router.push({ name: 'tasks' })" class="text-blue-600 hover:text-blue-700 hover:bg-blue-50 text-sm font-medium px-2 py-1 rounded transition-colors flex items-center gap-1">
                  查看全部
                  <svg class="w-4 h-4 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 风险任务 -->
          <div class="bg-white rounded-2xl shadow-lg border border-slate-100 hover:shadow-xl hover:border-slate-200 transition-all duration-200 group min-w-0">
            <div class="p-5">
              <div class="flex items-center justify-between mb-4">
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-slate-500 truncate">风险任务</p>
                  <p class="text-2xl font-bold text-red-600 mt-2 truncate">{{ stats.riskTasks }}</p>
                </div>
                <div class="w-12 h-12 bg-gradient-to-br from-red-50 to-red-100 rounded-xl flex items-center justify-center flex-shrink-0 ml-2 group-hover:scale-105 transition-transform">
                  <svg class="w-6 h-6 text-red-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                </div>
              </div>
              <div class="mt-4">
                <button @click="$router.push({ name: 'tasks' })" class="w-full h-9 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-1">
                  查看详情
                  <svg class="w-4 h-4 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 管理员告警面板 -->
      <div v-if="isAdmin" class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <!-- API 加载失败 -->
        <div v-if="alertsError" class="bg-red-50 border border-red-200 rounded-xl p-4">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-lg">❌</span>
            <h3 class="font-bold text-red-800">告警数据加载失败</h3>
          </div>
          <p class="text-sm text-red-600">{{ alertsError }}</p>
          <button @click="loadAlerts" class="mt-2 px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm hover:bg-red-200 transition-colors">重新加载</button>
        </div>

        <!-- 正常告警区域 -->
        <div v-else-if="alerts" class="space-y-3">
          <!-- 日报未提交告警 -->
          <div v-if="alerts.daily_missing?.length" class="bg-orange-50 border border-orange-200 rounded-xl p-4">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-lg">⚠️</span>
              <h3 class="font-bold text-orange-800">昨日日报未提交提醒</h3>
              <span class="bg-orange-200 text-orange-800 text-xs px-2 py-0.5 rounded-full font-medium">{{ alerts.daily_missing.length }}人</span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="u in alerts.daily_missing" :key="u.user_id" class="inline-flex items-center gap-1 px-3 py-1.5 bg-white border border-orange-200 rounded-lg text-sm">
                <span :class="u.role === 'admin' || u.role === '集团管理员' ? 'text-red-600' : 'text-slate-600'">{{ u.role === 'admin' || u.role === '集团管理员' ? '👤' : '👥' }}</span>
                {{ u.name }}
                <span class="text-xs text-slate-400">({{ u.date }})</span>
              </span>
            </div>
          </div>

          <!-- 周报未提交告警 -->
          <div v-if="alerts.weekly_missing?.length" class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-lg">📊</span>
              <h3 class="font-bold text-amber-800">本周周报未提交提醒</h3>
              <span class="bg-amber-200 text-amber-800 text-xs px-2 py-0.5 rounded-full font-medium">{{ alerts.weekly_missing.length }}人</span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="u in alerts.weekly_missing" :key="u.user_id" class="inline-flex items-center gap-1 px-3 py-1.5 bg-white border border-amber-200 rounded-lg text-sm">
                {{ u.name }}
                <span class="text-xs text-slate-400">({{ u.week }})</span>
              </span>
            </div>
          </div>

          <!-- 任务配额异常告警 -->
          <div v-if="alerts.task_quota_alert?.length" class="bg-red-50 border border-red-200 rounded-xl p-4">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-lg">🚨</span>
              <h3 class="font-bold text-red-800">今日任务配额异常</h3>
              <span class="bg-red-200 text-red-800 text-xs px-2 py-0.5 rounded-full font-medium">{{ alerts.task_quota_alert.length }}人未达标（&lt;60条）</span>
            </div>
            <div class="space-y-2">
              <div v-for="u in alerts.task_quota_alert" :key="u.user_id" :class="['flex items-center justify-between px-3 py-2 rounded-lg text-sm', u.level === 'critical' ? 'bg-red-100 border border-red-300' : u.level === 'warning' ? 'bg-orange-100 border border-orange-300' : 'bg-white border border-slate-200']">
                <div class="flex items-center gap-2">
                  <span>{{ u.level === 'critical' ? '🔴' : u.level === 'warning' ? '🟡' : '⚪' }}</span>
                  <span class="font-medium text-slate-800">{{ u.name }}</span>
                  <span class="text-xs text-slate-500">{{ u.company }}</span>
                </div>
                <div class="flex items-center gap-3">
                  <span class="text-slate-600">已列 <b :class="u.level === 'critical' ? 'text-red-600' : 'text-orange-600'">{{ u.task_count }}</b> 条</span>
                  <span class="text-xs text-slate-500">差 <b class="text-red-600">{{ u.shortfall }}</b> 条</span>
                  <div class="w-20 h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div :class="['h-full rounded-full', u.level === 'critical' ? 'bg-red-500' : u.level === 'warning' ? 'bg-orange-500' : 'bg-emerald-500']" :style="{ width: `${Math.min((u.task_count / u.min_required) * 100, 100)}%` }" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 一切正常 -->
          <div v-if="!alerts.daily_missing?.length && !alerts.weekly_missing?.length && !alerts.task_quota_alert?.length" class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
            <div class="flex items-center gap-2">
              <span class="text-lg">✅</span>
              <h3 class="font-bold text-emerald-800">一切正常</h3>
              <span class="text-sm text-emerald-600 ml-2">昨日日报全员提交、本周周报全员提交、今日任务配额全部达标</span>
            </div>
          </div>
        </div>

        <!-- 加载中 -->
        <div v-else class="bg-slate-50 border border-slate-200 rounded-xl p-4 animate-pulse">
          <div class="flex items-center gap-2">
            <div class="w-5 h-5 bg-slate-200 rounded-full" />
            <div class="h-4 bg-slate-200 rounded w-32" />
          </div>
        </div>
      </div>
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- 最近任务 -->
          <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="flex items-center justify-between px-5 pt-5 pb-4">
              <h3 class="text-lg font-bold text-slate-900">最近任务</h3>
              <button @click="$router.push({ name: 'tasks' })" class="text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg text-sm font-medium px-3 py-1.5 transition-colors flex items-center gap-1">
                查看全部
                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </button>
            </div>
            <div class="px-5 pb-5">
              <!-- 空状态 -->
              <div v-if="recentTasks.length === 0" class="text-center py-12">
                <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                </div>
                <p class="text-slate-500">暂无任务数据</p>
                <button @click="$router.push({ name: 'task-edit', query: { date: todayDate } })" class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg inline-flex items-center gap-2 transition-colors">
                  <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  添加任务
                </button>
              </div>
              <!-- 任务列表 -->
              <div v-else class="space-y-3">
                <div
                  v-for="(day, idx) in recentTasks.slice(0, 5)"
                  :key="idx"
                  @click="$router.push({ name: 'calendar' })"
                  class="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 hover:shadow-sm transition-all duration-200 cursor-pointer group"
                >
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform">
                      <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                    </div>
                    <div>
                      <p class="font-medium text-slate-900">{{ day.date }}</p>
                      <p class="text-sm text-slate-500">{{ day.tasks?.length || 0 }} 个任务</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-blue-600">¥{{ ((day.completedAmount || 0) / 10000).toFixed(1) }}万</p>
                    <p class="text-xs text-slate-500">目标 ¥{{ ((day.targetAmount || 0) / 10000).toFixed(1) }}万</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 快捷操作 -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="px-5 pt-5 pb-4">
              <h3 class="text-lg font-bold text-slate-900">快捷操作</h3>
            </div>
            <div class="px-5 pb-5 space-y-2">
              <button @click="$router.push({ name: 'calendar' })" class="w-full flex items-center justify-start h-12 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50 transition-all group px-3">
                <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center mr-3 group-hover:bg-blue-100 transition-colors">
                  <svg class="w-5 h-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                </div>
                <div class="text-left">
                  <p class="font-medium text-slate-900">X10成长日程</p>
                  <p class="text-xs text-slate-500">查看每日任务安排</p>
                </div>
              </button>

              <button @click="$router.push({ name: 'tasks' })" class="w-full flex items-center justify-start h-12 rounded-xl border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50 transition-all group px-3">
                <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center mr-3 group-hover:bg-emerald-100 transition-colors">
                  <svg class="w-5 h-5 text-emerald-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="text-left">
                  <p class="font-medium text-slate-900">任务列表</p>
                  <p class="text-xs text-slate-500">管理所有任务</p>
                </div>
              </button>

              <button @click="$router.push({ name: 'influencer-list' })" class="w-full flex items-center justify-start h-12 rounded-xl border border-slate-200 hover:border-purple-300 hover:bg-purple-50 transition-all group px-3">
                <div class="w-10 h-10 bg-purple-50 rounded-xl flex items-center justify-center mr-3 group-hover:bg-purple-100 transition-colors">
                  <svg class="w-5 h-5 text-purple-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <div class="text-left">
                  <p class="font-medium text-slate-900">达人管理</p>
                  <p class="text-xs text-slate-500">管理达人资源</p>
                </div>
              </button>

              <button @click="$router.push({ name: 'settings' })" class="w-full flex items-center justify-start h-12 rounded-xl border border-slate-200 hover:border-slate-300 hover:bg-slate-100 transition-all group px-3">
                <div class="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center mr-3 group-hover:bg-slate-200 transition-colors">
                  <svg class="w-5 h-5 text-slate-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                </div>
                <div class="text-left">
                  <p class="font-medium text-slate-900">系统设置</p>
                  <p class="text-xs text-slate-500">配置系统参数</p>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTaskStore } from '@/stores/tasks'
import AppLayout from '@/layouts/AppLayout.vue'
import api from '@/api'

const authStore = useAuthStore()
const taskStore = useTaskStore()

const currentUser = computed(() => authStore.user)
const isAdmin = computed(() => {
  const role = authStore.user?.role
  return role === 'admin' || role === '集团管理员' || role === '管理员'
})

const alerts = ref<any>(null)
const alertsError = ref('')

async function loadAlerts() {
  alertsError.value = ''
  alerts.value = null
  try {
    const res = await api.get('/admin/alerts')
    alerts.value = res.data
  } catch (e: any) {
    const msg = e.response?.data?.detail || e.message || '无法连接服务器'
    alertsError.value = msg
  }
}

const stats = ref({
  todayTarget: 0,        // 今日目标（来自成长日程自动平摊）
  todayCompleted: 0,     // 今日已完成
  monthlyTarget: 0,      // 月度总目标
  dailyAvgTarget: 0,     // 日均目标（月目标/工作日数）
  monthTotalCompleted: 0,// 本月累计完成
  weekTarget: 0,
  weekCompleted: 0,
  pendingTasks: 0,
  completedTasks: 0,
  riskTasks: 0,
})

const recentTasks = ref<any[]>([])

const todayDate = new Date().toISOString().split('T')[0]

const todayStr = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
})

/** 格式化金额显示 */
function formatMoney(val: number): string {
  if (!val || val === 0) return '0.0'
  if (val >= 10000) return (val / 10000).toFixed(1) + '万'
  if (val >= 1000) return (val / 1000).toFixed(1) + 'k'
  return String(Math.round(val))
}

/** 获取今天的 YYYY-MM-DD 格式 */
function getTodayKey(): string {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${dd}`
}

const todayPercent = computed(() => {
  if (stats.value.todayTarget === 0) return 0
  return Math.min(Math.round((stats.value.todayCompleted / stats.value.todayTarget) * 100), 100)
})

const weekPercent = computed(() => {
  if (stats.value.weekTarget === 0) return 0
  return Math.min(Math.round((stats.value.weekCompleted / stats.value.weekTarget) * 100), 100)
})

onMounted(async () => {
  const today = new Date()
  const year = today.getFullYear()
  const month = today.getMonth() + 1
  const todayKey = getTodayKey()

  // ========== 从成长日程API加载目标数据 ==========
  try {
    // 1. 加载月度目标（自动平摊数据）
    try {
      const mtRes = await api.get(`/tasks/monthly/target?year=${year}&month=${month}`)
      if (mtRes.data && mtRes.data.target_amount > 0) {
        stats.value.monthlyTarget = mtRes.data.target_amount
        stats.value.dailyAvgTarget = mtRes.data.daily_target_avg || 0
      }
    } catch {
      // 无月度目标，静默处理
    }

    // 2. 加载日历数据（包含每天的目标和完成量）
    const calRes = await api.get(`/tasks?year=${year}&month=${month}`)
    if (calRes.data) {
      const calendarData = calRes.data as Record<string, any>

      // 今日数据
      if (calendarData[todayKey]) {
        const todayData = calendarData[todayKey]
        stats.value.todayTarget = todayData.targetAmount || 0
        stats.value.todayCompleted = todayData.completedAmount || 0
        stats.value.pendingTasks = todayData.tasks?.filter((t: any) => t.status === 'pending').length || 0
        stats.value.completedTasks = todayData.tasks?.filter((t: any) => t.status === 'completed').length || 0
        stats.value.riskTasks = todayData.tasks?.filter((t: any) => t.risk && t.risk !== '无').length || 0
      }

      // 本月累计完成量
      let monthTotal = 0
      let weekTotalCompleted = 0
      let weekTotalTarget = 0
      Object.values(calendarData).forEach((dd: any) => {
        monthTotal += dd.completedAmount || 0

        // 计算本周数据
        const ddDate = new Date(dd.dateKey)
        if (isThisWeek(ddDate)) {
          weekTotalCompleted += dd.completedAmount || 0
          weekTotalTarget += dd.targetAmount || 0
        }
      })
      stats.value.monthTotalCompleted = monthTotal
      stats.value.weekCompleted = weekTotalCompleted
      stats.value.weekTarget = weekTotalTarget > 0 ? weekTotalTarget : stats.value.dailyAvgTarget * 7
    }
  } catch (e) {
    console.error('首页加载成长日程数据失败:', e)
  }

  // ========== 加载最近7天任务列表（用于"最近任务"区域） ==========
  try {
    await taskStore.fetchTasksByDate(todayKey)

    const recents: any[] = []
    for (let i = 0; i < 7; i++) {
      const d = new Date()
      d.setDate(d.getDate() - i)
      const dk = getTodayKeyFor(d)
      if (taskStore.tasks[dk]) {
        const dayInfo = taskStore.tasks[dk] as any
        recents.push({ date: dk, ...dayInfo })
      }
    }
    recentTasks.value = recents
  } catch (e) {
    console.error('加载最近任务失败:', e)
  }

  // ========== 加载管理员告警 ==========
  if (isAdmin.value) {
    await loadAlerts()
  }
})

/** 判断日期是否在本周 */
function isThisWeek(d: Date): boolean {
  const now = new Date()
  const startOfWeek = new Date(now)
  startOfWeek.setDate(now.getDate() - now.getDay())
  startOfWeek.setHours(0, 0, 0, 0)
  return d >= startOfWeek
}

/** 获取指定日期的 YYYY-MM-DD key */
function getTodayKeyFor(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${dd}`
}
</script>
