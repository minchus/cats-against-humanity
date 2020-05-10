import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Stats from './views/Stats.vue'
import Player from './views/Player.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
      path: '/stats',
      name: 'stats',
      component: Stats
    },
    {
      path: '/:room/:username',
      name: 'Player',
      component: Player
    }
  ]
})
