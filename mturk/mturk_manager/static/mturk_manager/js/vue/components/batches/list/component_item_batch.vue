<template>
  <!-- <div>wda</div> -->
  <tr
    v-bind:key="batch.id"
    class="text-no-wrap"
  >
    <td v-bind:style="stylesCell">
      <v-checkbox v-model="is_selected" primary hide-details></v-checkbox>
    </td>

    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-xs-left"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_hits"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.count_hits }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_creation"
      class="text-xs-center"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-display-datetime
        v-bind:datetime="item.datetime_creation"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="settings_batch__count_assignments"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.settings_batch.count_assignments }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="settings_batch__reward"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-display-amount
        v-bind:amount="item.settings_batch.reward"
      ></base-display-amount>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_total"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.countAssignmentsTotal }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_approved"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.countAssignmentsApproved }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_rejected"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      {{ item.countAssignmentsRejected }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="costs_max"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-display-amount
        v-bind:amount="item.costs_max"
      ></base-display-amount>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="costs_so_far"
      class="text-xs-right"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-display-amount
        v-bind:amount="item.costs_so_far"
      ></base-display-amount>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="progress"
      class="text-xs-center"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <base-progress-bar
        v-bind:title-popover="`Assignments (${item.countAssignmentsTotal})`"
        v-bind:datasets="datasets"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-xs-center"
      v-bind:item="batch"
      v-bind:columns-selected="columnsSelected"
      v-bind:is-condensed="isCondensed"
    >
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:to="{
          name: 'batch',
          params: {
            id: item.id
          }
        }"
      >
        <v-icon>info</v-icon>
      </v-btn>
    </base-table-cell>
  </tr>
</template>
<script>
import {
  mapState, mapActions, mapMutations, mapGetters,
} from 'vuex';
import _ from 'lodash';
import BaseDisplayAmount from '../../base-display-amount';
import BaseProgressBar from '../../base-progress-bar';
import BaseDisplayDatetime from '../../common/base-display-datetime';
import BaseTableCell from '../../base-table-cell';

export default {
  name: 'ComponentItemBatch',
  props: {
    props: {
      required: true,
    },
    array_columns_selected: {
      type: Array,
      required: true,
    },

    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {
      batch: this.props.item,
    };
  },
  watch: {
    columnsSelected() {
      return this.columnsSelected;
    },
  },
  computed: {
    datasets() {
      return [
        {
          label: 'Approved',
          backgroundColor: '#81C784',
          data: [this.batch.countAssignmentsApproved],
        },
        {
          label: 'Rejected',
          backgroundColor: '#E57373',
          data: [this.batch.countAssignmentsRejected],
        },
        {
          label: 'Submitted',
          backgroundColor: '#FFB74D',
          data: [this.batch.countAssignmentsSubmitted],
        },
        {
          label: 'Expired',
          backgroundColor: '#90A4AE',
          data: [this.batch.countAssignmentsDead],
        },
        {
          label: 'Pending',
          backgroundColor: '#64B5F6',
          data: [this.batch.countAssignmentsPending],
        },
      ];
    },
    is_selected: {
      get() {
        return _.has(this.object_batches_selected, this.batch.id);
      },
      set(is_selected) {
        this.set_batches_selected({
          array_items: [this.batch],
          add: is_selected,
        });
      },
    },
    columnsSelected() {
      return this.array_columns_selected.reduce((accumulator, column) => {
        accumulator[column] = column;
        return accumulator;
      }, {});
    },
    set_columns_selected() {
      return new Set(this.array_columns_selected);
    },
    // batch() {
    //   return this.props.item;
    // },
    // classesCell() {
    //   return {
    //
    //   },
    // },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: 'unset !important',
          paddingLeft: '5px !important',
          paddingRight: '5px !important',
        };
      }
      return {};
    },
    ...mapGetters(['get_show_progress_indicator']),
    ...mapGetters('moduleBatches', {
      object_batches_selected: 'get_object_batches_selected',
    }),
  },
  methods: {
    ...mapMutations('moduleBatches', {
      set_batches_selected: 'set_batches_selected',
    }),
  },
  mounted() {},
  components: {
    BaseTableCell,
    BaseDisplayDatetime,
    BaseProgressBar,
    BaseDisplayAmount,
  },
};
</script>

<style lang="scss" scoped></style>
