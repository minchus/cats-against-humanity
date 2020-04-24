<template>
  <v-card class="elevation-12">
    <v-card-text>
      <v-form ref='form' v-model='isValid'>
        <v-text-field
          label="Player name"
          name="username"
          type="text"
          v-model="username"
          :rules="[rules.required]"
        ></v-text-field>
        <v-text-field
          label="Room code"
          name="room_code"
          type="text"
          v-model="room_code"
          :rules="[rules.required]"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="grey lighten-2" class="black--text" @click="toggleIsJoin">Create game</v-btn>
      <v-spacer />
      <v-btn color="grey darken-2" class="white--text" @click="joinGame">Join</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'join-form',
  data () {
    return {
      username: '',
      room_code: null,
      isValid: true,
      rules: {
        required: value => !!value || 'Required'
      }
    }
  },
  methods: {
    ...mapMutations(['set_username', 'set_room', 'toggle_show_join']),
    joinGame () {
      this.$refs.form.validate()
      if (this.isValid) {
        this.set_username(this.username)
        this.set_room(this.room_id)
        // this.$router.push({ name: 'Player', params: { room: this.room_code } })
      }
    },
    toggleIsJoin () {
      this.toggle_show_join()
    }
  }
}
</script>
