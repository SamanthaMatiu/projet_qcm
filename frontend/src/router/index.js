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

  /** Admin **/

  {
    path: '/dashboardAdmin',
    name: 'Admin',
    component: () => import('../views/Dashboard/Admin.vue')
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
        path: 'detailQcm/:id',
        name: 'DetailQcm',
        component : () => import('../components/Prof/DetailQcm.vue')
      },
      {
        path: 'correction',
        name: 'Correction',
        component : () => import('../components/Prof/Correction.vue')
      }
    ]
  },
    /** Admin 

    {
      path: '/dashboardEleve',
      name: 'Eleve',
      component: () => import('../views/Dashboard/Eleve.vue')
    }**/
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
