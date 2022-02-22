<template>
  <v-container>
    <v-card max-width="700" class="mx-auto">
      <v-card-title>{{ recipe.title }}</v-card-title>
      <v-card-subtitle>{{ recipe.subtitle }}</v-card-subtitle>
      <v-subheader class="text-uppercase">Beschrijving</v-subheader>
      <v-card-text>{{ recipe.description }}</v-card-text>
      <v-subheader class="text-uppercase">Ingrediënten</v-subheader>
      <v-card-actions>
          <v-btn 
            v-clipboard="ingredients"
            small 
            title="Kopieer ingrediënten naar klembord">
              <v-icon small>mdi-clipboard-check-multiple</v-icon>
            </v-btn>
      </v-card-actions>
      <v-list dense>
        <v-list-item-group>
          <v-list-item v-for="(item, i) in recipe.ingredients" :key="i">
            <v-list-item-content>
              <v-list-item-title v-text="item"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <v-subheader class="text-uppercase">Bereiding</v-subheader>
       <v-expansion-panels
      multiple
    >
      <v-expansion-panel
       v-for="(item, i) in recipe.steps" :key="i"
      >
        <v-expansion-panel-header class="font-weight-bold">{{ item.title }}</v-expansion-panel-header>
        <v-expansion-panel-content>
          {{ item.description }}
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>


     
     
    </v-card>
     <v-btn style="top:2em;"
        color="blue"
        fab
        absolute
        medium
        dark
        top
        right
        :to="{ name: 'home'}"
      > <v-icon>mdi-home</v-icon>
      </v-btn>
  </v-container>

</template>

<script>
export default {
  name: "RecipePage",
  data: () => ({
    recipe: {},
  }),
  mounted() {
    const slug = this.recipeSlug;
    fetch(`/recipes/${slug}.json`)
      .then((response) => response.json())
      .then((data) => (this.recipe = data));
  },
  computed: {
    ingredients: function(){
      
      return this.recipe.ingredients.map(x=> `- ${x}`).join("\n")
    },
    recipeSlug: function () {
      return this.$route.params.recipeSlug;
    },
  },
};
</script>
