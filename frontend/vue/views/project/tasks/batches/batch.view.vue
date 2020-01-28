<template>
  <v-row
    no-gutters
  >
    <v-col
      cols="12"
      class="mb-2"
    >
      <v-card>
        <v-breadcrumbs
          class="breadcrumbs"
          v-bind:items="breadcrumbs"
        />
      </v-card>
    </v-col>

    <v-col cols="12">
      <component-batch-detail
        v-bind:id-batch="id"
        v-on:loaded-batch="batch = $event"
      />
    </v-col>
  </v-row>
</template>

<script>
import {
  mapState, mapMutations,
} from 'vuex';

import ComponentBatchDetail from '../../../../components/batches/detail/component_batch_detail';

export default {
  name: 'AppBatch',
  components: {
    ComponentBatchDetail,
  },
  props: {
    id: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      batch: null,
    };
  },
  computed: {
    breadcrumbs() {
      return [
        {
          text: 'Tasks',
          disabled: false,
          to: { name: 'tasks', hash: '#batches' },
          exact: true,
        },
        {
          text: this.batch === null ? '' : this.batch.name,
          disabled: true,
        },
      ];
    },
    ...mapState('moduleBatches', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  methods: {
    ...mapMutations('moduleBatches', {
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>
