import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

const HomeView = () => import('./views/HomeView.vue')
const LoginView = () => import('./views/LoginView.vue')
const RegisterView = () => import('./views/RegisterView.vue')
const ProblemListView = () => import('./views/ProblemListView.vue')
const ProblemView = () => import('./views/ProblemView.vue')
const ReviewView = () => import('./views/ReviewView.vue')
const JobsView = () => import('./views/JobsView.vue')
const LinksView = () => import('./views/LinksView.vue')
const AdminView = () => import('./views/AdminView.vue')

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView, meta: { public: true } },
    { path: '/register', component: RegisterView, meta: { public: true } },
    { path: '/problems', component: ProblemListView },
    { path: '/problems/:slug', component: ProblemView },
    { path: '/review', component: ReviewView },
    { path: '/jobs', component: JobsView },
    { path: '/links', component: LinksView },
    { path: '/admin', component: AdminView, meta: { admin: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.loaded) await auth.fetchMe()
  if (!to.meta.public && !auth.me) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.meta.public && auth.me) {
    return { path: '/' }
  }
  if (to.meta.admin && auth.me && !auth.me.is_admin) {
    return { path: '/' }
  }
  return true
})
