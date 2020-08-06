import { store } from '../store/vuex';
import { ServiceEndpoint } from './endpoint.service';
import { ServiceProjects } from './projects.service';
import queue from '../queue';
import { compareVersions } from '../helpers';
import { vuetify } from '../vuetify';

class ClassServiceApp {
  async init(force = false) {
    const isSuccess = await store.dispatch('module_app/load_credentials');

    if (isSuccess === false) {
      return {
        reason: 'load_credentials',
      };
    }

    ServiceEndpoint.init(force);

    const response = await ClassServiceApp.loadConfig();

    if (response.success) {
      await ServiceProjects.loadProjects();
      await ServiceProjects.loadProjectData();
    }

    return response;
  }

  static async loadConfig() {
    const response = await ServiceEndpoint.makeRequest({
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
    const response = await ServiceEndpoint.makeRequest({
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
    const response = await ServiceEndpoint.makeRequest({
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
    let urlProcessed = url.trim();

    if (!urlProcessed.startsWith('http')) {
      urlProcessed = `http://${urlProcessed}`;
    }

    if (urlProcessed.endsWith('/')) {
      urlProcessed = urlProcessed.slice(0, -1);
    }

    await store.dispatch('module_app/setState', {
      objectState: urlProcessed,
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
      // TODO: check, seems not to work
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

  async setAutosave(isActiveAutosave) {
    await store.dispatch('module_app/setState', {
      objectState: isActiveAutosave,
      nameState: 'isActiveAutosave',
      nameLocalStorage: 'isActiveAutosave',
    });
  }
}

export const AppService = new ClassServiceApp();
