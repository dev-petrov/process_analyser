<template>
  <b-container @keyup.enter="login">
    <b-row class="mt-5">
      <b-col cols="12"><h1>Детектор аномалий</h1></b-col>
    </b-row>
    <b-row>
      <b-col class="my-1" sm="7" order-sm="1" order="12"
        >
        <!-- <b-img class="w-75" :src="hackLogo"></b-img> -->
        <h3 class="mt-2">
          Панель просмотра аномалий.
        </h3></b-col
      >
      <b-col class="my-1" order-sm="12" order="1" sm="5">
        <b-card>
          <v-text-field label='Токен' v-model="token" type="password"></v-text-field>
          <v-btn @click="login" block color="primary">Войти</v-btn>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      token: "",
    };
  },
  methods: {
    async login() {
      await this.$store.dispatch("login", {
        token: this.token,
      });
      this.$router.replace({ name: "MainPage" });
    },
  },
  beforeMount() {
    if (this.$store.state.isAuthenticated) {
      this.$router.replace({ name: "MainPage" });
    }
  },
};
</script>

<style>
.temp {
  width: 80px;
}
</style>