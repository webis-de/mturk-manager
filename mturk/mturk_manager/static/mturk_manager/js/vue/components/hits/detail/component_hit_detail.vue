<template>
  <!-- <div>wda</div> -->

  <v-layout wrap>
    <v-flex>
      <!-- {{object_batches}} -->
      <h2 class="headline">
        HIT {{ hit.id_hit }}
        <v-btn
          slot="activator"
          class="my-0"
          icon
          small
          v-bind:to="{ name: 'hits' }"
        >
          <v-icon>arrow_upward</v-icon>
        </v-btn>
      </h2>
      <v-divider class="my-3"></v-divider>
      <list-assignments v-bind:id_hit="id_hit"></list-assignments>
    </v-flex>
  </v-layout>
</template>
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ListAssignments from '../../assignments/list/list-assignments';

export default {
  name: 'component-hit-detail',
  // props: {
  //  id_hit: {
  //      required: true,
  //  },
  // },
  props: {
    id_hit: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {};
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    list_assignments() {
      if (this.hit.object_assignments == undefined) {
        return [];
      }
      return _.orderBy(this.hit.object_assignments);
    },
    hit() {
      const object_hits = this.get_object_hits();
      if (object_hits == null) {
        return {};
      }
      if (object_hits[this.id_hit] == undefined) {
        return {};
      }
      return object_hits[this.id_hit];
    },
    ...mapGetters('moduleAssignments', {
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    ...mapGetters('moduleHITs', {
      get_object_hits: 'get_object_hits',
    }),
    ...mapGetters(['get_show_progress_indicator']),
  },
  methods: {
    ...mapActions('moduleAssignments', {
      function_reset_array_columns: 'reset_array_columns_general',
    }),
    ...mapMutations('moduleAssignments', {
      function_set_array_columns: 'set_array_columns_general',
    }),
  },
  components: {
    ListAssignments,
  },
};
</script>

<style lang="scss" scoped>
td {
  height: unset !important;
}
td .v-input--selection-controls {
  padding: unset;
}
</style>
