<template>
  <v-app>
    <v-main>
     <router-view></router-view>
    </v-main>
    <v-footer
      padless
    >
      <v-card
        flat
        tile
        width="100%"
        class="grey darken-2' text-center"
      >
        <v-card-text>
          <v-btn
            href="https://github.com/arbakker/kook"
            target="_blank"
            class="mx-4"
            icon
          >
            <v-icon size="24px">
              mdi-github
            </v-icon>
          </v-btn>
        </v-card-text>
        <v-card-text>
          KOOK - <a href="https://github.com/arbakker">arbakker's</a> persoonlijke kookboek
        </v-card-text>
      </v-card>
  </v-footer>
  </v-app>
  
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
};
</script>
