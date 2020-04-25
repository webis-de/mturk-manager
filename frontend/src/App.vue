<template>
  <v-app>
    <router-view />
    <!--<template v-if="url_api === null || token_instance === null">-->
    <!--<v-spacer></v-spacer>-->
    <!--<add-credentials></add-credentials>-->
    <!--<v-spacer></v-spacer>-->
    <!--</template>-->
    <!--<template v-else>-->
    <!--<router-view v-if="has_loaded_projects">-->
    <!--</router-view>-->

    <!--<template v-else>-->
    <!--<v-spacer></v-spacer>-->
    <!--<div class="text-xs-center">-->
    <!--<v-progress-circular-->
    <!--indeterminate-->
    <!--color="primary"-->
    <!--&gt;</v-progress-circular>-->
    <!--</div>-->
    <!--<v-spacer></v-spacer>-->
    <!--</template>-->
    <!--</template>-->
    <the-update-notification />
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { ServiceProjects } from './services/service_projects';
import TheUpdateNotification from './components/the-update-notification';
import { ServiceTemplates } from './services/service_templates';

export default {
  name: 'App',
  components: {
    TheUpdateNotification,
  },
  data() {
    return {
    };
  },
  computed: {
    ...mapGetters('moduleProjects', {
      slug_project_current: 'get_slug_project_current',
    }),
  },
  watch: {
    async slug_project_current() {
      await ServiceProjects.load_project_data();

      if (this.slug_project_current !== undefined) {
        await ServiceTemplates.getAll({
          typeTemplate: 'workerAll',
        });
      }
    },
  },
  methods: {
    ...mapActions(['init']),
  },
};
</script>
