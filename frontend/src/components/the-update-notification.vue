<template>
  <v-snackbar
    top
    v-bind:value="hasUpdate === true"
    v-bind:timeout="-1"
    color="error"
  >
    <v-spacer />
    Update Available!
    <base-help>
      Update your frontend by using the image <code>kritten/mturk-manager-frontend:{{ version_api }}</code>
    </base-help>
    <v-spacer />
  </v-snackbar>
</template>

<script>
import { mapState } from 'vuex';
import BaseHelp from './base-help';
import { compareVersions } from '../helpers';

export default {
  name: 'TheUpdateNotification',
  components: { BaseHelp },
  computed: {
    hasUpdate() {
      if (this.version_api === null) {
        return false;
      }

      return compareVersions(this.version, this.version_api) === -1;
    },
    ...mapState('module_app', ['version_api', 'version']),
  },
};
</script>

<style scoped></style>
