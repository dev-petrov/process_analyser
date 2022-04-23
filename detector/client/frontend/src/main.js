import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Axios from 'axios';
import { BootstrapVue } from 'bootstrap-vue'
import ErrorModal from './plugins/ErrorModal'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import store from './store';
import vuetify from './plugins/vuetify'


Vue.use(ErrorModal)
Vue.use(BootstrapVue)

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.isAuthenticated) {
      next({
        name: 'Login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})
Vue.config.productionTip = false
store.dispatch('checkAuth').then(() => {
  new Vue({
    router,
    store: store,
    vuetify,
    render: h => h(App)
  }).$mount('#app')
})
Axios.defaults.headers.common['Content-Type'] = 'application/json';
