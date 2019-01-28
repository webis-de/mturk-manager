// import "@babel/polyfill";

import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import Vuelidate from 'vuelidate'
import App from './App.vue';
import { store } from './store/vuex.js';
import UploadButton from 'vuetify-upload-button';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'vuetify/dist/vuetify.min.css';

import {router} from './services/service_router'

Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.use(UploadButton);
Vue.use(Vuelidate);

new Vue({
	router,
	store,
	el: '#app',
	render: h => h(App)
});