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
      },
      {
        path: 'correction/:id_qcm/:id_eleve',
        name: 'CorrigerQCM',
        component : () => import('../components/Prof/CorrigerQcm.vue')
      },
      {
        path: 'notes',
        name: 'ConsulterNotes',
        component : () => import('../components/Prof/ConsulterNotes.vue')
      }
      
    ]
  },
    /** Eleve **/

    {
      path: '/dashboardEleve',
      name: 'Eleve',
      component: () => import('../views/Dashboard/Eleve.vue'),
      redirect: '/dashboardEleve/home',
      children: [
        {
          path: 'home',
          name: 'HomeEleve',
          component : () => import('../components/Eleve/Home.vue')
        },
        {
          path: 'afaire',
          name: 'QcmsAFaire',
          component : () => import('../components/Eleve/QCMsAFaire.vue')
        },
        {
          path: 'afaire/:id',
          name: 'RepondreQCM',
          component : () => import('../components/Eleve/RepondreQCM.vue')
        },
        {
          path: 'fait',
          name: 'QcmsFait',
          component : () => import('../components/Eleve/QCMsFait.vue')
        },
        {
          path: 'fait/:id',
          name: 'ConsulterQCM',
          component : () => import('../components/Eleve/ConsulterQCM.vue')
        },
        {
          path: 'corriges',
          name: 'QcmsCorriges',
          component : () => import('../components/Eleve/QCMsCorriges.vue')
        },
        {
          path: 'corriges/:id',
          name: 'ConsulterQCMCorriges',
          component : () => import('../components/Eleve/ConsulterQCMCorriges.vue')
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
