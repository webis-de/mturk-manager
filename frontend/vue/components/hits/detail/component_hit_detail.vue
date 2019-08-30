<template>
  <v-layout wrap>
    <v-flex>
      <h2 class="headline">
        <v-btn
          slot="activator"
          class="my-0"
          icon
          small
          v-bind:to="{ name: 'tasksHITs' }"
        >
          <v-icon>arrow_back</v-icon>
        </v-btn>
        HIT {{ hit.idHit }}
      </h2>
      <v-divider class="my-3"></v-divider>
      <list-assignments
        v-bind:function-set-pagination="functionSetPagination"
        v-bind:pagination-computed="paginationComputed"

        v-bind:filters="{
          id_hit: idHit
        }"
      ></list-assignments>
    </v-flex>
  </v-layout>
</template>
<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ListAssignments from '../../assignments/list/list-assignments';
import {Service_HITs} from '../../../services/service_hits';

export default {
  name: 'ComponentHitDetail',
  components: {
    ListAssignments,
  },
  // props: {
  //  id_hit: {
  //      required: true,
  //  },
  // },
  props: {
    idHit: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      hitIntern: null,
    };
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
      return this.hitIntern === null ? {} : this.hitIntern;
    },
    ...mapGetters('moduleAssignments', {
      array_columns_selected: 'get_array_columns_selected_general',
    }),
    ...mapGetters('moduleHITs', {
      get_object_hits: 'get_object_hits',
    }),
    ...mapGetters(['get_show_progress_indicator']),
    ...mapState('moduleAssignments', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  created() {
    Service_HITs.loadHIT(this.idHit).then((hit) => {
      this.hitIntern = hit;
    });
  },
  methods: {
    ...mapActions('moduleAssignments', {
      function_reset_array_columns: 'reset_array_columns_general',
    }),
    ...mapMutations('moduleAssignments', {
      function_set_array_columns: 'set_array_columns_general',
      functionSetPagination: 'setPaginationGeneral',
    }),
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
