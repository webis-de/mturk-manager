<template>
  <span>
    <!-- v-bind:return-value.sync="worker.count_assignments_limit" -->
    <v-dialog
      v-model="dialog"
      max-width="500px"
      v-if="project_current.count_assignments_max_per_worker !== null"
    >
      <span
        slot="activator"
        v-bind:class="{ 'warning--text': has_reached_limit_assignments }"
      >
        {{ content }}
      </span>

      <v-card>
        <v-card-title>
          Assignment Limit for Worker {{ worker.id_worker }}
        </v-card-title>
        <v-card-text>
          <v-layout row align-center>
            <v-flex>
              <v-text-field
                type="number"
                v-model="limit"
                label="Assignment Limit"
                min="0"
                autofocus
              ></v-text-field>
            </v-flex>
            <v-flex>
              <v-btn
                color="primary"
                v-on:click="set(limit)"
                v-bind:disabled="!has_changed"
                >Set to {{ limit }}</v-btn
              >
            </v-flex>
            <v-flex>
              <v-btn color="primary" v-on:click="set(0)">Reset</v-btn>
            </v-flex>
            <v-flex>
              <v-btn color="primary" v-on:click="set(-1)">Unlock</v-btn>
            </v-flex>
          </v-layout>
          <!-- append-icon="clear"
	            v-on:click:append="limit = 0" -->
        </v-card-text>
        <!-- <v-card-actions>
            	<v-btn
            		color="primary"
            		flat
            		v-on:click="dialog=false"
        		>Close</v-btn>
          	</v-card-actions> -->
      </v-card>
    </v-dialog>

    <template v-else>
      No limit
    </template>

    <v-snackbar
      v-model="show_snackbar"
      v-bind:timeout="1000"
      color="info"
      bottom
    >
      Updated
      <v-btn flat v-on:click="show_snackbar = false">
        Close
      </v-btn>
    </v-snackbar>
  </span>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { Service_Workers } from '../../../services/service_worker';

export default {
  name: 'component-limit-assignments',
  props: {
    worker: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      limit: this.worker.count_assignments_limit,
      show_snackbar: false,
      dialog: false,
    };
  },
  watch: {
    dialog(was_opened) {
      if (!was_opened) {
        this.limit = this.worker.count_assignments_limit;
      }
    },
    'worker.count_assignments_limit': function () {
      console.log('aawd');
      this.limit = this.worker.count_assignments_limit;
    },
  },
  computed: {
    has_changed() {
      return this.limit != this.worker.count_assignments_limit;
    },
    content() {
      if (this.worker.count_assignments_limit == -1) {
        return 'Unlimited';
      }
      return `${this.worker.count_assignments_limit} of ${
        this.project_current.count_assignments_max_per_worker
      } ${this.has_reached_limit_assignments ? '(blocked)' : ''}`;
    },
    has_reached_limit_assignments() {
      return (
        this.worker.count_assignments_limit
        >= this.project_current.count_assignments_max_per_worker
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  methods: {
    set(value) {
      this.set_show_progress_indicator(true);

      Service_Workers.update_count_assignments_limit({
        worker: this.worker,
        value,
      }).then(() => {
        this.show_snackbar = true;
        (this.dialog = false), this.set_show_progress_indicator(false);
      });
    },
    ...mapActions(['set_show_progress_indicator']),
  },
};
</script>

<style lang="css">
.v-menu__activator {
	justify-content: center;
}
</style>
