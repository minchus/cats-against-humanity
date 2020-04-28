<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      right
    >
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-contact-mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Contact</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="grey darken-4"
      dark
    >
      <v-img
        alt="Cat Logo"
        class="shrink mr-2"
        contain
        src="@/assets/white-cat-icon.svg"
        transition="scale-transition"
        width="45"
      />
      <v-toolbar-title class="ml-1">Cats Against Humanity</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>

    <v-footer
      color="grey darken-4"
      app
    >
    </v-footer>

  </v-app>
</template>

<script>
export default {
  name: 'App',

  props: {
    source: String
  },

  data: () => ({
    drawer: null
  })
}
</script>
