<template>
  <span>
    <v-tooltip left>
      <v-btn icon slot="activator" class="ma-0 warning--text text--lighten-1">
        <v-icon>block</v-icon>
      </v-btn>
      <span>Soft Blocked</span>
    </v-tooltip>
    <v-tooltip left>
      <v-btn icon slot="activator" class="ma-0 error--text text--lighten-4">
        <v-icon>block</v-icon>
      </v-btn>
      <span>Hard Blocked</span>
    </v-tooltip>
  </span>
  <!-- <v-layout align-center>
    <v-flex mr-3>
        Block:
    </v-flex>
    <v-flex>
        <v-radio-group
            v-bind:disabled="!is_enabled"
            v-bind:value="status_block_current"
            v-on:input="status_block_new = $event"
            row>
            <v-radio
                v-for="(n, i) in labels_ticks"
                v-bind:key="`${worker.name}_${n}`"
                v-bind:name="worker.name"
                v-bind:label="n"
                v-bind:value="values[i]"
                class="mb-0"
            ></v-radio>
        </v-radio-group>
    </v-flex>
</v-layout> -->
</template>
<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import { STATUS_BLOCK } from '../../../classes/enums.js';

export default {
  name: 'component-block-worker',
  props: {
    worker: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      labels_ticks: ['None', 'Soft', 'Hard'],
      values: [STATUS_BLOCK.NONE, STATUS_BLOCK.SOFT, STATUS_BLOCK.HARD],
      is_updating: false,
      status_block_current: undefined,
      status_block_new: undefined,
    };
  },
  watch: {
    'worker.is_blocked': function (value) {
      this.status_block_current = value;
    },
    status_block_new(value_new) {
      this.set_show_progress_indicator(true);
      this.is_updating = true;

      this.status_block_current = value_new;

      this.update_status_block({
        worker: this.worker,
        status_block_new: value_new,
        status_block_old: this.worker.is_blocked,
      }).then(() => {
        this.is_updating = false;
        this.set_show_progress_indicator(false);
      });
    },
  },
  computed: {
    is_enabled() {
      return !this.is_updating && this.worker.is_blocked != undefined;
    },
  },
  methods: {
    ...mapActions('moduleWorkers', {
      update_status_block: 'update_status_block',
    }),
    ...mapActions(['set_show_progress_indicator']),
  },
  created() {},
  components: {},
};
</script>
