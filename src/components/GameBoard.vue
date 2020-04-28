<template>
  <v-container>

    <v-row align="stretch" justify="start" wrap>
      <v-col v-if="!submissionDone" lg="2" md="3" sm="5" xs="12">
        <v-card dark raised height="100%" min-height="100px">
          <v-card-text>
              <div class="overline mb-4">My card (not submitted)</div>
              <span class="headline" v-html="blackCardHtml"></span>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-for="(player, index) in submittedPlayers" :key="index" lg="2" md="3" sm="5" xs="12">
        <v-card :dark="!isWinner(player)" outlined class="card-outer" height="100%" min-height="100px">
          <v-card-text>
              <div v-if="isWinner(player)" class="overline mb-4">{{ player.name }}'s card wins</div>
              <div v-if="!isWinner(player)" class="overline mb-4">{{ player.name === username ? 'My card (submitted)' : '' }}</div>
              <span class="headline" v-html="getSubmission(player)"></span>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="isDealer" text class="white--text" @click="onPick(player)" :disabled="pickDisabled">Pick</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="isDealer" text class="white--text" @click="onReveal(index)" :disabled="submissionRevealed(player)">Reveal</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row align="stretch" justify="start" wrap class="mt-10">
      <v-col v-for="card in availableHand" :key="card" lg="2" md="3" sm="5" xs="12">
        <v-card outlined hover height="100%" class="card-outer" @click="onSelect(card)">
          <v-card-text>
            <div class="text--primary">
              <span v-html="card"></span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-btn color="grey lighten-2" class="mt-4 mr-4 black--text" @click="onReset" :disabled="resetDisabled">Reset</v-btn>
    <v-btn color="grey darken-2" class="mt-4 white--text" @click="onSubmit" :disabled="submitDisabled">Submit</v-btn>
    <div class="mt-3"><br></div>

    <v-footer
      color="grey darken-4"
      app
    >
    <span class="white--text">Dealer: {{ dealer }}</span>
    <v-divider inset vertical color="white" class="ml-5 mr-5"></v-divider>
    <span class="white--text">{{ numSubmitted }} / {{ numPlayers }} players have submitted</span>
    <v-divider inset vertical color="white" class="ml-5 mr-5"></v-divider>
    <span class="white--text">{{ this.roundsPlayed }} rounds played</span>
    <v-spacer></v-spacer>

    <div class="text-center">
      <v-dialog v-model="dialog" width="500" >

        <template v-slot:activator="{ on }">
          <v-btn color="grey darken-2" class="mt-2 mb-2 mr-3 white--text" v-on="on">Show scores</v-btn>
        </template>

        <v-card>
          <v-card-title class="headline grey lighten-2" primary-title > Scores ({{this.roundsPlayed}} rounds played)</v-card-title>

          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="player in players" :key="player.name">
                  <td>{{ player.name }}</td>
                  <td>{{ player.roundsWon }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="dialog = false" >Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>

    <v-btn color="grey darken-2" class="mt-2 mb-2 white--text" @click="onNextRound">Next Round</v-btn>
    </v-footer>

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
      room: '',
      cardsToSubmit: [],
      dialog: false
    }
  },
  methods: {
    ...mapMutations(['set_username']),
    formatBlackCard (blackCardIn, text) {
      let ret = ''
      if (blackCardIn.includes('_')) {
        ret = blackCardIn.replace(/_/, '<u><strong>' + text + '</strong></u>')
      } else {
        ret = blackCardIn + '<br><u><strong>' + text + '</strong></u>'
      }
      return ret
    },
    onSelect (cardText) {
      if (this.selectionIndex < this.pickCount) {
        this.cardsToSubmit.push(cardText)
        this.blackCardHtml = this.formatBlackCard(this.blackCardHtml, cardText)
        this.selectionIndex += 1
      }
    },
    onReset () {
      this.blackCardHtml = this.blackCardText
      this.selectionIndex = 0
      this.cardsToSubmit = []
    },
    onSubmit () {
      this.$socket.emit('submit', {
        room: this.room,
        username: this.username,
        submission: this.blackCardHtml,
        submittedCards: this.cardsToSubmit })
    },
    onReveal (index) {
      this.$socket.emit('reveal', {
        room: this.room,
        username: this.submittedPlayers[index].name
      })
    },
    onPick (player) {
      this.$socket.emit('pick', {
        room: this.room,
        pick: player.name
      })
    },
    getSubmission: function (player) {
      if (player.name === this.username && !this.isDealer) {
        return player.submission // Your own submission should always be revealed, unless you are the dealer
      }
      return this.submissionRevealed(player) ? player.submission : 'Not revealed'
    },
    submissionRevealed: function (player) {
      return player.submissionRevealed
    },
    isWinner (player) {
      return player.isWinner
    },
    onNextRound: function () {
      this.$socket.emit('next', {
        room: this.room
      })
    }
  },
  computed: {
    ...mapState({
      username: state => state.username,
      pickCount: state => state.game.black_card.pick,
      blackCardText: state => state.game.black_card.text,
      hand: state => Object.keys(state.game.players[state.username].hand),
      dealer: state => state.game.dealer,
      players: state => state.game.players,
      roundsPlayed: state => state.game.rounds_played
    }),
    isDealer: function () {
      return this.username === this.dealer
    },
    submittedPlayers: function () {
      let ret = []
      /* eslint-disable no-unused-vars */
      for (let [playerName, playerObj] of Object.entries(this.players)) {
        if (playerObj.hasSubmitted) {
          ret.push(playerObj)
        }
      }
      /* eslint-enable no-unused-vars */
      // Sort by submission order
      ret.sort((a, b) => (a.submissionNumber > b.submissionNumber) ? 1 : -1)
      return ret
    },
    numSubmitted: function () {
      let ret = 0
      /* eslint-disable no-unused-vars */
      for (let [playerName, playerObj] of Object.entries(this.players)) {
        if (playerObj.hasSubmitted) {
          ret += 1
        }
      }
      /* eslint-enable no-unused-vars */
      return ret
    },
    availableHand: function () {
      let ret = []
      for (let i = 0; i < this.hand.length; i++) {
        if (!this.cardsToSubmit.includes(this.hand[i])) {
          ret.push(this.hand[i])
        }
      }
      return ret
    },
    numPlayers: function () {
      return Object.keys(this.players).length
    },
    submissionDone: function () {
      return this.players[this.username].hasSubmitted
    },
    submitDisabled: function () {
      if (this.selectionIndex !== this.pickCount || this.submissionDone) {
        return true
      }
      return false
    },
    resetDisabled: function () {
      if (this.submissionDone) {
        return true
      }
      return false
    },
    pickDisabled: function () {
      /* eslint-disable no-unused-vars */
      for (let [playerName, playerObj] of Object.entries(this.players)) {
        if (playerObj.submissionRevealed === false || playerObj.isWinner === true) {
          return true
        }
      }
      /* eslint-enable no-unused-vars */
      return false
    }
  },
  mounted () {
    if (!this.username) this.set_username(this.$route.params.username)
    if (!this.room) this.room = this.$route.params.room
  },
  sockets: {
    reset: function () {
      console.log('reset received')
      this.onReset()
    }
  }
}
</script>

<style>
.card-outer {
  position: relative;
  padding-bottom: 0px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
</style>
