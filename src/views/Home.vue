<template>
  <v-layout align-start justify-center text-xs-center row wrap>
    <v-flex lg3 md5 sm8 xs12>
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
    </v-flex>
  </v-layout>
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
