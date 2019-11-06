<template>
  <tr
    v-bind:key="hit.id"
    class="text-no-wrap roboto-mono"
  >
    <td>
      <v-checkbox
        v-model="is_selected"
        class="pa-0 ma-0"
        primary
        hide-details
      />
    </td>

    <base-table-cell
      v-slot="{ item }"
      name="id_hit"
      class="text-left"
      v-bind:item="hit"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:to="{
        name: 'hit',
        params: {
          id: hit.id
        }
      }"
    >
      {{ item.id_hit }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="batch"
      class="text-right"
      v-bind:item="hit"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:to="{
        name: 'batch',
        params: {
          id: hit.batch.id
        }
      }"
    >
      {{ hit.batch.name.toUpperCase() }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_creation"
      class="text-right"
      v-bind:item="hit"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-datetime
        v-bind:datetime="hit.datetime_creation"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="progress"
      class="text-right"
      v-bind:item="hit"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-progress-bar
        v-bind:title-popover="`Assignments (${hit.countAssignmentsTotal})`"
        v-bind:datasets="datasets"
      />
    </base-table-cell>

<!--    <base-table-cell-->
<!--      v-slot="{ item }"-->
<!--      name="actions"-->
<!--      class="text-center"-->
<!--      v-bind:item="hit"-->
<!--      v-bind:columns-selected="objectColumnsSelected"-->
<!--    >-->
<!--      <v-btn-->
<!--        slot="activator"-->
<!--        class="my-0"-->
<!--        icon-->
<!--        small-->
<!--        v-bind:to="{-->
<!--          name: 'hit',-->
<!--          params: {-->
<!--            slug_project: $route.params.slug_project,-->
<!--            id: hit.id-->
<!--          }-->
<!--        }"-->
<!--      >-->
<!--        <v-icon>mdi-information</v-icon>-->
<!--      </v-btn>-->
<!--    </base-table-cell>-->
  </tr>
</template>
<script>
import {
  mapState, mapActions, mapMutations, mapGetters,
} from 'vuex';
import _ from 'lodash';
import BaseProgressBar from '../../base-progress-bar';
import BaseDisplayDatetime from '../../common/base-display-datetime';
import BaseTableCell from '../../base-table-cell';

export default {
  name: 'ComponentItemHit',
  components: {
    BaseTableCell,
    BaseDisplayDatetime,
    BaseProgressBar,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    show_links: {
      required: false,
      type: Boolean,
      default: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      hit: this.item,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    datasets() {
      return [
        {
          label: 'Approved',
          backgroundColor: '#81C784',
          data: [this.hit.countAssignmentsApproved],
        },
        {
          label: 'Rejected',
          backgroundColor: '#E57373',
          data: [this.hit.countAssignmentsRejected],
        },
        {
          label: 'Submitted',
          backgroundColor: '#FFB74D',
          data: [this.hit.countAssignmentsSubmitted],
        },
        {
          label: 'Expired',
          backgroundColor: '#90A4AE',
          data: [this.hit.countAssignmentsDead],
        },
        {
          label: 'Pending',
          backgroundColor: '#64B5F6',
          data: [this.hit.countAssignmentsPending],
        },
      ];
    },
    is_selected: {
      get() {
        return _.has(this.object_hits_selected, this.hit.id);
      },
      set(is_selected) {
        this.set_hits_selected({
          array_items: [this.hit],
          add: is_selected,
        });
      },
    },
    ...mapGetters('moduleHITs', {
      object_hits_selected: 'get_object_hits_selected',
    }),
    // count_assignments_total() {
    //     return this.hit.batch.settings_batch.count_assignments;
    // },
    count_assignments() {
      return _.size(this.hit.assignments);
    },
    // progress() {
    //     console.log('EXECUTED')
    //     return (this.count_assignments_available / this.count_assignments_total) * 100.0;
    // },
    // hit() {
    //   return this.props.item;
    // },

    // status_block() {
    //     if(this.worker.is_blocked == undefined)
    //     {
    //         return {
    //             description: 'Loading',
    //             color: 'success',
    //             icon: '',
    //         };
    //     }

    //     switch(this.worker.is_blocked)
    //     {
    //         case STATUS_BLOCK.NONE:
    //             return {
    //                 description: 'Not Blocked',
    //                 color: 'success',
    //                 icon: 'check',
    //             };
    //         case STATUS_BLOCK.SOFT:
    //             return {
    //                 description: 'Soft Blocked',
    //                 color: 'warning',
    //                 icon: 'block',
    //             };
    //         case STATUS_BLOCK.HARD:
    //             return {
    //                 description: 'Hard Blocked',
    //                 color: 'error',
    //                 icon: 'block',
    //             };
    //     }
    // },
    ...mapGetters(['get_show_progress_indicator']),
  },
  watch: {
    item() {
      // TODO: some other technique to prevent unnecessary updates?
      if (_.isEqual(this.hit, this.item)) return;

      this.hit = this.item;
    },
  },
  methods: {
    ...mapMutations('moduleHITs', {
      set_hits_selected: 'set_hits_selected',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
