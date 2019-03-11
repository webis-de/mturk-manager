<template>
  <div>
    <v-layout wrap>
      <v-flex xs class="pa-1">
        <budget></budget>
      </v-flex>
      <v-flex xs class="pa-1">
        <component-block-limit> </component-block-limit>
      </v-flex>
      <v-flex xs class="pa-1">
        <component-messages-reject-default> </component-messages-reject-default>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex xs class="pa-1">
        <h2 class="headline">
          Batch Profiles
        </h2>
        <table-settings-batch></table-settings-batch>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex xs class="pa-1">
        <h2 class="headline">
          Worker Templates
        </h2>
        <table-templates-worker></table-templates-worker>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <h2 class="headline">
          Assignment Templates
        </h2>
        <table-templates-assignment> </table-templates-assignment>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <h2 class="headline">
          HIT Templates
        </h2>
        <table-templates-hit></table-templates-hit>
      </v-flex>
    </v-layout>

    <v-layout wrap>
      <v-flex class="pa-1">
        <h2 class="headline">
          Global Templates
        </h2>
        <table-templates-global></table-templates-global>
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
import ComponentClearSandbox from './clear_sandbox/component_clear_sandbox.vue';
import slug_project from '../../mixins/slug_project';
import Budget from '../finances/budget';
import TableTemplatesWorker from './templates_worker/table-templates-worker';
import TableTemplatesAssignment from './templates_assignment/table-templates-assignment';
import TableTemplatesHit from './templates_hit/table-template-hit';
import TableTemplatesGlobal from './templates_global/table-template-global';
import TableSettingsBatch from './settings_batch/table-settings-batch';

export default {
  mixins: [slug_project],
  name: 'app_settings_project',

  data() {
    return {};
  },
  components: {
    TableSettingsBatch,
    TableTemplatesGlobal,
    TableTemplatesHit,
    TableTemplatesAssignment,
    TableTemplatesWorker,
    Budget,
    ComponentBlockLimit,
    ComponentMessagesRejectDefault,
    ComponentClearSandbox,
  },
};
</script>

<style lang="css" scoped></style>
