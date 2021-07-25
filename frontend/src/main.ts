import '@mdi/font/css/materialdesignicons.css';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify/lib';
import { Ripple } from 'vuetify/lib/directives';
import Vuelidate from 'vuelidate';
import axios from 'axios';
import VueAxios from 'vue-axios';
import Vuex from 'vuex';
import VueCookies from 'vue-cookies';
import VueCompositionApi from '@vue/composition-api';
import App from '@/App.vue';
import { store } from './store/vuex';

import { router } from './router';
import { vuetify } from './vuetify';

import './assets/main.scss';
import { apolloProvider } from './vue-apollo';

Vue.config.performance = process.env.NODE_ENV === 'development';

Vue.use(Vuetify, { directives: { Ripple } });
Vue.use(VueRouter);
Vue.use(Vuelidate);
Vue.use(VueAxios, axios);
Vue.use(Vuex);
Vue.use(VueCookies);
Vue.use(VueCompositionApi);

export default new Vue({
  router,
  store,
  vuetify,
  el: '#app',
  apolloProvider,
  render: (h) => h(App),
});
