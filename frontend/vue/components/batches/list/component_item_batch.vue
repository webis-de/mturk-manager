<template>
  <base-table-item
    v-bind:key="batch.id"
    v-bind:item="item"
    v-bind:items-selected="itemsSelected"
    v-on:changed-selection="$emit('changed-selection', $event)"
  >
    <base-table-cell
    v-bind:key="batch.id + 'checklbox'"
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
      v-bind:to="{
        name: 'batch',
        params: {
          id: item.id
        }
      }"
    >
      {{ item.name.toLowerCase() }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="datetime_creation"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-datetime
        v-bind:datetime="item.datetime_creation"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_hits"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.count_hits }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="settings_batch__count_assignments"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.settings_batch.count_assignments }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_total"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.countAssignmentsTotal }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_approved"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.countAssignmentsApproved }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="count_assignments_rejected"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.countAssignmentsRejected }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="settings_batch__reward"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-amount
        v-bind:amount="item.settings_batch.reward"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="costs_max"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-amount
        v-bind:amount="item.costs_max"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="costs_so_far"
      class="text-right"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-amount
        v-bind:amount="item.costs_so_far"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="progress"
      class="text-center pr-4"
      v-bind:item="batch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-progress-bar
        v-bind:title-popover="`Assignments (${item.countAssignmentsTotal})`"
        v-bind:datasets="datasets"
      />
    </base-table-cell>

    <!--    <base-table-cell-->
    <!--      v-slot="{ item }"-->
    <!--      name="actions"-->
    <!--      class="text-center"-->
    <!--      v-bind:item="batch"-->
    <!--      v-bind:columns-selected="objectColumnsSelected"-->
    <!--    >-->
    <!--      <v-btn-->
    <!--        slot="activator"-->
    <!--        class="my-0"-->
    <!--        icon-->
    <!--        small-->
    <!--        v-bind:to="{-->
    <!--          name: 'batch',-->
    <!--          params: {-->
    <!--            id: item.id-->
    <!--          }-->
    <!--        }"-->
    <!--      >-->
    <!--        <v-icon>mdi-information</v-icon>-->
    <!--      </v-btn>-->
    <!--    </base-table-cell>-->
  </base-table-item>
<!--  <tr-->

<!--    class="text-no-wrap"-->
<!--    v-bind:class="classes"-->
<!--  >-->
<!--    <td>-->
<!--      <base-table-checkbox-->
<!--        v-model="isSelected"-->
<!--      />-->
<!--    </td>-->


<!--  </tr>-->
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
import BaseTableCheckbox from '../../base-table-checkbox';
import BaseTableItem from '../../base-table-item';

export default {
  name: 'ComponentItemBatch',
  components: {
    BaseTableItem,
    BaseTableCheckbox,
    BaseTableCell,
    BaseDisplayDatetime,
    BaseProgressBar,
    BaseDisplayAmount,
  },
  props: {
    item: {
      required: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
    itemsSelected: {
      type: Object,
      required: true,
    },
    classes: {
      required: false,
      type: Object | Array,
      default() {
        return {};
      },
    },
  },
  data() {
    return {
      batch: this.item,
    };
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
    // batch() {
    //   return this.props.item;
    // },
    // classesCell() {
    //   return {
    //
    //   },
    // },
    ...mapGetters(['get_show_progress_indicator']),
    ...mapGetters('moduleBatches', {
      object_batches_selected: 'get_object_batches_selected',
    }),
  },
  watch: {
    item() {
      // TODO: some other technique to prevent unnecessary updates?
      if (_.isEqual(this.batch, this.item)) return;

      this.batch = this.item;
    },
  },
  methods: {
    ...mapMutations('moduleBatches', {
      set_batches_selected: 'set_batches_selected',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
