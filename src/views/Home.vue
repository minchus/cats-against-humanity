<template>
  <v-layout align-start justify-center text-xs-center row wrap>
    <v-flex lg3 md5 sm8 xs12>
      <v-card class="mt-10 text-xs-left">
        <landing-form></landing-form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import LandingForm from '../components/LandingForm'

export default {
  name: 'Home',

  components: {
    LandingForm
  }
}
</script>
