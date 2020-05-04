import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Api from './views/Api.vue'
import Player from './views/Player.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/:room/:username',
      name: 'Player',
      component: Player
    }
  ]
})
