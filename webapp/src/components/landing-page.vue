<template>
  <v-container>
    <v-row class="text-center">
      <v-col>
        <v-card max-width="700" class="mx-auto">
          <v-toolbar color="blue" dark>
            <v-text-field  :label="'Zoek in ' + nrOfRecipes + ' recepten'"
            prepend-icon="mdi-magnify" @keydown="search" v-model="query" hide-detailscyan single-line></v-text-field>
          </v-toolbar>
          <v-subheader class="text-uppercase" v-if="displayRecipes.length===0">Geen resultaten</v-subheader>
          <v-list three-line v-if="displayRecipes.length>0">
            <template v-for="(item, index) in displayRecipes">
              <v-subheader
                v-if="item.header"
                :key="item.header"
                v-text="item.header"
              ></v-subheader>

              <v-divider
                v-else-if="item.divider"
                :key="index"
                :inset="item.inset"
              ></v-divider>

              <v-list-item
                v-else
                :key="item.title"
                :to="{ name: 'recipe', params: { recipeSlug: item.slug } }"
              >
                <v-list-item-content>
                  <v-list-item-title v-html="item.title"></v-list-item-title>
                  <v-list-item-subtitle
                    v-html="item.subtitle"
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import recipes from "../assets/recipes.json";
import Fuse from "fuse.js";
export default {
  name: "LandingPage",
  data: () => ({
    recipes: recipes,
    displayRecipes: [],
    query: "",
    fuse: "fuse",
  }),
  mounted() {
    this.init()
  },
  computed: {
    nrOfRecipes(){
      return this.recipes.length
    }
  },
  methods: {
    search() {
      setTimeout(() => {
        if (this.query === "") {
          console.log("search query empty")
          this.displayRecipes = this.recipes
        }else{
          console.log("search query not empty")
          const searchResult = this.fuse.search(this.query, {});
          console.log(searchResult)
          this.displayRecipes = searchResult.map(({ item }) => item).sort(this.compare);
        }
      })
    },
    init() {
      this.displayRecipes = this.recipes;
      const options = {
        shouldSort: true,
        threshold: 0.3,
        location: 0,
        distance: 100,
        minMatchCharLength: 3,
        ignoreLocation: true,
        keys: ["title", "subtitle"],
      };
      this.fuse = new Fuse(this.recipes, options);
      this.search();
    },
  },
};
</script>
