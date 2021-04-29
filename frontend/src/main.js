import BootstrapVue from 'bootstrap-vue';
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/build/css/mdb.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import Multiselect from 'vue-multiselect'

axios.interceptors.request.use(req => {
  console.log(`${req.method} ${req.url}`);
  req.headers.common['x-access-token'] = localStorage.getItem('token');
  return req;
})

Vue.use(BootstrapVue);
Vue.component('multiselect', Multiselect)
Vue.config.productionTip = false

axios.defaults.withCredentials = false;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
