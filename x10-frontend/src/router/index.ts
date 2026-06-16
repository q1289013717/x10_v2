import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/Login.vue'),
    },
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/Home.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: () => import('@/pages/Calendar.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/pages/Tasks.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/task-edit',
      name: 'task-edit',
      component: () => import('@/pages/TaskEdit.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('@/pages/Statistics.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('@/pages/Reports.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/report-edit',
      name: 'report-edit',
      component: () => import('@/pages/ReportEdit.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/report-detail',
      name: 'report-detail',
      component: () => import('@/pages/ReportDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/training',
      name: 'training',
      component: () => import('@/pages/TrainingDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/training-detail/:id',
      redirect: '/training',
    },
    {
      path: '/training-quiz',
      name: 'training-quiz',
      component: () => import('@/pages/TrainingQuiz.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/training-problem',
      name: 'training-problem',
      component: () => import('@/pages/TrainingProblem.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/influencer-list',
      name: 'influencer-list',
      component: () => import('@/pages/InfluencerList.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/influencer-summary',
      name: 'influencer-summary',
      component: () => import('@/pages/InfluencerSummary.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/darensource',
      name: 'darensource',
      component: () => import('@/pages/DarenSource.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/consensus-archive',
      name: 'consensus-archive',
      component: () => import('@/pages/ConsensusArchive.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/pages/Settings.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/pages/NotFound.vue'),
    },
  ],
})

// 路由守卫 — 检查认证状态
router.beforeEach(async (to, _from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }

    // 如果 AuthStore 中已有用户信息，直接放行（已验证过）
    const authStore = useAuthStore()
    if (authStore.user) {
      next()
      return
    }

    // 尝试从 localStorage 恢复用户信息，或调用 /auth/me 验证
    authStore.restore()
    if (authStore.user) {
      next()
      return
    }

    try {
      await authStore.fetchCurrentUser()
      next()
    } catch {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
