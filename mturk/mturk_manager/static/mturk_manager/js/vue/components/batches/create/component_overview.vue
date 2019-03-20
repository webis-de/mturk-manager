<template>
  <v-layout
    class="pa-3"
    wrap
  >
    <v-flex>
      <h1 class="headline">Overview</h1>
      <v-layout
        class="my-3"
      >
        <v-flex xs3>
          Valid CSV:
        </v-flex>
        <v-flex>
          <template v-if="is_valid_csv">
            <v-icon color="success">check</v-icon>
          </template>
          <template v-else>
            None
          </template>
        </v-flex>
      </v-layout>

      <v-layout
        class="my-3"
      >
        <v-flex xs3>
          Number of variables:
        </v-flex>
        <v-flex>
          <template v-if="is_valid_csv">
            {{ get_variables.length }}

            <v-tooltip top>
              <v-icon slot="activator">info</v-icon>
              <span>{{ get_variables.join(", ") }}</span>
            </v-tooltip>
          </template>
          <template v-else>
            None
          </template>
        </v-flex>
      </v-layout>

      <v-layout
        class="my-3"
      >
        <v-flex xs3>
          Number of HITs:
        </v-flex>
        <v-flex>
          <template v-if="is_valid_csv">
            {{ count_hits }}
          </template>
          <template v-else>
            None
          </template>
        </v-flex>
      </v-layout>

      <v-layout
        class="my-3"
      >
        <v-flex xs3>
          Available until:
        </v-flex>
        <v-flex>
          <template v-if="is_valid">
            {{ format_lifetime_absolute }} ({{ lifetime_formatted }})
          </template>
          <template v-else>
            None
          </template>
        </v-flex>
      </v-layout>

      <v-layout
        class="my-2"
      >
        <v-flex xs3>
          Costs:
        </v-flex>
        <v-flex>
          <overview-costs
            v-if="is_valid"

            style="margin-left: -13px"
            v-bind:settings-batch="settings_batch_current"
          />
          <template
            v-else
          >
            None
          </template>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>
<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import humanizeDuration from 'humanize-duration';
import Settings_Batch from '../../../classes/settings_batch';
import BaseDisplayAmount from '../../base-display-amount.vue';
import OverviewCosts from './overview-costs';

// import ComponentStepUploadCSV from './component_step_upload_csv.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'component-overview',
  props: {
    settings_batch_current: {
      required: true,
      type: Settings_Batch | undefined,
    },
    is_invalid_settings_batch: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {
      current_time_ms: Date.now(),
    };
  },
  methods: {},
  computed: {
    lifetime_formatted() {
      if (this.settings_batch_current == undefined) return undefined;

      return humanizeDuration(this.settings_batch_current.lifetime * 1000);
    },
    format_lifetime_absolute() {
      if (this.settings_batch_current == undefined) return undefined;

      const lifetime_absolute = this.current_time_ms + this.settings_batch_current.lifetime * 1000.0;
      return new Date(lifetime_absolute).toLocaleString();
    },
    count_hits() {
      if (this.is_valid_csv) {
        return this.data_csv.length;
      }
      return null;
    },
    get_variables() {
      if (this.is_valid_csv) {
        return Object.keys(this.data_csv[0]);
      }

      return [];
    },
    data_csv() {
      if (this.is_valid_csv) {
        return this.object_csv_parsed.data;
      }
      return null;
    },
    is_valid() {
      return this.is_valid_csv && !this.is_invalid_settings_batch;
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapGetters('moduleBatches', {
      object_csv_parsed: 'get_object_csv_parsed',
      is_valid_csv: 'is_valid_csv',
    }),
  },
  created() {
    setInterval(() => {
      this.current_time_ms = Date.now();
    }, 1000);
  },
  components: {
    OverviewCosts,
    BaseDisplayAmount,
  },
};
</script>

<style scoped></style>
