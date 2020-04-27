<template>
  <v-container>
    <v-alert type="error" :value="!!error" transition="slide-y-reverse-transition">
      {{ error }}
    </v-alert>
    <div v-if="gameLoaded">
      <game-board></game-board>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex'
import GameBoard from '../components/GameBoard'

export default {
  name: 'player',
  components: {
    GameBoard
  },
  data () {
    return {
      room: ''
    }
  },
  computed: {
    ...mapGetters(['gameLoaded']),
    ...mapState(['error', 'username'])
  },
  methods: {
    ...mapMutations(['set_username'])
  },
  mounted () {
    if (!this.username) this.set_username(this.$route.params.username)
    if (!this.room) this.room = this.$route.params.room
    this.$socket.emit('join', {
      username: this.username,
      room: this.room,
      firstTime: false })
  }
}
</script>
