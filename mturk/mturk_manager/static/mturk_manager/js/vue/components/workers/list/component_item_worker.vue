<template>
  <!-- <div>wda</div> -->
  <tr>
    <td v-bind:style="stylesCell">
      <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
    </td>
    <td
      v-if="set_columns_selected.has('name')"
      class="text-xs-left"
      v-bind:style="stylesCell"
    >
      {{ props.item.id_worker }}
    </td>
    <!--<td>-->
    <!--</td>-->
    <!--<td>-->
    <!--</td>-->
    <td
      v-if="set_columns_selected.has('counter_assignments')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-limit-assignments
        v-bind:key="`component_limit_assignments_${props.item.name}`"
        v-bind:worker="worker"
      ></component-limit-assignments>
    </td>
    <td
      v-if="set_columns_selected.has('block_soft')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-block-soft-worker
        v-bind:key="`component_block_soft_worker_${worker.name}`"
        v-bind:worker="worker"
      ></component-block-soft-worker>
    </td>
    <td
      v-if="set_columns_selected.has('block_soft_hard')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-block-global-worker
        v-bind:key="`component_block_global_worker_${worker.name}`"
        v-bind:worker="worker"
      ></component-block-global-worker>
    </td>
    <td
      v-if="set_columns_selected.has('block_hard')"
      class="text-xs-center"
      v-bind:style="stylesCell"
    >
      <component-block-hard-worker
        v-bind:key="`component_block_hard_worker_${worker.name}`"
        v-bind:worker="worker"
      ></component-block-hard-worker>
    </td>
  </tr>
</template>
<script>
import { mapGetters } from 'vuex';

// import ComponentBlockSoftWorker from './component_block_worker.vue';
import ComponentBlockSoftWorker from './component_block_soft_worker.vue';
import ComponentBlockGlobalWorker from './component_block_global_worker.vue';
import ComponentBlockHardWorker from './component_block_hard_worker.vue';
import ComponentLimitAssignments from './component_limit_assignments.vue';

export default {
  name: 'component-item-worker',
  props: {
    props: {
      type: Object,
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
      show_snackbar: false,
      worker: this.props.item,
    };
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    set_columns_selected() {
      return new Set(this.array_columns_selected);
    },
    // worker() {
    //   return this.props.item;
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
  methods: {},
  components: {
    ComponentBlockSoftWorker,
    ComponentBlockGlobalWorker,
    ComponentBlockHardWorker,
    ComponentLimitAssignments,
  },
};
</script>

<style lang="scss" scoped></style>
