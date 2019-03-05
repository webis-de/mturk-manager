<template>
  <div>
    <!-- v-bind:action="`/view/${this.project_current.slug}`" -->
    <form v-on:submit.prevent="submit">
      <input type="hidden" name="list_ids[]" value="1" />
      <input type="hidden" name="list_ids[]" value="3" />
      <v-btn
        type="submit"
        color="primary"
        small
        v-bind:disabled="count_assignments_selected === 0"
      >
        Annotate {{ count_assignments_selected }} assignment(s)
      </v-btn>
    </form>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';

export default {
  name: 'component_annotate',
  data() {
    return {};
  },
  methods: {
    submit() {
      window.open(this.url, '_blank');
    },
  },
  computed: {
    count_assignments_selected() {
      return _.size(this.object_assignments_selected);
    },
    url() {
      let url = `/view/${this.project_current.slug}?list_ids=[`;
      url += _.join(_.map(this.object_assignments_selected), ',');
      // url += _.join(_.map(this.object_assignments_selected, (assignment) => assignment.id), ',');
      return `${url}]`;
    },
    ...mapGetters('moduleAssignments', {
      object_assignments_selected: 'get_object_assignments_selected',
    }),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  components: {},
};
</script>

<style scoped></style>
