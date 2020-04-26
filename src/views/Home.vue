<template>
  <v-container>
    <v-row align="start" justify="center">
      <v-col lg="5" md="6" sm="7" xs="12">
        <v-card class="mt-10 text-xs-left">
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
import JoinForm from '../components/JoinForm'
import CreateForm from '../components/CreateForm'

export default {
  name: 'Home',
  data () {
    return {
      isJoin: true
    }
  },
  methods: {
    toggleIsJoin () {
      console.log('got here')
      this.isJoin = !this.isJoin
    }
  },
  computed: {
    showJoin () {
      return this.$store.state.showJoin
    }
  },
  components: {
    JoinForm,
    CreateForm
  }
}
</script>
