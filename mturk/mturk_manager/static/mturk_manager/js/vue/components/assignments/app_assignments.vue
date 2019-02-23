<template>
  <span>
    <template v-if="$route.name == 'assignments'">

      <h1 class="headline">Assignments</h1>

      <v-switch label="Only Submitted" v-model="show_only_submitted_assignments"></v-switch>

      <list-assignments
        v-bind:filters="{
          show_only_submitted_assignments,
        }"
      ></list-assignments>

      <component-annotate></component-annotate>
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
      show_only_submitted_assignments: false,
    };
  },
};
</script>
