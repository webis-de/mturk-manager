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
          <template v-if="isValidCSV">
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
          <template v-if="isValidCSV">
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
          <template v-if="isValidCSV">
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

            v-on:updated_costs_with_fee="$emit('updated_costs_with_fee', $event)"
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
import BaseDisplayAmount from '../../base-display-amount.vue';
import OverviewCosts from './overview-costs';
import {Service_Batches} from '../../../services/service_batches';

// import ComponentStepUploadCSV from './component_step_upload_csv.vue';
// import ComponentShowMoneySpent from './component-show-money-spent.vue';
// import ComponentShowBatches from './component-show-batches.vue';
export default {
  name: 'component-overview',
  props: {
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
  computed: {
    isValidCSV() {
      return Service_Batches.isValidCSV();
    },
    lifetime_formatted() {
      if (this.$store.state.moduleBatches.objectSettingsBatch === null) return null;

      return humanizeDuration(this.$store.state.moduleBatches.objectSettingsBatch.lifetime * 1000);
    },
    format_lifetime_absolute() {
      if (this.$store.state.moduleBatches.objectSettingsBatch === null) return null;

      const lifetime_absolute = this.current_time_ms + this.$store.state.moduleBatches.objectSettingsBatch.lifetime * 1000.0;
      return new Date(lifetime_absolute).toLocaleString();
    },
    count_hits() {
      if (this.isValidCSV) {
        return this.data_csv.length;
      }
      return null;
    },
    get_variables() {
      if (this.isValidCSV) {
        return Object.keys(this.data_csv[0]);
      }

      return [];
    },
    data_csv() {
      if (this.isValidCSV) {
        return this.$store.state.moduleBatches.objectCSVParsed.data;
      }
      return null;
    },
    is_valid() {
      return this.isValidCSV && !this.is_invalid_settings_batch;
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
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
