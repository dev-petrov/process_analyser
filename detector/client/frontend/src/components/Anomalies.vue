<template>
  <div>
    <v-data-table
      :loading="loading"
      class="elevation-1"
      :items="$store.state.anomalies"
      :headers="headers"
      @click:row="
        (row) =>
          $router.push({
            name: 'ClosestRawValues',
            query: {
              ...$route.query,
            },
            params: {
              id: row.id,
            },
          })
      "
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="6">
            <v-toolbar-title class="ml-5 mt-3">Аномалии</v-toolbar-title>
          </v-col>
        </v-row>
      </template>
      <template v-slot:item.dttm="{ item }">
        <span>{{ new Date(Date.parse(item.dttm) + tzOffset).toLocaleString() }}</span>
      </template>
      <template v-slot:item.reason="{ item }">
        <span>{{ item.reason.slice(0, 100) }}...</span>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "Время",
          value: "dttm",
        },
        {
          text: "Причина",
          value: "reason",
        },
      ],
      loading: true,
    };
  },
  async mounted() {
    this.loading = true;
    if (this.$store.state.anomalies.length == 0) {
      await this.$store.dispatch("setAnomalies");
    }
    this.loading = false;
  },
  computed:{
      tzOffset() {
        const date = new Date();
        return -1 * date.getTimezoneOffset() * 60 * 1000;
      },
  }
};
</script>

<style>
</style>