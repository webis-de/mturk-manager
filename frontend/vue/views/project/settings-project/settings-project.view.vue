<template>
  <v-row no-gutters>
    <v-col>
      <v-row dense>
        <v-col
          cols="12"
          class="pt-0"
        >
          <v-list
            dense
            flat
          >
            <v-list-item-group>
              <v-list-item
                v-for="anchor of arrayAnchors"
                v-bind:key="anchor.anchor"
                style="min-height: 24px"
                v-on:click.native="scrollTo(anchor.anchor)"
              >
                <v-list-item-icon class="ma-0">
                  <v-icon>mdi-chevron-down</v-icon>
                </v-list-item-icon>
                <v-list-item-content class="py-0">
                  {{ anchor.label }}
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-col>

        <v-col
          id="general"
          cols="12 display-1"
        >
          General
        </v-col>

        <v-col cols="12">
          <v-card>
            <v-container
              fluid
              class="py-0 px-2"
            >
              <v-row dense>
                <v-col xs>
                  <budget />
                </v-col>
                <v-col xs>
                  <component-block-limit />
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <table-settings-batch />
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <v-container
              fluid
              class="py-0 px-2"
            >
              <v-row dense>
                <v-col class="shrink">
                  <h2 class="headline">
                    Sandbox
                  </h2>
                  <component-clear-sandbox />
                </v-col>
                <v-col>
                  <h2 class="headline">
                    Import from MTurk
                  </h2>
                  <import-batch />
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col
          id="templates"
          cols="12 display-1"
        >
          Templates
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="12">
          <v-card>
            <table-templates-worker />
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <table-templates-assignment />
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <table-templates-hit />
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <table-templates-global />
          </v-card>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col
          id="messages"
          cols="12 display-1"
        >
          Messages
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="12">
          <v-card>
            <table-messages-reject />
          </v-card>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col
          id="global"
          cols="12 display-1"
        >
          Global
        </v-col>
      </v-row>

      <v-row dense>


        <v-col cols="12">
          <v-card>
            <v-container
              fluid
              class="py-0 px-2"
            >
              <v-row dense>
                <v-col>
                  <h2 class="headline">
                    Light Mode
                  </h2>
                  <v-switch
                    v-model="isActiveModeLight"
                    color="primary"
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-col>

        <v-col cols="12">
          <!--          <v-card>-->
          <v-dialog max-width="1500">
            <template v-slot:activator="{ on }">
              <v-btn
                color="primary"
                v-on="on"
              >
                About
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                About
              </v-card-title>
              <v-card-text>
                <about />
              </v-card-text>
            </v-card>
          </v-dialog>
          <!--          </v-card>-->
        </v-col>
      </v-row>
    </v-col>
  </v-row>
  <!----------------------------------------------------------------->
  <!----------------------------------------------------------------->
  <!----------------------------------------------------------------->
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
import ImportBatch from '../../../components/project/import-batch';
import About from '../../../components/about/about';
import ChangelogNotification from '../../../components/about/changelog-notification';
import { Service_App } from '../../../services/service.app';

export default {
  name: 'AppSettingsProject',
  components: {
    ChangelogNotification,
    About,
    ImportBatch,
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
    return {
      isActiveModeLight: this.$store.state.module_app.isActiveModeLight,
    };
  },
  computed: {
    arrayAnchors() {
      return [
        {
          label: 'General',
          anchor: '#general',
        },
        {
          label: 'Templates',
          anchor: '#templates',
        },
        {
          label: 'Messages',
          anchor: '#messages',
        },
        {
          label: 'Global',
          anchor: '#global',
        },
      ];
    },
  },
  watch: {
    isActiveModeLight() {
      Service_App.setLightMode(this.isActiveModeLight);
    },
  },
  methods: {
    scrollTo(hash) {
      this.$vuetify.goTo(hash, { offset: 8, duration: 0 });
    },
  },
};
</script>

<style lang="css" scoped></style>
