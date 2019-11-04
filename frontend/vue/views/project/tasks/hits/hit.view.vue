<template>
  <component-hit-detail
    v-bind:id-hit="id"
  />
</template>

<script>
import ComponentHitDetail from '../../../../components/hits/detail/component_hit_detail.vue';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'AppHit',
  components: {
    ComponentHitDetail,
  },
  props: {
    id: {
      required: true,
      type: Number,
    },
  },
  computed: {
    ...mapState('moduleHITs', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  methods: {
    ...mapMutations('moduleHITs', {
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>
