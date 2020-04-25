<template>
  <component-assignment-detail
    v-bind:id_assignment="id"
  />
</template>

<script>
import ComponentAssignmentDetail from '../../../../components/assignments/detail/component_assignment_detail.vue';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'AppAssignment',
  components: {
    ComponentAssignmentDetail,
  },
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
