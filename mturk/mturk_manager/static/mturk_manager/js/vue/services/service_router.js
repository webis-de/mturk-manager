import VueRouter from 'vue-router';
import {store} from '../store/index.js';

import app_dashboard from '../components/dashboard/app_dashboard.vue';
import app_connection_error from '../components/connection_error/app_connection_error.vue';
import app_project from '../components/project/app_project.vue';
import app_batches from '../components/batches/app_batches.vue';
import app_hits from '../components/hits/app_hits.vue';
import app_assignments from '../components/assignments/app_assignments.vue';
import app_finances from '../components/finances/app_finances.vue';
import AppQualifications from '../components/qualifications/AppQualifications.vue';
import app_workers from '../components/workers/app_workers.vue';
import AppSettingsProject from '../components/settings_project/app_settings_project.vue';

function parse_params(route)
{
	const result = {};

	for(let key in route.params)
	{
		const value = Number(route.params[key]);
		if(!isNaN(value))
		{
			result[key] = value;
		} else {
			result[key] = route.params[key];
		}
	}

	return result;
}

const routes = [
	{ 
		path: '/', 
		name: 'dashboard',
		component: app_dashboard,
	},
	{ 
		path: '/projects', 
		name: 'projects',
		redirect: { name: 'dashboard' },
		// necessary to allow children
		component: { template: '<router-view></router-view>' },
		children: [
			{ 
				path: ':slug_project',
				name: 'project',
				component: app_project,
				redirect: (to) => {
					return {
						name: 'batches',
						params: {
							slug_project: to.params.slug_project
						}
					}
				},
				props: parse_params,
				children: [
					{ 
						path: 'batches',
						name: 'batches',
						component: app_batches,
						props: parse_params,
					},
					{ 
						path: 'batches/:id_batch',
						name: 'batch',
						component: app_batches,
						props: parse_params,
					},
					{ 
						path: 'hits',
						name: 'hits',
						component: app_hits,
						props: parse_params,
					},
					{ 
						path: 'hits/:id_hit',
						name: 'hit',
						component: app_hits,
						props: parse_params,
					},
					{ 
						path: 'assignments',
						name: 'assignments',
						component: app_assignments,
						props: parse_params,
					},
					{ 
						path: 'assignments/:id_assignment',
						name: 'assignment',
						component: app_assignments,
						props: parse_params,
					},
					{ 
						path: 'finances', 
						name: 'finances',
						component: app_finances,
					},
					{ 
						path: 'workers', 
						name: 'workers',
						component: app_workers,
					},
					// { 
					// 	path: '/qualifications', 
					// 	name: 'Qualifications',
					// 	component: AppQualifications,
					// },
					{ 
						path: 'settings_project', 
						name: 'settings_project',
						component: AppSettingsProject,
					},
				]
			},
		]
	},
	{ 
		path: '/connection_error', 
		name: 'connection_error',
		component: app_connection_error,
	},
];

const router = new VueRouter({
  routes // short for `routes: routes`
});

router.beforeEach((to, from, next) => {
	console.log('from', from)
	console.log('to', to)
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

export default router;