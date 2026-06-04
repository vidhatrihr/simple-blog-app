import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import FeedView from '../views/FeedView.vue'
import WriteView from '../views/WriteView.vue'
import BlogView from '../views/BlogView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/feed', component: FeedView },
    { path: '/write', component: WriteView },
    { path: '/blog/:slug', component: BlogView },
    { path: '/profile/:userId', component: ProfileView },
  ],
})

export default router
