<template>
  <v-container>
    <v-row align="stretch" justify="start" wrap>
      <v-col lg="2" md="3" sm="5" xs="12">
        <v-card dark outlined class="mb-12">
          <v-card-text>
              {{ blackCardText }}
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-for="pick in pickCount" :key="pick" lg="2" md="3" sm="5" xs="12">
        <v-card outlined class="mb-12">
          <v-card-text>
              {{ selectionOne }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="stretch" justify="start" wrap>
      <v-col v-for="card in hand" :key="card" lg="2" md="3" sm="5" xs="12">
        <v-card outlined hover height="100%" class="card-outer" @click="onSelect">
          <v-card-text>
            <div class="text--primary">
              {{ card }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
      <v-btn color="grey lighten-2" class="black--text">Submit</v-btn>
      <v-btn color="grey darken-2" class="white--text">Reset</v-btn>
  </v-container>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'game-board',
  data () {
    return {
      selectionOne: '',
      room: ''
    }
  },
  methods: {
    ...mapMutations(['set_username']),
    onSelect () {
      console.log('card clicked')
    }
  },
  computed: {
    ...mapState({
      username: state => state.username,
      game: state => state.game,
      pickCount: state => state.game.black_card.pick,
      blackCardText: state => state.game.black_card.text,
      hand: state => Object.keys(state.game.players[state.username].hand)
    })
  },
  mounted () {
    if (!this.username) this.set_username(this.$route.params.username)
    if (!this.room) this.room = this.$route.params.room
  }
}
</script>

<style>
.card-outer {
  position: relative;
  padding-bottom: 20px;
}
</style>
