// import Vue from 'vue/dist/vue.common';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import Vuex from 'vuex';
import Vuelidate from 'vuelidate'
import App from './App.vue';
import app_dashboard from './components/dashboard/app_dashboard.vue';
import app_batches from './components/batches/app_batches.vue';
import app_hits from './components/hits/app_hits.vue';
import AppFinances from './components/finances/AppFinances.vue';
import AppQualifications from './components/qualifications/AppQualifications.vue';
import AppWorkers from './components/workers/AppWorkers.vue';
import AppSettingsProject from './components/settings_project/app_settings_project.vue';
import {store} from './store/index.js';
import UploadButton from 'vuetify-upload-button';

import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.use(UploadButton);
Vue.use(Vuelidate);

const routes = [
	{ 
		path: '/', 
		name: 'dashboard',
		component: app_dashboard,
	},
	{ 
		path: '/projects', 
		redirect: {name: 'dashboard'},
	},
	{ 
		path: '/projects/:slug_project/batches',
		name: 'batches',
		component: app_batches,
	},
	{ 
		path: '/projects/:slug_project/hits',
		name: 'hits',
		component: app_hits,
	},
	{ 
		path: '/projects/:slug_project/hits/:id_hit',
		name: 'hit',
		component: app_hits,
	},
	{ 
		path: '/projects/:slug_project/finances', 
		name: 'finances',
		component: AppFinances,
	},
	// { 
	// 	path: '/qualifications', 
	// 	name: 'Qualifications',
	// 	component: AppQualifications,
	// },
	{ 
		path: '/projects/:slug_project/workers', 
		name: 'workers',
		component: AppWorkers,
	},
	{ 
		path: '/projects/:slug_project/settings_project', 
		name: 'settings_project',
		component: AppSettingsProject,
	},
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

router.beforeEach((to, from, next) => {
	console.log(to)
	console.log(from)
	if(to.name == 'dashboard')
	{
		store.dispatch('moduleProjects/set_slug_project_current', null);
	} else {
		// if(store.getters['moduleProjects/get_slug_project_current'] == null)
		// {
		// 	console.log('redirected');
		// 	next({name: 'dashboard'});
		// }
	}
	next();
});

new Vue({
	router,
	store,
	el: '#app',
	render: h => h(App)
});