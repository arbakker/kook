<template>
  <v-container>
    <v-row class="text-center">
      <v-col>
        <v-card max-width="700" class="mx-auto">
          <v-card-text>Deze applicatie is beveiligd met een wachtwoord</v-card-text>
          <v-form
            @submit.prevent="validateBeforeSubmit"
            style="padding: 0.5em"
            ref="form"
            lazy-validation>
            <v-text-field
              v-model="password"
              type="password"
              counter
              label="Wachtwoord"
              required
              :rules="rules"
              ></v-text-field>

            <v-btn color="primary" type="submit" @click="validateBeforeSubmit">
              OK
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      password: null,
      rules: [
        (value) => {
          if (!this.matchLogin(value)) {
            return "wachtwoord is niet correct";
          }
          return true;
        },
      ]
    };
  },
  methods: {
    matchLogin(val) {
      const check = process.env.VUE_APP_PASSWORD;
      var check_decoded = atob(check);
      return val === check_decoded;
    },
    validateBeforeSubmit() {
      if (this.matchLogin(this.password)) {
        localStorage.setItem("user-password", this.password);
        this.$router.push("home");
      }
    },
  },
};
</script>