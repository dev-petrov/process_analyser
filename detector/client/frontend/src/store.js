import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'

Vue.use(Vuex)

const state = () => ({
    user: null,
    isAuthenticated: false,
    anomalies: [],
})

const store = new Vuex.Store({
    state: state,
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setAnomalies(state, value) {
            state.anomalies = value;
        }
    },
    actions: {
        async setAnomalies(context) {
            let anomalies = (await http.getList('Anomaly', {}, true)).data;
            context.commit('setAnomalies', anomalies);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var token = creds.token;
            localStorage.setItem("api_token", token)
            var status = false;
            try {
                await Axios.get("/check_token", { headers: http.getHeaders() });
                status = true;
            } catch (error) {
                localStorage.removeItem("api_token")
                var data = error.response.data;
                if (data.detail) {
                    Vue.showErrorModal(data.detail);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            localStorage.removeItem("api_token")
            context.commit('setAuthenticated', false);
        },
        async checkAuth(context) {
            context.commit('setAuthenticated', true);
            try {
                var result = await Axios.get("/check_token", { headers: http.getHeaders() });
                if (result.status != 200) {
                    context.commit('setAuthenticated', false);
                    return
                }
                context.commit('setAuthenticated', true);
            } catch (e) {
                context.commit('setAuthenticated', false);
            }
        },
    }
})

export default store;
