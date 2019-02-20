<template>
  <div>
    <h2 class="headline">
      Batch Profiles
    </h2>
    <component-list-settings-batch />
  </div>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import _ from 'lodash';
import ComponentListSettingsBatch from './table-settings-batch.vue';

export default {
  name: 'ComponentSettingsBatch',
  components: {
    ComponentListSettingsBatch,
  },
  data() {
    return {
      // search: undefined,
    };
  },
  computed: {},
  methods: {},
};
</script>

<style scoped></style>
