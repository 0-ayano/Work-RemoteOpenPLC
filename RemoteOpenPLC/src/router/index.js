import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/run',
      name: 'runing',
      component: () => import('../views/RunningView.vue')
    },
    {
      path: '/set',
      name: 'setting',
      component: () => import('../views/SettingView.vue')
    }
  ]
})

export default router