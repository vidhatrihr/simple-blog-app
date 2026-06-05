import { createRouter, createWebHistory } from 'vue-router'
import { useWhoAmI } from '@/composables/useWhoAmI.js'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import FeedView from '../views/FeedView.vue'
import WriteView from '../views/WriteView.vue'
import BlogView from '../views/BlogView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView, meta: { guestOnly: true } },
    { path: '/register', component: RegisterView, meta: { guestOnly: true } },
    { path: '/feed', component: FeedView, meta: { requiresAuth: true } },
    { path: '/write', component: WriteView, meta: { requiresAuth: true } },
    { path: '/blog/:slug', component: BlogView, meta: { requiresAuth: true } },
    { path: '/profile/:userId', component: ProfileView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to, from) => {
  const { whoAmI, clearUser } = useWhoAmI()

  if (from.meta.guestOnly && to.meta.requiresAuth) {
    clearUser()
  }

  const me = await whoAmI()

  if (to.meta.requiresAuth && !me) {
    return '/'
  }
  if (to.meta.guestOnly && me) {
    return '/feed'
  }
})

export default router
