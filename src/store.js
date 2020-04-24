import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    connected: false,
    game: {},
    room: '',
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
    SOCKET_connect (state) {
      state.connected = true
    },
    SOCKET_disconnect (state) {
      state.connected = false
    },
    SOCKET_message (state, message) {
      state.game = message
      state.room = message.game_id
      state.error = null
    },
    SOCKET_join_room (state, message) {
      state.error = null
      state.room = message.room
    },
    SOCKET_error (state, message) {
      state.error = message.error
    },
    set_turn (state, team) {
      state.turn = team
    },
    set_game (state, game) {
      state.game = game
    },
    set_room (state, room) {
      state.room = room
    },
    set_username (state, username) {
      state.username = username
    },
    reset_error (state) {
      state.room = null
      state.error = null
    },
    reset_room (state) {
      state.game = {}
    },
    toggle_show_join (state) {
      state.showJoin = !state.showJoin
    }
  }
})
