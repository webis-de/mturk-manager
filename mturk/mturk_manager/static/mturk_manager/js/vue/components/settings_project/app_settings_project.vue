<template>
  <div>
    <v-layout wrap>
      <v-flex xs6 class="pa-1">
        <component-settings-batch> </component-settings-batch>
      </v-flex>
      <v-flex xs6 class="pa-1">
        <component-block-limit> </component-block-limit>
        <component-messages-reject-default> </component-messages-reject-default>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex xs class="pa-1">
        <component-templates-worker> </component-templates-worker>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <component-templates-assignment> </component-templates-assignment>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <component-templates-hit> </component-templates-hit>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <component-templates-global> </component-templates-global>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex shrink class="pa-1">
        <component-clear-sandbox> </component-clear-sandbox>
      </v-flex>
      <!--<v-flex shrink class="pa-1">-->
      <!--<component-delete-project>-->
      <!--</component-delete-project>-->
      <!--</v-flex>-->
    </v-layout>
  </div>
</template>

<script>
import ComponentBlockLimit from './block_limit/component_block_limit.vue';
import ComponentMessagesRejectDefault from './messages_reject/component_messages_reject_default.vue';
import ComponentSettingsBatch from './settings_batch/component_settings_batch.vue';
import ComponentTemplatesWorker from './templates_worker/component_templates_worker.vue';
import ComponentTemplatesAssignment from './templates_assignment/component_templates_assignment.vue';
import ComponentTemplatesGlobal from './templates_global/component_templates_global.vue';
import ComponentTemplatesHit from './templates_hit/component_templates_hit.vue';
import ComponentClearSandbox from './clear_sandbox/component_clear_sandbox.vue';
import ComponentDeleteProject from './delete_project/component_delete_project.vue';
import slug_project from '../../mixins/slug_project';

export default {
  mixins: [slug_project],
  name: 'app_settings_project',

  data() {
    return {};
  },
  components: {
    ComponentBlockLimit,
    ComponentMessagesRejectDefault,
    ComponentSettingsBatch,
    ComponentTemplatesWorker,
    ComponentTemplatesAssignment,
    ComponentTemplatesGlobal,
    ComponentTemplatesHit,
    ComponentClearSandbox,
    ComponentDeleteProject,
  },
};
</script>

<style lang="css" scoped></style>
