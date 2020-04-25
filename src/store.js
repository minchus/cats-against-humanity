import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    connected: false,
    game: {},
    roomCode: '',
    username: '',
    error: null,
    dealer: '',
    showJoin: true
  },
  getters: {
    words (state) {
      if (state.game.solution) {
        return Object.keys(state.game.solution)
      }
      return []
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
      state.roomCode = message.room_code
      state.error = null
    },
    socket_error (state, message) {
      state.error = message.error
    },
    set_game (state, game) {
      state.game = game
    },
    set_room (state, room) {
      state.roomCode = room
    },
    set_username (state, username) {
      state.username = username
    },
    reset_error (state) {
      state.error = null
    },
    reset_room (state) {
      state.room = ''
      state.game = {}
    },
    toggle_show_join (state) {
      state.showJoin = !state.showJoin
      state.error = null
    }
  }
})
