<template>
  <component-batch-detail
    v-bind:id_batch="id"
  />
</template>

<script>
import {
  mapState, mapMutations,
} from 'vuex';

import ComponentBatchDetail from '../../../components/batches/detail/component_batch_detail.vue';

export default {
  name: 'AppBatches',
  components: {
    ComponentBatchDetail,
  },
  props: {
    id: {
      required: true,
      type: Number,
    },
  },
  computed: {
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
