<template>
  <v-app-bar color="light-blue" dark app>
    <v-toolbar-title
      ><router-link to="/" class="text-white"
        >Детектор аномалий</router-link
      ></v-toolbar-title
    >
    <v-spacer></v-spacer>

      <v-btn plain @click="logout" v-if="$store.state.isAuthenticated">
        Выйти
      </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  methods: {
      async logout () {
          await this.$store.dispatch('logout'); 
          this.$router.replace({name: 'Login'});
      }
  }
};
</script>

<style>
</style>