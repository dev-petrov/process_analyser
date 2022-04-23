import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import ru from 'vuetify/lib/locale/ru'
import en from 'vuetify/lib/locale/en'

Vue.use(Vuetify);

const opts = {
    lang: {
        current: 'ru',
        locales: { ru, en },
    }
}

export default new Vuetify(opts);