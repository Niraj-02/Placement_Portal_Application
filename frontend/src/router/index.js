import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CompanyRegistrationView from '../views/CompanyRegistrationView.vue'
import StudentHistory from "@/components/student/StudentHistory.vue"
import StudentEditProfile from "@/components/student/StudentEditProfile.vue"
import CompanyEditProfile from "@/components/company/CompanyEditProfile.vue"

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
      name: 'student_registration',
      component: () => import('../views/student/StudentRegistrationView.vue'),
    },
    {
      path: '/admin_dashboard',
      name: 'AdminDashboard',
      component: () => import('../views/admin/AdminDashboardView.vue'),
    },
    {
      path: '/company_dashboard',
      name: 'CompanyDashboard',
      component: () => import('../views/company/CompanyDashboardView.vue'),
    },
    {
      path:'/company/create-drive',
      name:'CreateDrive',
      component: () => import('../views/company/CreateDriveView.vue')
    },

    {
      path:'/company/drive/:id/applications',
      component: () => import('../views/company/DriveApplicationsView.vue') 
    },
    {
      path: '/student_dashboard',
      name: 'StudentDashboard',
      component: () => import('../views/student/StudentDashboardView.vue'),
    },
    {
      path: '/student/company/:id',
      name: 'StudentCompanyDetails',
      component: () => import('../views/student/CompanyDetailsView.vue'),
    },
    {
      path: '/student/drive/:id',
      name: 'StudentDriveDetails',
      component: () => import ('../views/student/DriveDetailsView.vue')
    },
    {
      path:"/student_history",
      component:StudentHistory
    },

    {
      path:"/student_edit_profile",
      component:StudentEditProfile
    },
    {
      path:"/company_edit_profile",
      component:CompanyEditProfile
    }
  ],
})

export default router
