<template>
  <component-hit-detail
    v-bind:id_hit="id"
  />
</template>

<script>
import ComponentHitDetail from '../../../components/hits/detail/component_hit_detail.vue';
import slug_project from '../../../mixins/slug_project';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'AppHits',
  components: {
    ComponentHitDetail,
  },
  mixins: [slug_project],
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
