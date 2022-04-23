<template>
  <v-card>
    <v-card-title>
      <v-row>
        <v-col cols="7">
          Процессы за период для аномалии
          {{ new Date(Date.parse(anomaly.dttm) + tzOffset).toLocaleString() }}
        </v-col>
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
                <v-chip v-if="index < 2">
                  <span>{{ item.text }}</span>
                </v-chip>
                <span v-if="index === 2" class="grey--text caption"
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
    <v-data-table :loading="loading" :headers="showHeaders" :items="raw_values">
      <template v-slot:item.dttm="{ item }">
        <span>{{
          new Date(Date.parse(item.dttm) + tzOffset).toLocaleString()
        }}</span>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import axios from "axios";
import http from "../http";

export default {
  data() {
    return {
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
      anomaly: {},
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