<template>
  <v-snackbar
    top
    v-bind:value="version_api !== version && version_api !== null"
    v-bind:timeout="0"
    color="error"
    auto-height
  >
    <v-spacer></v-spacer>
    Update Available!
    <base-help>
      Pull the latest changes of the git repository to update the
      application.
    </base-help
    >
    <v-spacer></v-spacer>
  </v-snackbar>
</template>

<script>
import { mapState } from 'vuex';
import BaseHelp from './base-help';

export default {
  name: 'the-update-notification',
  components: {BaseHelp},
  data() {
    return {};
  },
  computed: {
    ...mapState('module_app', ['version_api', 'version']),
  },
};
</script>

<style scoped></style>
