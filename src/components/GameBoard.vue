<template>
  <v-container>
    <v-row align="start" justify="center" wrap>
      <v-col v-for="card in hand" :key="card" lg="1" md="3" sm="5" xs="12">
        <v-card class="mt-10 text-xs-left">
          <v-card-text class="cn-text">{{ card }}</v-card-text>
          <v-card-actions>
            <v-btn color="grey darken-2" class="white--text" @click="joinGame">Select</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'game-board',
  data () {
    return {
    }
  },
  computed: {
    ...mapState({
      hand: state => Object.keys(state.game.players[state.username].hand), // .players[state.username].hand,
      username: state => state.username
    })
  }
}
</script>
