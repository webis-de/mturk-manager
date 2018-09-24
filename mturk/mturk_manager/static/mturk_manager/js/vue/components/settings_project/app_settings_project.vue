<template>
<div>
    <v-layout wrap>
      <v-flex xs6 class="pr-2">
        <component-settings-batch>
        </component-settings-batch>
      </v-flex>
      <v-flex xs6 class="pl-2">
        <component-templates-worker>
        </component-templates-worker>
      </v-flex>
	</v-layout>
</div>
</template>

<script>
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
    ComponentSettingsBatch,
  	ComponentTemplatesWorker,
  }
}
</script>

<style lang="css" scoped>
</style>