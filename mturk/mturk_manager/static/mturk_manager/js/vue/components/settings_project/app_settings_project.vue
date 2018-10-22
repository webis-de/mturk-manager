<template>
<div>
    <v-layout wrap>
      <v-flex xs6 class="pa-1">
        <component-block-limit>
        </component-block-limit>
      </v-flex>
  </v-layout>
    <v-layout wrap>
      <v-flex xs6 class="pa-1">
        <component-settings-batch>
        </component-settings-batch>
      </v-flex>
      <v-flex xs6 class="pa-1">
        <component-templates-worker>
        </component-templates-worker>
      </v-flex>
  </v-layout>
</div>
</template>

<script>
    import ComponentBlockLimit from './block_limit/component_block_limit.vue';
    import ComponentSettingsBatch from './settings_batch/component_settings_batch.vue';
    import ComponentTemplatesWorker from './templates_worker/component_templates_worker.vue';
    import slug_project from '../../mixins/slug_project';

export default {
    mixins: [
        slug_project,
    ],
  name: 'app_settings_project',

  data () {
    return {

    }
  },
  components: {
    ComponentBlockLimit,
    ComponentSettingsBatch,
  	ComponentTemplatesWorker,
  }
}
</script>

<style lang="css" scoped>
</style>