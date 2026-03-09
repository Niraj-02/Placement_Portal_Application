import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CompanyRegistrationView from '../views/CompanyRegistrationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/company_registration',
      name: 'company_registration',
      component: CompanyRegistrationView,
    },
    {
      path: '/student_registration',
      name: 'student',
      component: () => import('../views/StudentRegistrationView.vue'),
    },
  ],
})

export default router
