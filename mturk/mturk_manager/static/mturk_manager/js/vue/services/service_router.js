// import VueRouter from 'vue-router';


// const routes = [
// 	{
// 		path: '/',
// 		name: 'dashboard',
// 		component: app_dashboard,
// 	},
// 	{
// 		path: '/add_credentials',
// 		name: 'add_credentials',
// 		component: add_credentials,
// 	},
// 	{
// 		path: '/projects',
// 		name: 'projects',
// 		redirect: { name: 'dashboard' },
// 		// necessary to allow children
// 		component: { template: '<router-view></router-view>' },
// 		children: [
// 			{
// 				path: ':slug_project',
// 				name: 'project',
// 				component: app_project,
// 				redirect: (to) => {
// 					return {
// 						name: 'batches',
// 						params: {
// 							slug_project: to.params.slug_project
// 						}
// 					}
// 				},
// 				props: parse_params,
// 				children: [
// 					{
// 						path: 'batches',
// 						name: 'batches',
// 						meta: {
// 							name: 'Batches'
// 						},
// 						component: app_batches,
// 						props: parse_params,
// 					},
// 					{
// 						path: 'batches/:id_batch',
// 						name: 'batch',
// 						meta: {
// 							name: 'Batch'
// 						},
// 						component: app_batches,
// 						props: parse_params,
// 					},
// 					{
// 						path: 'hits',
// 						name: 'hits',
// 						meta: {
// 							name: 'HITs'
// 						},
// 						component: loadView(),
// 						props: parse_params,
// 					},
// 					{
// 						path: 'hits/:id_hit',
// 						name: 'hit',
// 						meta: {
// 							name: 'HIT'
// 						},
// 						component:  loadView(),
// 						// component: app_hits,
// 						props: parse_params,
// 					},
// 					{
// 						path: 'assignments',
// 						name: 'assignments',
// 						meta: {
// 							name: 'Assignments'
// 						},
// 						component: app_assignments,
// 						props: parse_params,
// 					},
// 					{
// 						path: 'assignments/:id_assignment',
// 						name: 'assignment',
// 						meta: {
// 							name: 'Assignment'
// 						},
// 						component: app_assignments,
// 						props: parse_params,
// 					},
// 					{
// 						path: 'finances',
// 						name: 'finances',
// 						meta: {
// 							name: 'Finances'
// 						},
// 						component: app_finances,
// 					},
// 					{
// 						path: 'workers',
// 						name: 'workers',
// 						meta: {
// 							name: 'Workers'
// 						},
// 						component: app_workers,
// 					},
// 					// {
// 					// 	path: '/qualifications',
// 					// 	name: 'Qualifications',
// 					// 	component: AppQualifications,
// 					// },
// 					{
// 						path: 'settings_project',
// 						name: 'settings_project',
// 						meta: {
// 							name: 'Project Settings'
// 						},
// 						component: AppSettingsProject,
// 					},
// 				]
// 			},
// 		]
// 	},
// 	{
// 		path: '/connection_error',
// 		name: 'connection_error',
// 		component: app_connection_error,
// 	},
// ];
