// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import Vuex from 'vuex';
import App from './App.vue';
import app_batches from './components/batches/app_batches.vue';
import AppFinances from './components/finances/AppFinances.vue';
import AppQualifications from './components/qualifications/AppQualifications.vue';
import AppWorkers from './components/workers/AppWorkers.vue';
import {store} from './store/index.js';
import UploadButton from 'vuetify-upload-button';

import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.use(UploadButton);

const routes = [
	{ 
		path: '/batches', 
		name: 'Batches',
		component: app_batches,
	},
	{ 
		path: '/finances', 
		name: 'Finances',
		component: AppFinances,
	},
	{ 
		path: '/qualifications', 
		name: 'Qualifications',
		component: AppQualifications,
	},
	{ 
		path: '/workers', 
		name: 'Workers',
		component: AppWorkers,
	},
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

new Vue({
	router,
	store,
	el: '#app',
	render: h => h(App)
});