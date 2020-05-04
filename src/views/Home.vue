<template>
  <v-container>
    <span class="title">An online version of Cards Against Humanity&trade;</span>
    <v-row align="start" justify="center">
      <v-col lg="5" md="6" sm="7" cols="12">
        <v-card class="mt-8 text-xs-left">
          <v-toolbar
            color="grey darken-2"
            dark
            flat
          >
            <v-toolbar-title class="subtitle-1">Join a game or start a new one</v-toolbar-title>
          </v-toolbar>
          <join-form v-if="showJoin"></join-form>
          <create-form v-else></create-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex'
import JoinForm from '../components/JoinForm'
import CreateForm from '../components/CreateForm'

export default {
  name: 'Home',
  data () {
    return {
    }
  },
  methods: {
    ...mapMutations(['reset_error', 'set_join'])
  },
  computed: {
    showJoin () {
      return this.$store.state.showJoin
    }
  },
  components: {
    JoinForm,
    CreateForm
  },
  mounted () {
    this.set_join(true)
    this.reset_error()
  }
}
</script>
