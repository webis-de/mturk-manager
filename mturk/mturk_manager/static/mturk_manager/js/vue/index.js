// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import Vuex from 'vuex';
import App from './App.vue';
import AppFinances from './components/finances/AppFinances.vue';
import AppQualifications from './components/qualifications/AppQualifications.vue';
import AppWorkers from './components/workers/AppWorkers.vue';
import {store} from './store/index.js';

import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.use(Vuetify)
Vue.use(VueRouter)

const routes = [
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