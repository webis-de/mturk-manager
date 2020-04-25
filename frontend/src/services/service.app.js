import { store } from '../store/vuex';
import { Service_Endpoint } from './service_endpoint';
import { ServiceProjects } from './service_projects';
import queue from '../queue';
import { compareVersions } from '../helpers';
import { vuetify } from '../vuetify';
import { ServiceTemplates } from './service_templates';

class ClassServiceApp {
  async init(force = false) {
    const isSuccess = await store.dispatch('module_app/load_credentials');

    if (isSuccess === false) {
      return {
        reason: 'load_credentials',
      };
    }

    Service_Endpoint.init(force);

    const response = await ClassServiceApp.loadConfig();

    if (response.success) {
      await ServiceProjects.load_projects();
      await ServiceProjects.load_project_data();
      if (store.state.moduleProjects.slug_project_current !== undefined) {
        await ServiceTemplates.getAll({
          typeTemplate: 'workerAll',
        });
      }
    }

    return response;
  }

  static async loadConfig() {
    const response = await Service_Endpoint.make_request({
      url: {
        path: 'config',
      },
      method: 'get',
    });

    if (response.success === true) {
      await store.dispatch('module_app/init', response.data);
      console.warn('frontend version', store.state.module_app.version);
      console.warn('config', response.data);
    }


    return response;
  }

  async resetChangelog() {
    await store.dispatch('module_app/setState', {
      objectState: [],
      nameState: 'changelog',
      nameLocalStorage: 'changelog',
    });
  }

  async loadChangelog() {
    const response = await Service_Endpoint.make_request({
      url: {
        host: 'https://api.github.com',
        path: 'repos/webis-de/mturk-manager/releases',
      },
      method: 'get',
      options: {
        headers: {
          Authorization: null,
        },
      },
    });

    if (response.success === true) {
      const { changelog } = store.state.module_app;
      let changelogNew = response.data;

      changelogNew = changelogNew.filter((release) => release.prerelease === false);

      // get the latest version stored in the browser
      let versionStoredLatest;
      if (changelog.length > 0) {
        versionStoredLatest = changelog[0].tag;
      }

      // get only new releases from the response
      if (versionStoredLatest !== undefined) {
        changelogNew = changelogNew.filter((release) => compareVersions(release.tag_name, versionStoredLatest) === 1);
      }

      changelogNew = changelogNew.map((release) => ({
        id: release.id,
        name: release.name,
        tag: release.tag_name,
        created: release.published_at,
        body: null,
      }));

      await store.dispatch('module_app/setState', {
        objectState: changelogNew.concat(changelog),
        nameState: 'changelog',
        nameLocalStorage: 'changelog',
      });
    }
  }

  async loadRelease(idTag) {
    const response = await Service_Endpoint.make_request({
      url: {
        host: 'https://api.github.com',
        path: 'repos/webis-de/mturk-manager/releases',
        value: idTag,
      },
      method: 'get',
      options: {
        headers: {
          Authorization: null,
        },
      },
    });

    if (response.success === true) {
      await store.dispatch('module_app/setReleaseBody', {
        idTag,
        body: response.data.body,
      });
    }
  }

  async updateCredentials({ url, token }) {
    url = url.trim();

    if (!url.startsWith('http')) {
      url = `http://${url}`;
    }

    if (url.endsWith('/')) {
      url = url.slice(0, -1);
    }

    await store.dispatch('module_app/setState', {
      objectState: url,
      nameState: 'url_api',
      nameLocalStorage: 'url_api',
    });

    await store.dispatch('module_app/setState', {
      objectState: token,
      nameState: 'token_instance',
      nameLocalStorage: 'token_instance',
    });

    const response = await this.init(true);

    if (response.success === true) {
      // send the user to the dashboard if no error occured
      queue.notify('router', { name: 'dashboard' });
    }
  }

  async setLightMode(isActiveModeLight) {
    await store.dispatch('module_app/setState', {
      objectState: isActiveModeLight,
      nameState: 'isActiveModeLight',
      nameLocalStorage: 'isActiveModeLight',
    });

    vuetify.framework.theme.dark = !isActiveModeLight;
  }
}

export const Service_App = new ClassServiceApp();
