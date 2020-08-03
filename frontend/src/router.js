import VueRouter from 'vue-router';
import goTo from 'vuetify/es5/services/goto';
import { ServiceProjects } from './services/projects.service';
// import ViewDashboard from './views/dashboard/dashboard.view';
// import ViewAddCredentials from './views/add-credentials/add-credentials.view';
// import ViewConnectionError from './views/connection-error/connection-error.view';
// import ViewProject from './views/project/project.view';
// import ViewTasks from './views/project/tasks/tasks.view';
// import ViewBatches from './views/project/tasks/batches/batches.view';
// import ViewHITs from './views/project/tasks/hits/hits.view';
// import ViewAssignments from './views/project/tasks/assignments/assignments.view';
// import ViewFinances from './views/project/finances/finances.view';
// import ViewWorkers from './views/project/workers/workers.view';
// import ViewAbout from './views/about/about.view';
// import ViewAdmin from './views/admin/admin.view';
// import ViewSettingsProject from './views/project/settings-project/settings-project.view';
import About from './components/about/about';
// import AppSettingsProject from './views/project/settings-project/settings-project.view';
import { store } from './store/vuex';
import { AppService } from './services/app.service';
import queue from './queue';

const ViewDashboard = () => import(/* webpackChunkName: "dashboard" */ './views/dashboard/dashboard.view');
const ViewAddCredentials = () => import(/* webpackChunkName: "credentials" */ './views/add-credentials/add-credentials.view');
const ViewConnectionError = () => import(/* webpackChunkName: "connection-error" */ './views/connection-error/connection-error.view');
const ViewAbout = () => import(/* webpackChunkName: "about" */ './views/about/about.view');
const ViewAdmin = () => import(/* webpackChunkName: "admin" */ './views/admin/admin.view');
const ViewWorkers = () => import(/* webpackChunkName: "workers" */ './views/project/workers/workers.view');
const ViewFinances = () => import(/* webpackChunkName: "finances" */ './views/project/finances/finances.view');
const ViewAssignment = () => import(/* webpackChunkName: "assignments" */ './views/project/tasks/assignments/assignment.view');
const ViewHIT = () => import(/* webpackChunkName: "hits" */ './views/project/tasks/hits/hit.view');
const ViewBatch = () => import(/* webpackChunkName: "batches" */ './views/project/tasks/batches/batch.view');
const ViewAssignments = () => import(/* webpackChunkName: "assignments" */ './views/project/tasks/assignments/assignments.view');
const ViewHITs = () => import(/* webpackChunkName: "hits" */ './views/project/tasks/hits/hits.view');
const ViewBatches = () => import(/* webpackChunkName: "batches" */ './views/project/tasks/batches/batches.view');
const ViewTasks = () => import(/* webpackChunkName: "tasks" */ './views/project/tasks/tasks.view');
const ViewProject = () => import(/* webpackChunkName: "project" */ './views/project/project.view');
const ViewSettingsProject = () => import(/* webpackChunkName: "settings-project" */ './views/project/settings-project/settings-project.view');

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
    path: '/admin',
    name: 'admin',
    component: ViewAdmin,
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
        redirect: (to) => ({
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
            // component: { template: '<router-view></router-view>' },
            component: ViewTasks,
            // props: parse_params,
            // redirect: to => ({
            //   name: 'tasksBatches',
            //   params: {
            //     slug_project: to.params.slug_project,
            //   },
            // }),
            // beforeEnter: (to, from, next) => {
            //   console.warn('from.name', from.name);
            //   if (to.name !== 'tasksBatches' || from.name === 'tasks') {
            //     next({
            //       name: 'tasksBatches',
            //       params: {
            //         slug_project: to.params.slug_project,
            //       },
            //     });
            //   } else {
            //     next();
            //   }
            // },
            children: [
              {
                path: 'batches',
                name: 'tasksBatches',
                meta: {
                  name: 'Batches',
                  index: 0,
                },
                component: ViewBatches,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'batch',
                    meta: {
                      name: null,
                    },
                    component: ViewBatch,
                    props: parse_params,
                  },
                ],
              },
              {
                path: 'hits',
                name: 'tasksHITs',
                meta: {
                  name: 'HITs',
                  index: 1,
                },
                component: ViewHITs,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'hit',
                    meta: {
                      name: null,
                    },
                    component: ViewHIT,
                    props: parse_params,
                  },
                ],
              },
              {
                path: 'assignments',
                name: 'tasksAssignments',
                meta: {
                  name: 'Assignments',
                  index: 2,
                },
                component: ViewAssignments,
                props: parse_params,
                children: [
                  {
                    path: ':id',
                    name: 'assignment',
                    meta: {
                      name: null,
                    },
                    component: ViewAssignment,
                    props: parse_params,
                  },
                ],
              },
            ],
          },
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
          {
            path: 'settings',
            name: 'settings_project',
            meta: {
              name: 'Project Settings',
            },
            component: { template: '<router-view></router-view>' },
            redirect: (to) => ({
              name: 'projectSettingsGeneral',
              params: {
                slug_project: to.params.slug_project,
              },
            }),
            children: [
              {
                path: 'general',
                name: 'projectSettingsGeneral',
                meta: {
                  name: 'General Settings',
                  index: 0,
                },
                component: ViewSettingsProject,
                props: parse_params,
              },
              {
                path: 'templates',
                name: 'projectSettingsTemplates',
                meta: {
                  name: 'Template Settings',
                  index: 1,
                },
                component: ViewSettingsProject,
                props: parse_params,
              },
              {
                path: 'messages',
                name: 'projectSettingsMessages',
                meta: {
                  name: 'Message Settings',
                  index: 2,
                },
                component: ViewSettingsProject,
                props: parse_params,
              },
            ],
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
  // scrollBehavior(to) {
  //   console.warn('to.hash', to.hash);
  //   if (to.hash) {
  //     return goTo(to.hash);
  //     return {
  //       selector: to.hash,
  //       offset: { x: 0, y: 50 },
  //     };
  //   }
  //
  //   return false;
  // },
  mode: 'history',
});

queue.listen('router', (payload) => {
  router.push(payload);
});

// router.afterEach((to, from) => {
//   if (from.name === null && to.hash !== '') {
//     console.log('afterEach');
//     setTimeout(() => {
//       goTo(to.hash);
//     }, 5000)
//   }
// });

router.beforeEach((to, from, next) => {
  if (to.matched[0].name !== 'projects') {
    ServiceProjects.ping();
  }

  ServiceProjects.setSlugCurrent(to.params.slug_project);
  next();
});

// router.beforeEach((to, from, next) => {
//   if (to.name === 'tasks') {
//     next({
//       name: 'tasksBatches',
//       params: {
//         slug_project: to.params.slug_project,
//       },
//     });
//     return;
//   }
//   next();
// });

// go to add_credentials if there are no credentials stored and the target route is not already add_credentials
router.beforeEach(async (to, from, next) => {
  if (
    store.getters['module_app/has_credentials'] === false
    && to.name !== 'add_credentials'
  ) {
    const response = await AppService.init();
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
