import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import vuetify from './plugins/vuetify'

import App from './App.vue'
import router from './router'
import store from './store'
import './filters'

Vue.config.productionTip = false

// Vue.use(VueSocketIO, `//${window.location.host}`, store)

Vue.use(new VueSocketIO({
  debug: true,
  connection: `//${window.location.host}`,
  vuex: {
    store,
    actionPrefix: 'socket_',
    mutationPrefix: 'socket_'
  }
}))

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
