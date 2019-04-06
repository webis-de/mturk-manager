<template>
  <component-assignment-detail
    v-bind:id_assignment="id"
  />
</template>

<script>
import ComponentAssignmentDetail from '../../../components/assignments/detail/component_assignment_detail.vue';
import slug_project from '../../../mixins/slug_project';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'AppAssignments',
  components: {
    ComponentAssignmentDetail,
  },
  mixins: [slug_project],
  props: {
    id: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
    };
  },
  computed: {
    ...mapState('moduleAssignments', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  methods: {
    ...mapMutations('moduleAssignments', {
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>
