<template>
  <v-layout align-start justify-center text-xs-center row wrap>
    <v-flex lg3 md5 sm8 xs12>
      <v-card class="mt-10 text-xs-left">
        <join-form></join-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import JoinForm from '../components/JoinForm'

export default {
  name: 'Home',

  components: {
    JoinForm
  }
}
</script>
