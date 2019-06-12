<template>
  <v-layout>
    <v-flex>
      <v-tabs
        v-bind:value="$route.meta.type"
        v-on:change="changedView($event)"
      >
        <v-tab key="general">
          General
        </v-tab>
        <v-tab key="templates">
          Templates
        </v-tab>
        <v-tab key="messages">
          Messages
        </v-tab>

        <v-tabs-items class="mt-1">
          <v-tab-item
            key="general"
          >
            <v-container
              fluid
              grid-list-md
              class="pa-0"
            >
              <v-layout wrap>
                <v-flex xs>
                  <v-card class="pa-2">
                    <budget />
                  </v-card>
                </v-flex>
                <v-flex xs>
                  <v-card class="pa-2">
                    <component-block-limit />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex
                  xs
                >
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Batch Profiles
                    </h2>
                    <table-settings-batch />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex shrink>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Sandbox
                    </h2>
                    <component-clear-sandbox />
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-tab-item>

          <v-tab-item
            key="templates"
          >
            <v-container
              fluid
              grid-list-md
              class="pa-0"
            >
              <v-layout wrap>
                <v-flex xs>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Worker Templates
                    </h2>
                    <table-templates-worker />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Assignment Templates
                    </h2>
                    <table-templates-assignment />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      HIT Templates
                    </h2>
                    <table-templates-hit />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Global Templates
                    </h2>
                    <table-templates-global />
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-tab-item>

          <v-tab-item
            key="messages"
          >
            <v-container
              fluid
              grid-list-md
              class="pa-0"
            >
              <v-layout wrap>
                <v-flex xs>
                  <v-card class="pa-2">
                    <h2 class="headline">
                      Reject Messages
                    </h2>
                    <table-messages-reject />
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout wrap />
            </v-container>
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-flex>
  </v-layout>
<!--  <div>-->
<!--    <v-layout wrap>-->
<!--      <v-flex xs class="pa-1">-->
<!--        <budget></budget>-->
<!--      </v-flex>-->
<!--      <v-flex xs class="pa-1">-->
<!--        <component-block-limit> </component-block-limit>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex xs class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          Batch Profiles-->
<!--        </h2>-->
<!--        <table-settings-batch></table-settings-batch>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex xs class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          Worker Templates-->
<!--        </h2>-->
<!--        <table-templates-worker></table-templates-worker>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          Assignment Templates-->
<!--        </h2>-->
<!--        <table-templates-assignment> </table-templates-assignment>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          HIT Templates-->
<!--        </h2>-->
<!--        <table-templates-hit></table-templates-hit>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          Global Templates-->
<!--        </h2>-->
<!--        <table-templates-global></table-templates-global>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout wrap>-->
<!--      <v-flex class="pa-1">-->
<!--        <h2 class="headline">-->
<!--          Reject Messages-->
<!--        </h2>-->
<!--        <table-messages-reject/>-->
<!--      </v-flex>-->
<!--    </v-layout>-->

<!--    <v-layout>-->
<!--      <v-flex shrink class="pa-1">-->
<!--        <component-clear-sandbox> </component-clear-sandbox>-->
<!--      </v-flex>-->
<!--      &lt;!&ndash;<v-flex shrink class="pa-1">&ndash;&gt;-->
<!--      &lt;!&ndash;<component-delete-project>&ndash;&gt;-->
<!--      &lt;!&ndash;</component-delete-project>&ndash;&gt;-->
<!--      &lt;!&ndash;</v-flex>&ndash;&gt;-->
<!--    </v-layout>-->
<!--  </div>-->
</template>

<script>
import ComponentBlockLimit from '../../../components/settings_project/block_limit/component_block_limit';
import ComponentClearSandbox from '../../../components/settings_project/clear_sandbox/component_clear_sandbox';
import Budget from '../../../components/finances/budget';
import TableTemplatesWorker from '../../../components/settings_project/templates_worker/table-templates-worker';
import TableTemplatesAssignment from '../../../components/settings_project/templates_assignment/table-templates-assignment';
import TableTemplatesHit from '../../../components/settings_project/templates_hit/table-template-hit';
import TableTemplatesGlobal from '../../../components/settings_project/templates_global/table-template-global';
import TableSettingsBatch from '../../../components/settings_project/settings_batch/table-settings-batch';
import TableMessagesReject from '../../../components/messages-reject/table-messages-reject';

export default {
  name: 'AppSettingsProject',
  components: {
    TableMessagesReject,
    TableSettingsBatch,
    TableTemplatesGlobal,
    TableTemplatesHit,
    TableTemplatesAssignment,
    TableTemplatesWorker,
    Budget,
    ComponentBlockLimit,
    ComponentClearSandbox,
  },
  data() {
    return {};
  },
  methods: {
    changedView(index) {
      switch (index) {
        case 0:
          this.$router.push({
            name: 'projectSettingsGeneral',
          });
          break;
        case 1:
          this.$router.push({
            name: 'projectSettingsTemplates',
          });
          break;
        case 2:
          this.$router.push({
            name: 'projectSettingsMessages',
          });
          break;
        default:
          break;
      }
    },
  },
};
</script>

<style lang="css" scoped></style>
