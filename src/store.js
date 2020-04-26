import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    connected: false,
    game: null,
    username: '',
    error: null,
    showJoin: true
  },
  getters: {
    gameLoaded (state) {
      if (state.game && state.username) {
        return true
      }
      return false
    }
  },
  mutations: {
    socket_connect (state) {
      state.connected = true
    },
    socket_disconnect (state) {
      state.connected = false
    },
    socket_message (state, message) {
      state.game = message
      state.error = null
    },
    socket_error (state, message) {
      state.error = message.error
    },
    reset_error (state) {
      state.error = null
      state.game = null
    },
    set_game (state, game) {
      state.game = game
    },
    set_username (state, username) {
      state.username = username
    },
    toggle_show_join (state) {
      state.showJoin = !state.showJoin
      state.error = null
    }
  }
})
