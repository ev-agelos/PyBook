import Vue from 'vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import App from './App.vue'
import router from './router'
import store from './store.js'

Vue.use(Buefy)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  data: {
      store: store,
      user: {},
      bookmarks: [],
      pagination: {}
  }
}).$mount('#app')
