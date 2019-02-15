<template>
  <div>
    <h2 class="headline">Batch Profiles</h2>
    <component-list-settings-batch></component-list-settings-batch>
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentListSettingsBatch from './component_list_settings_batch.vue';

export default {
  name: 'component-settings-batch',
  data() {
    return {
      // search: undefined,
    };
  },
  methods: {},
  computed: {},
  components: {
    ComponentListSettingsBatch,
  },
};
</script>

<style scoped></style>
