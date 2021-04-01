import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/connexion',
  },
  {
    path: '/inscription',
    name: 'Inscription',
    component: () => import('../views/Inscription.vue')
  },
  {
    path: '/connexion',
    name: 'Connexion',
    component: () => import('../views/Connexion.vue')
  },

  /** Prof **/

  {
    path: '/dashboardProf',
    name: 'Prof',
    component: () => import('../views/Dashboard/Prof.vue'),
    redirect: '/dashboardProf/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component : () => import('../components/Prof/Home.vue')
      },
      {
        path: 'creation',
        name: 'CreationQcm',
        component : () => import('../components/Prof/CreerQcm.vue')
      },
      {
        path: 'consultation',
        name: 'Consultation',
        component : () => import('../components/Prof/Consultation.vue')
      },
      {
        path: 'correction',
        name: 'Correction',
        component : () => import('../components/Prof/Correction.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
