<template>
  <div>
    <h2 class="headline">Worker Templates</h2>
    <component-list-templates-worker></component-list-templates-worker>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentListTemplatesWorker from './component_list_templates_worker.vue';

export default {
  // mixins: [
  //     settings_batch,
  // ],
  name: 'component-templates-worker',
  data() {
    return {
      // search: undefined,
    };
  },
  methods: {},
  computed: {},
  components: {
    ComponentListTemplatesWorker,
  },
};
</script>

<style scoped></style>
