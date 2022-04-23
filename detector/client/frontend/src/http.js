import Axios from 'axios';
import Vue from 'vue';

export default {
    urls: {
        Anomaly: '/api/anomaly/',
        ClosestRawValue: '/api/closest_raw_values/',
    },
    getFilterValues: async function (filters) {
        var filter = "";
        if (Object.keys(filters).length != 0) {
            filter = "?";
            for (const key in filters) {
                const element = filters[key];
                filter += `${key}=${element}&`;
            }
            filter = filter.slice(0, filter.lastIndexOf('&'))

        }
        return filter
    },
    getHeaders() {
        return {
            'Authorization': `Token ${localStorage.getItem("api_token")}`,
        }
    },
    getList: async function (url_name, filters = {}, raise_exception = false) {
        var filter = (await this.getFilterValues(filters));
        try {
            return (await Axios.get(`${this.urls[url_name]}${filter}`, { headers: this.getHeaders() }))
        } catch (error) {
            if (raise_exception) {
                Vue.showErrorModal(error.response.data);
                return { data: [] }
            }
            return error.response;
        }
    },
    getItem: async function (url_name, id, raise_exception = false) {
        try {
            return (await Axios.get(`${this.urls[url_name]}${id}/`, { headers: this.getHeaders() }))
        } catch (error) {
            if (raise_exception) {
                Vue.showErrorModal(error.response.data);
                return { data: {} }
            }
            return error.response;
        }
    },
    createItem: async function (url_name, data, raise_exception = false) {
        try {
            return (await Axios.post(`${this.urls[url_name]}`, data, { headers: this.getHeaders() }))
        } catch (error) {
            if (raise_exception) {
                Vue.showErrorModal(error.response.data);
                return { data: data };
            }
            return error.response;
        }
    },
    updateItem: async function (url_name, id, data, raise_exception = false) {
        try {
            return (await Axios.put(`${this.urls[url_name]}${id}/`, data, { headers: this.getHeaders() }))
        } catch (error) {
            if (raise_exception) {
                Vue.showErrorModal(error.response.data);
                return { data: data };
            }
            return error.response;
        }
    },
    deleteItem: async function (url_name, id, raise_exception = false) {
        try {
            return (await Axios.delete(`${this.urls[url_name]}${id}/`, { headers: this.getHeaders() }))
        } catch (error) {
            if (raise_exception) {
                Vue.showErrorModal(error.response.data);
            }
            return error.response;
        }
    }
}
