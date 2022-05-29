<template>
  <div id="app">
    <v-app>
      <nav-bar />
      <v-main>
          <router-view></router-view>
      </v-main>
      <v-dialog v-model="showErrorModal" max-width="300">
        <v-card>
          <v-card-title class="text-h5"> Ошибка </v-card-title>

          <v-card-text>
            {{ modalContent }}
          </v-card-text>

          <v-card-actions>
            <v-btn color="green darken-1" text @click="showErrorModal = false">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import ErrorModal from "./plugins/ErrorModal";

export default {
  components: { NavBar },
  name: "app",
  data() {
    return {
      showErrorModal: false,
      modalContent: null,
    };
  },
  async beforeMount() {
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
  },
};
</script>
<style>
a {
  text-decoration: none !important;
}
</style>
