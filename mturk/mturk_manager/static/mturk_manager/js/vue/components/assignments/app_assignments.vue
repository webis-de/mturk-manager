<template>
  <span>
    <template v-if="$route.name == 'assignments'">

      <h1 class="headline">Assignments</h1>

      <list-assignments
        v-bind:function-set-pagination="functionSetPagination"
        v-bind:pagination-computed="paginationComputed"
      >
        <template v-slot:actions>
          <component-annotate></component-annotate>
        </template>
      </list-assignments>

    </template>
    <template v-else-if="$route.name == 'assignment'">
      <component-assignment-detail
        v-bind:id_assignment="id_assignment"
      ></component-assignment-detail>
    </template>
  </span>
</template>

<script>
import ComponentAssignmentDetail from './detail/component_assignment_detail.vue';
import ComponentAnnotate from './annotate/component_annotate.vue';
import slug_project from '../../mixins/slug_project';
import ListAssignments from './list/list-assignments';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'AppAssignments',
  components: {
    ListAssignments,
    ComponentAssignmentDetail,
    ComponentAnnotate,
  },
  mixins: [slug_project],
  props: {
    id_assignment: {},
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
