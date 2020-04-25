<template>
  <v-card class="elevation-12">
    <v-card-text>Sample text</v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'player',
  components: {
    // GameBoard
  },
  computed: {
    ...mapState(['room', 'username']),
    role () {
      return this.$route.name
    }
  },
  mounted () {
    if (!this.username) this.set_username('#unknown')
    if (!this.room) this.set_room(this.$route.params.room)
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
