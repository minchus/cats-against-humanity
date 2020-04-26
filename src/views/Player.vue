<template>
  <game-board></game-board>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import GameBoard from '../components/GameBoard'

export default {
  name: 'player',
  components: {
    GameBoard
  },
  computed: {
    ...mapState(['room', 'username']),
    role () {
      return this.$route.name
    }
  },
  mounted () {
    // join game if e.g. this page was reached by typing address in bar
    // if (!this.username) this.set_username('#unknown')
    // if (!this.room) this.set_room(this.$route.params.room)
    // const params = {
    //   username: this.username,
    //   room: this.room
    // }
    // this.$socket.emit('join', params)
  },
  methods: {
    ...mapMutations(['set_room', 'set_username'])
  }
}
</script>
