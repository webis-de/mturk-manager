<template>
  <div>
    <h2 class="headline">Assignment Templates</h2>
    <component-list-templates-assignment></component-list-templates-assignment>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentListTemplatesAssignment from './component_list_templates_assignment.vue';

export default {
  // mixins: [
  //     settings_batch,
  // ],
  name: 'component-templates-assignment',
  data() {
    return {
      // search: undefined,
    };
  },
  methods: {},
  computed: {},
  components: {
    ComponentListTemplatesAssignment,
  },
};
</script>

<style scoped></style>
