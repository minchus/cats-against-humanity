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
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="grey lighten-2" class="black--text" @click="toggleIsJoin">Back to join</v-btn>
      <v-spacer />
      <v-btn color="grey darken-2" class="white--text" @click="createGame">Create game</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'create-form',
  data () {
    return {
      username: '',
      isValid: true,
      rules: {
        required: value => !!value || 'Required'
      }
    }
  },
  methods: {
    ...mapMutations(['set_username', 'toggle_show_join']),
    createGame () {
      this.$refs.form.validate()
      if (this.isValid) {
        this.set_username(this.username)
        this.$socket.emit('create', { username: this.username })
      }
    },
    toggleIsJoin () {
      this.toggle_show_join()
    }
  }
}
</script>
