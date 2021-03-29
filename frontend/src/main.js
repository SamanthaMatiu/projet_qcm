import BootstrapVue from 'bootstrap-vue';
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.interceptors.request.use(req => {
  console.log(`${req.method} ${req.url}`);
  req.headers.common['x-access-tokens'] = localStorage.getItem('token');
  return req;
})

Vue.use(BootstrapVue);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
