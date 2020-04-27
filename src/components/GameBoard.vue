<template>
  <v-container>
    Dealer: {{ dealer }}

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
        <v-card dark outlined class="card-outer" height="100%" min-height="100px">
          <v-card-text>
              <div class="overline mb-4">{{ player.name }}'s card<br>Votes: {{ player.votes }}</div>
              <span class="headline" v-html="getSubmission(player)"></span>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="submissionRevealed(player)" text class="white--text" @click="onVote(index)" :disabled="voteDisabled">Vote</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="isDealer" text class="white--text" @click="onReveal(index)" :disabled="submissionRevealed(player)">Reveal</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

    </v-row>

    <v-row align="stretch" justify="start" wrap class="mt-10">
      <v-col v-for="card in hand" :key="card" lg="2" md="3" sm="5" xs="12">
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
    <v-btn color="grey darken-2" class="mt-4 white--text" @click="onNextRound">Next Round</v-btn>

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
      showMyCard: true
    }
  },
  methods: {
    ...mapMutations(['set_username']),
    onSelect (cardText) {
      if (this.selectionIndex < this.pickCount) {
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
    },
    onReveal (index) {
      this.$socket.emit('reveal', {
        room: this.room,
        username: this.submittedPlayers[index].name
      })
    },
    onVote (index) {
      this.$socket.emit('vote', {
        room: this.room,
        voteFor: this.submittedPlayers[index].name,
        voter: this.username
      })
    },
    getSubmission: function (player) {
      if (player.name === this.username && !this.isDealer) {
        return player.submission // Your own submission should always be revealed, unless you are the dealer
      }
      return this.submissionRevealed(player) ? player.submission : '?'
    },
    submissionRevealed: function (player) {
      return player.submissionRevealed
    }
  },
  computed: {
    ...mapState({
      username: state => state.username,
      pickCount: state => state.game.black_card.pick,
      blackCardText: state => state.game.black_card.text,
      hand: state => Object.keys(state.game.players[state.username].hand),
      dealer: state => state.game.dealer,
      players: state => state.game.players
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
    voteDisabled: function () {
      return this.players[this.username].hasVoted
    }
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
  padding-bottom: 0px;
}
.card-actions {
  position: absolute;
  bottom: 0;
}
</style>
