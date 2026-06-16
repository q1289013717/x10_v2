<template>
  <div class="min-h-screen bg-[#f5f6f7] flex">
    <!-- 左侧品牌区域 — 增长引擎风格 -->
    <div class="hidden lg:flex lg:w-[55%] bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#0f172a] relative overflow-hidden">
      <!-- 背景装饰 -->
      <div class="absolute inset-0">
        <!-- 网格背景 -->
        <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 32px 32px;" />
        <!-- 光晕效果 -->
        <div class="absolute -top-24 -left-24 w-[500px] h-[500px] bg-blue-600/15 rounded-full blur-[120px]" />
        <div class="absolute -bottom-32 -right-32 w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-[140px]" />
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-500/5 rounded-full blur-[100px]" />
        <!-- 装饰线条 -->
        <div class="absolute top-0 right-20 w-px h-full bg-gradient-to-b from-transparent via-white/[0.05] to-transparent" />
        <div class="absolute bottom-20 left-1/4 w-48 h-px bg-gradient-to-r from-transparent via-cyan-400/30 to-transparent" />
      </div>

      <div class="relative z-10 flex flex-col justify-center px-16 xl:px-20 py-12">
        <!-- Logo + 标题区 -->
        <div class="mb-14">
          <!-- Logo -->
          <div class="inline-flex items-center justify-center w-[72px] h-[72px] bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 rounded-2xl shadow-2xl shadow-blue-600/30 mb-8 relative">
            <div class="absolute inset-0 bg-blue-400/20 rounded-2xl blur-xl" />
            <svg class="w-9 h-9 text-white relative z-10" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>

          <!-- 主标题 -->
          <h1 class="text-[44px] font-extrabold text-white mb-5 tracking-tight leading-tight">
            X10<span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">增长引擎</span>
          </h1>

          <!-- 副标语 — 三行独立展示 -->
          <div class="space-y-3">
            <div class="flex items-center gap-3 group cursor-default">
              <span class="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-500/15 border border-emerald-500/25 text-emerald-400 text-sm font-bold">01</span>
              <p class="text-xl font-medium text-slate-200 tracking-wide">让<span class="text-emerald-400 font-semibold">目标</span>清晰</p>
              <div class="ml-auto w-20 h-px bg-gradient-to-r from-emerald-500/40 to-transparent opacity-60" />
            </div>
            <div class="flex items-center gap-3 group cursor-default">
              <span class="flex items-center justify-center w-8 h-8 rounded-lg bg-blue-500/15 border border-blue-500/25 text-blue-400 text-sm font-bold">02</span>
              <p class="text-xl font-medium text-slate-200 tracking-wide">让<span class="text-blue-400 font-semibold">过程</span>可见</p>
              <div class="ml-auto w-20 h-px bg-gradient-to-r from-blue-500/40 to-transparent opacity-60" />
            </div>
            <div class="flex items-center gap-3 group cursor-default">
              <span class="flex items-center justify-center w-8 h-8 rounded-lg bg-purple-500/15 border border-purple-500/25 text-purple-400 text-sm font-bold">03</span>
              <p class="text-xl font-medium text-slate-200 tracking-wide">让<span class="text-purple-400 font-semibold">增长</span>可复制</p>
              <div class="ml-auto w-20 h-px bg-gradient-to-r from-purple-500/40 to-transparent opacity-60" />
            </div>
          </div>
        </div>

        <!-- 核心能力卡片组 -->
        <div class="grid grid-cols-3 gap-4 mt-6">
          <div v-for="(item, idx) in features" :key="idx" class="group relative bg-white/[0.04] backdrop-blur-sm hover:bg-white/[0.08] border border-white/[0.08] hover:border-white/[0.16] rounded-2xl p-5 transition-all duration-300 cursor-default">
            <!-- 卡片顶部装饰线 -->
            <div :class="['absolute top-0 left-4 right-4 h-px', item.gradientLine]" />
            <!-- 图标 -->
            <div :class="['w-11 h-11 rounded-xl flex items-center justify-center mb-3 transition-transform duration-300 group-hover:scale-110', item.iconBg]">
              <svg class="w-5 h-5" :class="item.iconColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path :d="item.iconPath"/></svg>
            </div>
            <h3 class="text-base font-semibold text-white mb-1">{{ item.title }}</h3>
            <p class="text-xs text-slate-400 leading-relaxed">{{ item.desc }}</p>
          </div>
        </div>

        <!-- 底部数据条 -->
        <div class="mt-10 flex items-center gap-6 text-slate-500 text-xs">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-lg shadow-emerald-500/50" />
            <span>系统运行中</span>
          </div>
          <span class="w-px h-3 bg-slate-700" />
          <span>v2.0</span>
          <span class="w-px h-3 bg-slate-700" />
          <span>安全连接</span>
        </div>
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="flex-1 flex items-center justify-center p-4 sm:p-8">
      <div class="w-full max-w-md">
        <!-- 移动端 Logo -->
        <div class="lg:hidden text-center mb-6 sm:mb-8">
          <div class="inline-flex items-center justify-center w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/30 mb-3 sm:mb-4">
            <svg class="w-6 h-6 sm:w-7 sm:h-7 text-white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-slate-900">X10增长引擎</h1>
          <p class="text-slate-500 mt-1 text-sm sm:text-base">让增长可复制</p>
        </div>

        <!-- 登录卡片 -->
        <div class="bg-white rounded-2xl p-5 sm:p-8 shadow-soft border border-slate-100">
          <div class="mb-5 sm:mb-6">
            <h2 class="text-lg sm:text-xl font-bold text-slate-900">登录账号</h2>
            <p class="text-sm text-slate-500 mt-1">请输入账号和密码登录系统</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
            <!-- 账号 -->
            <div>
              <label class="text-slate-700 flex items-center gap-2 text-sm font-medium mb-1.5">
                <svg class="w-4 h-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                账号
              </label>
              <input
                v-model="form.account"
                type="text"
                placeholder="请输入账号"
                class="h-10 sm:h-11 w-full bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 rounded-lg px-4 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-base"
              />
            </div>

            <!-- 密码 -->
            <div>
              <label class="text-slate-700 flex items-center gap-2 text-sm font-medium mb-1.5">
                <svg class="w-4 h-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                密码
              </label>
              <div class="relative">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  class="h-10 sm:h-11 w-full bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 rounded-lg pl-4 pr-10 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all text-base"
                />
                <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors p-1">
                  <svg v-if="showPassword" class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                  <svg v-else class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                </button>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-lg p-3 text-red-600 text-sm flex items-center gap-2">
              <svg class="w-4 h-4 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              {{ loginError }}
            </div>

            <!-- 记住我 / 忘记密码 -->
            <div class="flex items-center justify-between flex-wrap gap-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="rememberMe" type="checkbox" class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                <span class="text-sm text-slate-600">记住我</span>
              </label>
              <button type="button" @click="onForgotPassword" class="text-sm text-blue-600 hover:text-blue-700 font-medium">忘记密码？</button>
            </div>

            <!-- 登录按钮 -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full h-11 sm:h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition-all duration-200 shadow-lg shadow-blue-600/30 disabled:opacity-60 active:scale-[0.98]"
            >
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                登录中...
              </span>
              <span v-else>登录</span>
            </button>
          </form>
        </div>

        <!-- 底部信息 -->
        <div class="text-center mt-4 sm:mt-6 text-slate-400 text-xs sm:text-sm">
          <p>&copy; 2026 赫拉生物科技（深圳）有限公司</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ account: '', password: '' })
