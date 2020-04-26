<template>
  <v-container>

    <v-row align="stretch" justify="start" wrap>
      <v-col lg="2" md="3" sm="5" xs="12">
        <v-card dark outlined height="100%" min-height="100px">
          <v-card-text>
              <span v-html="blackCardHtml"></span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row align="stretch" justify="start" wrap>
      <v-col v-for="card in hand" :key="card" lg="2" md="3" sm="5" xs="12">
        <v-card outlined hover height="100%" class="card-outer" @click="onSelect(card)">
          <v-card-text>
            <div class="text--primary">
              {{ card }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-btn color="grey lighten-2" class="mt-4 mr-4 black--text" @click="onReset">Reset</v-btn>
    <v-btn color="grey darken-2" class="mt-4 white--text" @click="onSubmit">Submit</v-btn>

  </v-container>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

export default {
  name: 'game-board',
  data () {
    return {
      blackCardHtml: this.$store.state.game.black_card.text,
      selectionIndex: 0,
      room: ''
    }
  },
  methods: {
    ...mapMutations(['set_username']),
    onSelect (cardText) {
      if (this.selectionIndex < this.pickCount) {
        console.log('selection %i set to %s', this.selectionIndex, cardText)
        if (this.blackCardHtml.includes('_')) {
          this.blackCardHtml = this.blackCardHtml.replace(/_/, '<u><strong>' + cardText + '</strong></u>')
        } else {
          this.blackCardHtml += '<br><u><strong>' + cardText + '</strong></u>'
        }
        this.selectionIndex += 1
      }
    },
    onReset () {
      this.blackCardHtml = this.blackCardText
      this.selectionIndex = 0
    },
    onSubmit () {
      this.$socket.emit('submit', {
        room: this.room,
        username: this.username,
        submission: this.blackCardHtml })
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
