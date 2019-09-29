<template>
  <v-snackbar
    top
    v-bind:value="hasUpdate === true"
    v-bind:timeout="0"
    color="error"
  >
    <v-spacer />
    Update Available!
    <base-help>
      Pull the latest changes of the git repository to update the
      application.
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
