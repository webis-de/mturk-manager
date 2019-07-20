<template>
  <v-tooltip bottom>
    <v-btn
      icon
      v-bind:loading="show_progress_indicator"
      v-on:click="refresh_data"
      slot="activator"
    >
      <v-icon>refresh</v-icon>
    </v-btn>
    <span>Refresh qualifications</span>
  </v-tooltip>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'component-toolbar-qualifications',
  props: {
    show_progress_indicator: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {};
  },
  methods: {
    refresh_data() {
      this.set_show_progress_indicator(true);

      this.sync_policies(true).then(() => {
        this.set_show_progress_indicator(false);
      });
    },
    ...mapActions(['set_show_progress_indicator']),
    ...mapActions('modulePolicies', {
      sync_policies: 'sync_policies',
    }),
  },
};
</script>
