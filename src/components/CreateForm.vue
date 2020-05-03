<template>
  <v-card class="elevation-12">
    <v-card-text>
      <v-form ref='form' v-model='isValid' v-on:submit.prevent="onSubmit">
        <v-alert type="error" :value="!!error" transition="slide-y-reverse-transition">
          {{ error }}
        </v-alert>

        <v-text-field
          label="Player name"
          name="username"
          type="text"
          v-model="username"
          :rules="[rules.required]"
        ></v-text-field>

        <v-select
          v-model="selected_decks"
          :items="deck_list"
          item-value="code"
          item-text="description"
          multiple
          chips
          hint="Pick cards to include in game"
          persistent-hint
        ></v-select>

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
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'create-form',
  data () {
    return {
      username: '',
      isValid: true,
      selected_decks: [this.$store.state.deck_list[0].code],
      rules: {
        required: value => !!value || 'Required'
      }
    }
  },
  methods: {
    ...mapMutations(['set_username', 'toggle_show_join', 'set_error']),
    createGame () {
      if (this.selected_decks.length === 0) {
        this.set_error('At least one set of cards should be selected')
        return
      }
      this.$refs.form.validate()
      if (this.isValid) {
        this.set_username(this.username)
        this.$socket.emit('create', { username: this.username, decks: this.selected_decks })
      }
    },
    toggleIsJoin () {
      this.toggle_show_join()
    }
  },
  computed: {
    ...mapState(['deck_list', 'error'])
  },
  sockets: {
    message: function (data) {
      this.$router.push({
        name: 'Player',
        params: { room: data.room_code, username: this.username }
      })
    }
  }
}
</script>
