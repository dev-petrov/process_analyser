<template>
  <div>
    <v-dialog
      v-model="showDiffModal"
      @click:outside="normal_state_differ = []"
    >
      <v-card>
        <v-card-title class="text-h5"> Различающиеся признаки </v-card-title>
        <v-data-table :headers="diff_headers" :items="normal_state_differ">
          <template v-slot:item.self_interval="{ item }">
            <span
              >{{ item.self_interval }}</span
            >
          </template>
          <template v-slot:item.state_interval="{ item }">
            <span>{{ item.state_interval }}</span>
          </template>
        </v-data-table>
      </v-card>
    </v-dialog>
    <h1 class="ml-2 mt-3">
      Аномалия
      {{ new Date(Date.parse(anomaly.dttm) + tzOffset).toLocaleString() }}
    </h1>
    <v-row class="my-2">
      <v-col>
        <v-card>
          <v-card-title>Ближайшие нормальные состояния ({{anomaly.reason.closest_states.length}})</v-card-title>
          <v-data-table
            :loading="loading"
            :headers="normal_states_headers"
            :items="
              anomaly.reason.closest_states.map((v) => ({
                diff_len: v.length,
                items: [...v],
              }))
            "
            :items-per-page="5"
            @click:row="(row) => (normal_state_differ = [...row.items])"
          >
          </v-data-table>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <v-card-title>Агрегированное значение</v-card-title>
          <v-data-table
            :loading="loading"
            :headers="aggregated_headers"
            :items="aggregated"
            :items-per-page="5"
          >
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <v-card>
      <v-card-title>
        <v-row>
          <v-col cols="3"> Процессы за период </v-col>
          <v-col>
            <div>
              <v-select
                v-model="selectedHeaders"
                :items="headers"
                item-value="value"
                label="Выберите колонки"
                multiple
                outlined
              >
                <template v-slot:selection="{ item, index }">
                  <v-chip v-if="index < 5">
                    <span>{{ item.text }}</span>
                  </v-chip>
                  <span v-if="index === 5" class="grey--text caption"
                    >(ещё +{{ selectedHeaders.length - 2 }})</span
                  >
                </template>
              </v-select>
            </div>
          </v-col>
          <v-col cols="1">
            <div class="d-flex align-items-center justify-content-end">
              <v-tooltip bottom open-delay="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mx-1"
                    v-bind="attrs"
                    v-on="on"
                    icon
                    @click="downloadReport"
                  >
                    <v-icon color="gray" v-bind="attrs" v-on="on">
                      download
                    </v-icon>
                  </v-btn>
                </template>
                <span>Скачать</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </v-card-title>
      <v-data-table
        :loading="loading"
        :headers="showHeaders"
        :items="raw_values"
      >
        <template v-slot:item.dttm="{ item }">
          <span>{{
            new Date(Date.parse(item.dttm) + tzOffset).toLocaleString()
          }}</span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";
import http from "../http";

export default {
  data() {
    return {
      aggregated_headers: [
        { text: "Название", value: "name" },
        { text: "Значение", value: "value" },
      ],
      normal_states_headers: [
        { text: "Кол-во разлчиающихся признаков", value: "diff_len" },
      ],
      diff_headers: [
        { text: "Название", value: "field" },
        { text: "Интервал нормального состояния", value: "self_interval" },
        { text: "Интервал аномалии", value: "state_interval" },
      ],
      headers: [
        { text: "Время", value: "dttm" },
        { text: "ID процесса", value: "pid" },
        { text: "Имя процесса", value: "name" },
        { text: "Имя пользователя", value: "username" },
        { text: "ID родительского процесса", value: "ppid" },
        { text: "Имя родительского процесса", value: "parent_name" },
        { text: "Потребление процессора, %", value: "cpu_percent" },
        { text: "Потребление ОЗУ, %", value: "memory_percent" },
        { text: "Количество потоков", value: "num_threads" },
        { text: "Терминал", value: "terminal" },
        { text: "Приоритет", value: "nice" },
        { text: "Команда запуска", value: "cmdline" },
        { text: "Исполняемый файл", value: "exe" },
        { text: "Статус", value: "status" },
        { text: "Время запуска", value: "create_time" },
        { text: "Кол-во открытых соединений", value: "connections" },
        { text: "Кол-во открытых файлов", value: "open_files" },
      ],
      normal_state_differ: [],
      raw_values: [],
      selectedHeaders: [
        "dttm",
        "pid",
        "name",
        "username",
        "cpu_percent",
        "memory_percent",
        "num_threads",
        "status",
        "connections",
        "open_files",
      ],
      anomaly: {
        reason: { closest_states: [] },
      },
      loading: true,
    };
  },
  async mounted() {
    this.loading = true;
    this.anomaly = (
      await http.getItem("Anomaly", this.$route.params.id, true)
    ).data;
    this.raw_values = (
      await http.getList("ClosestRawValue", { dttm: this.anomaly.dttm }, true)
    ).data;
    this.loading = false;
  },
  computed: {
    showHeaders() {
      return this.headers.filter((s) => this.selectedHeaders.includes(s.value));
    },
    tzOffset() {
      const date = new Date();
      return -1 * date.getTimezoneOffset() * 60 * 1000;
    },
    aggregated() {
      var result = [];
      let aggregated_values = this.anomaly.reason.aggregated;
      for (const key in aggregated_values) {
        result.push({
          name: key,
          value: aggregated_values[key],
        });
      }
      return result;
    },
    showDiffModal() {
      return this.normal_state_differ.length
    }
  },
  methods: {
    downloadReport() {
      axios
        .get(`/api/closest_raw_values_report/?dttm=${this.anomaly.dttm}`, {
          responseType: "blob",
          headers: http.getHeaders(),
        })
        .then((response) => {
          const filename =
            response.headers["content-disposition"].split("=")[1];
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", filename);
          document.body.appendChild(link);
          link.click();
        });
    },
  },
};
</script>

<style>
</style>