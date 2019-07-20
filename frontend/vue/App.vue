<template>
  <v-app dark>
    <router-view/>
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
import { Service_Projects } from './services/service_projects';
import TheUpdateNotification from './components/the-update-notification';

export default {
  name: 'App',
  components: {
    TheUpdateNotification,
  },
  data() {
    return {
    };
  },
  watch: {
    slug_project_current() {
      Service_Projects.load_project_data();
    },
  },
  computed: {
    ...mapGetters('moduleProjects', {
      slug_project_current: 'get_slug_project_current',
    }),
  },
  methods: {
    ...mapActions(['init']),
  },
};
</script>
