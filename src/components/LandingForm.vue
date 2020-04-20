<template>
  <v-card class="elevation-12">
    <v-toolbar
      color="grey darken-2"
      dark
      flat
    >
      <v-toolbar-title class="subtitle-1">Join a game or create a new one</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
        <v-text-field
          label="Player name"
          name="username"
          type="text"
        />
      <v-form>
        <v-text-field
          label="Room code (to join existing game)"
          name="room-id"
          type="text"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="grey lighten-2">New game</v-btn>
      <v-spacer />
      <v-btn color="grey darken-2" class="white--text">Join</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'LandingForm',
  props: {
    source: String
  }
}
</script>
