import Vue from 'vue'
import Vuetify from 'vuetify'
import Vuex from 'vuex'
import App from './AppMoney.vue';
import {store} from './store/index.js';

import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.use(Vuetify)

new Vue({
  store,
  el: '#app',
  render: h => h(App)
});