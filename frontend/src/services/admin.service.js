import { store } from '../store/vuex';
import { BaseLoadPageService } from './baseLoadPage.service';

class ClassAdminService {
  async loadInfoSize() {
    return Promise.all([
      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_batches',
            'moduleBatches',
          ),
          use_sandbox: false,
        },
      }),
      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_batches',
            'moduleBatches',
          ),
          use_sandbox: true,
        },
      }),

      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_hits',
            'moduleHITs',
          ),
          use_sandbox: false,
        },
      }),
      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_hits',
            'moduleHITs',
          ),
          use_sandbox: true,
        },
      }),

      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_assignments',
            'moduleAssignments',
          ),
          use_sandbox: false,
        },
      }),
      BaseLoadPageService.loadPage({
        pagination: {
          rowsPerPage: 1,
        },
        url: {
          path: store.getters.get_url(
            'url_api_assignments',
            'moduleAssignments',
          ),
          use_sandbox: true,
        },
      }),
    ]);
  }
}

export const ServiceAdmin = new ClassAdminService();
