<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        text
        v-bind:loading="is_syncing_mturk"
        v-bind:color="$vuetify.theme.isDark === true && useSandbox === false ? 'primary' : 'primary darken-3'"
        v-on:click="sync_mturk(true)"
        v-on="on"
      >
        <v-icon>mdi-sync</v-icon>
        <template v-if="$vuetify.breakpoint.lgAndUp">
          Sync with MTurk
        </template>
      </v-btn>
    </template>

    <span>Refresh batch data</span>
  </v-tooltip>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { ServiceBatches } from '../../services/batches.service';

export default {
  name: 'SyncWithMturk',
  data() {
    return {};
  },
  computed: {
    useSandbox() {
      return this.$store.state.module_app.use_sandbox;
    },
    ...mapGetters(['get_show_progress_indicator']),
    ...mapGetters('moduleBatches', {
      is_syncing_mturk: 'get_is_syncing_mturk',
    }),
  },
  methods: {
    sync_mturk() {
      ServiceBatches.syncMturk();
    },
    ...mapActions(['set_show_progress_indicator']),
    ...mapActions('moduleBatches', {
      sync_database: 'sync_database',
    }),
  },
};
</script>
