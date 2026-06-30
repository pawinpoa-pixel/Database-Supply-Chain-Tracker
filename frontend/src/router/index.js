import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/LandingView.vue'
import Login from '../views/LoginView.vue'
import Register from '../views/RegisterView.vue'
import Dashboard from '../views/DashboardView.vue'
import { getToken } from '../api/auth'

const routes = [
  { path: '/', component: Landing },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/dashboard',
    component: Dashboard,
    beforeEnter: (to, from, next) => {
      getToken() ? next() : next('/login')
    },
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
