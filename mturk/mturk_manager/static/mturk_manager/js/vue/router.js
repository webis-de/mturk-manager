import VueRouter from 'vue-router';
import { Service_Projects } from './services/service_projects';
import ViewDashboard from './views/dashboard/dashboard.view';
import ViewAddCredentials from './views/add-credentials/add-credentials.view';
import ViewConnectionError from './views/connection-error/connection-error.view';
import ViewProject from './views/project/project.view';
import ViewTasks from './views/project/tasks/tasks.view';
import ViewBatches from './views/project/tasks/batches/batches.view';
import ViewHITs from './views/project/tasks/hits/hits.view';
import ViewAssignments from './views/project/tasks/assignments/assignments.view';
import ViewFinances from './views/project/finances/finances.view';
import ViewWorkers from './views/project/workers/workers.view';
import ViewAbout from './views/about/about.view';
import About from './components/about/about';
import AppSettingsProject from './views/project/settings-project/settings-project.view';
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
//   return () => import(/* webpackChunkName: "view-[request]" */ `../components/hits/hits.view.vue`)
// }

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: ViewDashboard,
  },
  {
    path: '/add_credentials',
    name: 'add_credentials',
    component: ViewAddCredentials,
  },
  {
    path: '/about',
    name: 'about',
    component: ViewAbout,
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
        component: ViewProject,
        redirect: to => ({
          name: 'tasks',
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
            component: { template: '<router-view></router-view>' },
            // component: viewTasks,
            // props: parse_params,
            redirect: to => ({
              name: 'tasksBatches',
              params: {
                slug_project: to.params.slug_project,
              },
            }),
            children: [
              {
                path: 'batches',
                name: 'tasksBatches',
                meta: {
                  name: 'Tasks',
                  index: 0,
                },
                component: ViewTasks,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'batch',
                    meta: {
                      name: 'Tasks',
                    },
                    component: ViewBatches,
                    props: parse_params,
                  },
                ],
              },
              {
                path: 'hits',
                name: 'tasksHITs',
                meta: {
                  name: 'Tasks',
                  index: 1,
                },
                component: ViewTasks,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'hit',
                    meta: {
                      name: 'Tasks',
                    },
                    component: ViewHITs,
                    props: parse_params,
                  },
                ],
              },
              {
                path: 'assignments',
                name: 'tasksAssignments',
                meta: {
                  name: 'Tasks',
                  index: 2,
                },
                component: ViewTasks,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'assignment',
                    meta: {
                      name: 'Tasks',
                    },
                    component: ViewAssignments,
                    props: parse_params,
                  },
                ],
              },
            ],
          },
          // {
          //   path: 'batches/:id_batch',
          //   name: 'batch',
          //   meta: {
          //     name: 'Batch',
          //   },
          //   component: app_batches,
          //   props: parse_params,
          // },
          // {
          //   path: 'hits',
          //   name: 'hits',
          //   meta: {
          //     name: 'HITs',
          //   },
          //   component: app_hits,
          //   props: parse_params,
          // },
          // {
          //   path: 'hits/:id_hit',
          //   name: 'hit',
          //   meta: {
          //     name: 'HIT',
          //   },
          //   component: app_hits,
          //   props: parse_params,
          // },
          // {
          //   path: 'assignments',
          //   name: 'assignments',
          //   meta: {
          //     name: 'Assignments',
          //   },
          //   component: app_assignments,
          //   props: parse_params,
          // },
          // {
          //   path: 'assignments/:id_assignment',
          //   name: 'assignment',
          //   meta: {
          //     name: 'Assignment',
          //   },
          //   component: app_assignments,
          //   props: parse_params,
          // },
          {
            path: 'finances',
            name: 'finances',
            meta: {
              name: 'Finances',
            },
            component: ViewFinances,
          },
          {
            path: 'workers',
            name: 'workers',
            meta: {
              name: 'Workers',
            },
            component: ViewWorkers,
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
          {
            path: 'about',
            name: 'aboutProject',
            meta: {
              name: 'About',
            },
            component: {
              template: '<about></about>',
              components: { About },
            },
          },
        ],
      },
    ],
  },
  {
    path: '/connection_error',
    name: 'connection_error',
    component: ViewConnectionError,
  },
];

export const router = new VueRouter({
  routes,
});

queue.listen('router', (payload) => {
  router.push(payload);
});

router.beforeEach((to, from, next) => {
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
    } if (response.exception !== undefined) {
      // some exception occured fetching data from the server
      return;
    }
  }

  next();
});
