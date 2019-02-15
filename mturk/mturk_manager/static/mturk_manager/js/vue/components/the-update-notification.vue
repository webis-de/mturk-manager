<template>
  <v-snackbar
    top
    v-bind:value="version_api > version_app"
    v-bind:timeout="0"
    color="info"
    auto-height
  >
    <v-spacer></v-spacer>
    Update Available!
    <help-icon
      >Pull the latest changes of the git repository to update the
      application.</help-icon
    >
    <v-spacer></v-spacer>
  </v-snackbar>
</template>

<script>
import { mapState } from 'vuex';
import HelpIcon from './help-icon';

export default {
  name: 'the-update-notification',
  components: { HelpIcon },
  data() {
    return {};
  },
  computed: {
    ...mapState('module_app', ['version_api', 'version_app']),
  },
};
</script>

<style scoped></style>
