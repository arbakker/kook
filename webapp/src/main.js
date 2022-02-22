import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import VueClipboards from 'vue-clipboards'

Vue.config.productionTip = false

Vue.use(VueRouter)
Vue.use(VueClipboards)

import RecipePage from './components/recipe-page.vue'
import LandingPage from './components/landing-page.vue'
import ProtectedPage from './components/protected-page.vue'

const routes = [
  {
    path: '/', component: LandingPage, name: 'home', meta: {
      requiresAuth: true
    }
  },
  {
    path: '/recipe/:recipeSlug', component: RecipePage, name: 'recipe', meta: {
      requiresAuth: true
    }
  },
  {
    path: '/protected', component: ProtectedPage, name: 'protected',
  },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    if (!localStorage.getItem('user-password')) next('/protected')
    else next()
  } else next()
})

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
