<template>
  <base-table-item
    v-bind:key="worker.id"
    v-bind:item="item"
    v-bind:items-selected="itemsSelected"
    v-on:changed-selection="$emit('changed-selection', $event)"
  >
    <base-table-cell
      v-slot="{ item }"
      name="id_worker"
      class="text-left"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.id_worker }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="number_of_assignments"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.number_of_assignments }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="number_of_approved_assignments_of_project"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.number_of_approved_assignments_of_project }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="number_of_rejected_assignments_of_project"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.number_of_rejected_assignments_of_project }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="ratio_approved_assignments_of_project"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-bind:style="{color: ratioApprovedColorOfProject}">{{ item.ratio_approved_assignments_of_project.toFixed(2) }}</span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="number_of_approved_assignments"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.number_of_approved_assignments }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="number_of_rejected_assignments"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.number_of_rejected_assignments }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="ratio_approved_assignments"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-bind:style="{color: ratioApprovedColor}">{{ item.ratio_approved_assignments.toFixed(2) }}</span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="counter_assignments"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-limit-assignments
        v-bind:key="`component_limit_assignments_${item.id_worker}`"
        v-bind:worker="item"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="block_soft"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-block-soft-worker
        v-bind:key="`component_block_soft_worker_${item.id_worker}`"
        v-bind:worker="item"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="block_soft_hard"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-block-global-worker
        v-bind:key="`component_block_global_worker_${item.id_worker}`"
        v-bind:worker="item"
      />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="block_hard"
      class="text-center"
      v-bind:item="worker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-block-hard-worker
        v-bind:key="`component_block_hard_worker_${item.id_worker}`"
        v-bind:worker="item"
      />
    </base-table-cell>
  </base-table-item>
</template>
<script>
import { mapGetters } from 'vuex';

// import ComponentBlockSoftWorker from './component_block_worker.vue';
import _ from 'lodash';
import ComponentBlockSoftWorker from './component_block_soft_worker.vue';
import ComponentBlockGlobalWorker from './component_block_global_worker.vue';
import ComponentBlockHardWorker from './component_block_hard_worker.vue';
import ComponentLimitAssignments from './component_limit_assignments.vue';
import Worker from '../../../classes/workers';
import BaseTableCell from '../../base-table-cell';
import BaseTableItem from '../../base-table-item';

export default {
  name: 'ComponentItemWorker',
  props: {
    item: {
      type: Worker,
      required: true,
    },
    itemsSelected: {
      type: Object,
      required: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      show_snackbar: false,
      worker: this.item,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    ratioApprovedColorOfProject() {
      return `hsl(${this.interpolate(0, 120, this.worker.ratio_approved_assignments_of_project, 1)}, 100%, 50%)`;
    },
    ratioApprovedColor() {
      return `hsl(${this.interpolate(0, 120, this.worker.ratio_approved_assignments, 1)}, 100%, 50%)`;
    },
    // worker() {
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
      if (_.isEqual(this.worker, this.item)) return;

      this.worker = this.item;
    },
  },
  methods: {
    interpolate(startValue, endValue, stepNumber, lastStepNumber) {
      return (endValue - startValue) * stepNumber / lastStepNumber + startValue;
    },
  },
  components: {
    BaseTableItem,
    BaseTableCell,
    ComponentBlockSoftWorker,
    ComponentBlockGlobalWorker,
    ComponentBlockHardWorker,
    ComponentLimitAssignments,
  },
};
</script>

<style lang="scss" scoped></style>
