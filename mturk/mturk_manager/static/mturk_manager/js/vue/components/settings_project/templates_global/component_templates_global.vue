<template>
  <div>
    <h2 class="headline">Global Templates</h2>
    <component-list-templates-global></component-list-templates-global>
  </div>
</template>

<script>
// import settings_batch from '../../../mixins/settings_batch';
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentListTemplatesGlobal from './component_list_templates_global.vue';

export default {
  // mixins: [
  //     settings_batch,
  // ],
  name: 'component-templates-global',
  data() {
    return {
      // search: undefined,
    };
  },
  methods: {},
  computed: {},
  components: {
    ComponentListTemplatesGlobal,
  },
};
</script>

<style scoped></style>
