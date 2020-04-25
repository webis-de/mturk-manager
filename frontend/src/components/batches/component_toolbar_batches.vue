<template>
  <v-row no-gutters>
    <!--<v-flex shrink>-->
    <!--<v-tooltip bottom>-->
    <!--<v-btn-->
    <!--text-->
    <!--v-bind:loading="get_show_progress_indicator"-->
    <!--v-on:click="refresh_data(true)"-->
    <!--slot="activator"-->
    <!--&gt;-->
    <!--<v-icon>refresh</v-icon>-->
    <!--Refresh Data-->
    <!--</v-btn>-->
    <!--<span>Refresh batch data</span>-->
    <!--</v-tooltip>-->
    <!--</v-flex>-->
    <v-col shrink>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            text
            v-bind:loading="is_syncing_mturk"
            v-on:click="sync_mturk(true)"
            v-on="on"
          >
            <v-icon>mdi-sync</v-icon>
            Sync with MTurk
          </v-btn>
        </template>
        <span>Refresh batch data</span>
      </v-tooltip>
    </v-col>
  </v-row>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { ServiceBatches } from '../../services/batches.service';

export default {
  name: 'ComponentToolbarBatches',
  props: {
    nameRoute: {},
  },
  data() {
    return {};
  },
  created() {
    // console.log($route);
  },
  computed: {
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
