import VueRouter from 'vue-router';
import { Service_Projects } from './services/service_projects';
import viewDashboard from './views/dashboard/dashboard.view';
import viewAddCredentials from './views/add-credentials/add-credentials.view';
import viewConnectionError from './views/connection-error/connection-error.view';
import viewProject from './views/project/project.view';
import viewTasks from './views/tasks/tasks.view';
import app_batches from './components/batches/app_batches';
import app_hits from './components/hits/app_hits';
import app_assignments from './components/assignments/app_assignments';
import viewFinances from './views/finances/finances.view';
import viewWorkers from './views/workers/workers.view';
import AppSettingsProject from './views/settings-project/settings-project.view';
import { store } from './store/vuex';
import { Service_App } from './services/service.app';
import queue from './queue';

function parse_params(route) {
  const result = {};

  for (const key in route.params) {
    const value = Number(route.params[key]);
    if (!isNaN(value)) {
      result[key] = value;
    } else {
      result[key] = route.params[key];
    }
  }

  return result;
}

// function loadView(view) {
//   return () => import(/* webpackChunkName: "view-[request]" */ `../components/hits/app_hits.vue`)
// }

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: viewDashboard,
  },
  {
    path: '/add_credentials',
    name: 'add_credentials',
    component: viewAddCredentials,
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
        component: viewProject,
        redirect: to => ({
          name: 'batches',
          params: {
            slug_project: to.params.slug_project,
          },
        }),
        props: parse_params,
        children: [
          {
            path: 'tasks',
            name: 'tasks',
            meta: {
              name: 'Tasks',
            },
            component: viewTasks,
            props: parse_params,
          },
          {
            path: 'batches',
            name: 'batches',
            meta: {
              name: 'Batches',
            },
            component: app_batches,
            props: parse_params,
          },
          {
            path: 'batches/:id_batch',
            name: 'batch',
            meta: {
              name: 'Batch',
            },
            component: app_batches,
            props: parse_params,
          },
          {
            path: 'hits',
            name: 'hits',
            meta: {
              name: 'HITs',
            },
            component: app_hits,
            props: parse_params,
          },
          {
            path: 'hits/:id_hit',
            name: 'hit',
            meta: {
              name: 'HIT',
            },
            component: app_hits,
            props: parse_params,
          },
          {
            path: 'assignments',
            name: 'assignments',
            meta: {
              name: 'Assignments',
            },
            component: app_assignments,
            props: parse_params,
          },
          {
            path: 'assignments/:id_assignment',
            name: 'assignment',
            meta: {
              name: 'Assignment',
            },
            component: app_assignments,
            props: parse_params,
          },
          {
            path: 'finances',
            name: 'finances',
            meta: {
              name: 'Finances',
            },
            component: viewFinances,
          },
          {
            path: 'workers',
            name: 'workers',
            meta: {
              name: 'Workers',
            },
            component: viewWorkers,
          },
          // {
          // 	path: '/qualifications',
          // 	name: 'Qualifications',
          // 	component: AppQualifications,
          // },
          {
            path: 'settings_project',
            name: 'settings_project',
            meta: {
              name: 'Project Settings',
            },
            component: AppSettingsProject,
          },
        ],
      },
    ],
  },
  {
    path: '/connection_error',
    name: 'connection_error',
    component: viewConnectionError,
  },
];

export const router = new VueRouter({
  routes,
});

queue.listen('router', (payload) => {
  router.push(payload);
});

router.beforeEach((to, from, next) => {
  // console.log('from', from);
  // console.log('to', to);
  if (to.matched[0].name !== 'projects') {
    Service_Projects.ping();
  }

  Service_Projects.set_slug_current(to.params.slug_project);
  next();
});

// go to add_credentials if there are no credentials stored and the target route is not already add_credentials
router.beforeEach(async (to, from, next) => {
  if (
    store.getters['module_app/has_credentials'] === false
    && to.name !== 'add_credentials'
  ) {
    const response = await Service_App.init();
    if (response.reason === 'load_credentials') {
      next({ name: 'add_credentials' });
      return;
    } else if(response.exception !== undefined) {
      //some exception occured fetching data from the server
      return;
    }
  }

  // console.log('to', to);
  // console.log('from', from);
  next();
});
