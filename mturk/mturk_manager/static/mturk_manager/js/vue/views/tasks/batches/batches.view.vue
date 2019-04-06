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
import slug_project from '../../../mixins/slug_project';

export default {
  name: 'AppBatches',
  components: {
    ComponentBatchDetail,
  },
  mixins: [
    slug_project,
    // load_data,
  ],
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
