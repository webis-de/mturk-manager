<template>
  <v-tooltip top>
    <template v-slot:activator="{ on }">
      <v-icon
        v-if="hasUnseenVersions"
        small
        color="warning"
        v-on="on"
      >
        warning
      </v-icon>
    </template>

    <span>
      Check the changelog for new features and fixes
    </span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'ChangelogNotification',
  computed: {
    hasUnseenVersions() {
      return this.$store.state.module_app.version !== this.$store.state.module_app.versionSeen;
    },
  },
};
</script>
