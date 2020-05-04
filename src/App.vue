<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      right
      disable-resize-watcher
      dark
    >
      <v-list dense>
        <v-list-item link to="/">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item link to="/about">
          <v-list-item-action>
            <v-icon>mdi-help</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="grey darken-4"
      dark
    >
      <router-link to="/" title="home">
      <v-img
        alt="Cat Logo"
        class="shrink"
        contain
        src="./assets/cat-white.svg"
        transition="scale-transition"
        width="50"
      />
      </router-link>

      <router-link to="/" title="Home" style="text-decoration:none;">
        <v-toolbar-title class="headline ml-3 white--text">Cats Against Humanity</v-toolbar-title>
      </router-link>

      <v-spacer></v-spacer>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>

    <v-footer color="grey darken-4" app></v-footer>

  </v-app>
</template>

<script>
export default {
  name: 'App',

  props: {
    source: String
  },

  data: () => ({
    drawer: false
  }),

  mounted () {
    this.$socket.emit('list_decks')
  }
}
</script>