const showPassword = ref(false)
const rememberMe = ref(false)
const loading = ref(false)
const loginError = ref('')

const features = [
  {
    title: '数据驱动增长',
    desc: '实时追踪核心指标，数据说话',
    iconPath: 'M3 3v18h18M7 14l4-4 4 4 6-6',
    iconBg: 'bg-emerald-500/15',
    iconColor: 'text-emerald-400',
    gradientLine: 'bg-gradient-to-r from-emerald-400/80 to-transparent',
  },
  {
    title: '智能任务管理',
    desc: '目标自动拆解，每日清晰可见',
    iconPath: 'M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11',
    iconBg: 'bg-blue-500/15',
    iconColor: 'text-blue-400',
    gradientLine: 'bg-gradient-to-r from-blue-400/80 to-transparent',
  },
  {
    title: '团队协作高效',
    desc: '全员进度透明，复制成功路径',
    iconPath: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75',
    iconBg: 'bg-purple-500/15',
    iconColor: 'text-purple-400',
    gradientLine: 'bg-gradient-to-r from-purple-400/80 to-transparent',
  },
]

async function handleLogin() {
  loading.value = true
  loginError.value = ''
  try {
    await authStore.login(form.account, form.password)
    // 管理员登录进首页（看告警面板），普通员工进日历
    if (authStore.isAdmin) {
      router.push('/')
    } else {
      router.push('/calendar')
    }
  } catch (e: any) {
    loginError.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}

function onForgotPassword() {
  window.alert('如需重置密码，请联系管理员')
}
</script>
