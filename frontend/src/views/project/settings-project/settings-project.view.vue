<template>
  <base-page>
    <base-page-group-divider
      v-bind:identifier="{
        identifier: 'general',
        label: 'General'
      }"
    >
      General
    </base-page-group-divider>

    <base-page-group>
      <base-page-section v-bind:title="'Budget'">
        <v-row dense>
          <v-col xs>
            <budget />
          </v-col>
        </v-row>
      </base-page-section>
      <base-page-section v-bind:title="'Limit Block'">
        <v-row dense>
          <v-col xs>
            <component-block-limit />
          </v-col>
        </v-row>
      </base-page-section>
    </base-page-group>
    <base-page-section type="table">
      <table-settings-batch />
    </base-page-section>

    <base-page-group>
      <base-page-section
        v-bind:title="'Sandbox'"
        shrink
      >
        <v-row dense>
          <v-col>
            <component-clear-sandbox />
          </v-col>
        </v-row>
      </base-page-section>
      <base-page-section
        v-bind:title="'Import'"
        shrink
      >
        <v-row dense>
          <v-col>
            <import-batch />
          </v-col>
        </v-row>
      </base-page-section>
    </base-page-group>

    <base-page-group-divider
      v-bind:identifier="{
        identifier: 'templates',
        label: 'Templates'
      }"
    >
      Templates
    </base-page-group-divider>

    <base-page-section type="table">
      <table-templates-worker />
    </base-page-section>
    <base-page-section type="table">
      <table-templates-requester />
    </base-page-section>

    <base-page-group-divider
      v-bind:identifier="{
        identifier: 'messages',
        label: 'Messages'
      }"
    >
      Messages
    </base-page-group-divider>

    <base-page-section type="table">
      <table-messages-reject />
    </base-page-section>

    <base-page-group-divider
      v-bind:identifier="{
        identifier: 'global',
        label: 'Global'
      }"
    >
      Global
    </base-page-group-divider>
    <base-page-group>
      <base-page-section
        v-bind:title="'Light Mode'"
        shrink
      >
        <v-row dense>
          <v-col>
            <v-switch
              v-model="isActiveModeLight"
              color="primary"
              hide-details
              class="mt-0"
            />
          </v-col>
        </v-row>
      </base-page-section>
      <base-page-section
        v-bind:title="'Autosave'"
        shrink
      >
        <v-row dense>
          <v-col>
            <v-switch
              v-model="isActiveAutosave"
              color="primary"
              hide-details
              class="mt-0"
            />
          </v-col>
        </v-row>
      </base-page-section>
      <base-page-section
        v-bind:title="'Database'"
        shrink
      >
        <v-row dense>
          <v-col>
            <v-dialog
              width="500"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  color="primary"
                  v-on="on"
                >
                  Update Credentials
                </v-btn>
              </template>

              <v-card>
                <v-card-title>
                  Update Credentials
                </v-card-title>
                <v-card-text>
                  <the-update-credentials
                    class="text-center"
                  />
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </base-page-section>
    </base-page-group>

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
  </base-page>
</template>

<script lang="ts">
import TableSettingsBatch from '@/modules/settingsBatch/components/table/table-settings-batch';
import ComponentBlockLimit from '../../../components/settings_project/block_limit/component_block_limit';
import ComponentClearSandbox from '../../../components/settings_project/clear_sandbox/component_clear_sandbox';
import Budget from '../../../components/finances/budget';
import TableMessagesReject from '../../../components/messages-reject/table-messages-reject';
import ImportBatch from '../../../components/project/import-batch';
import About from '../../../components/about/about';
import ChangelogNotification from '../../../components/about/changelog-notification';
import { AppService } from '../../../services/app.service';
import BasePage from '../../../components/base/base-page';
import BasePageSection from '../../../components/base/base-page-section';
import BasePageGroupDivider from '../../../components/base/base-page-group-divider';
import BasePageGroup from '../../../components/base/base-page-group';
import TheUpdateCredentials from '../../../components/the-update-credentials';
import TableTemplatesRequester from '../../../modules/template/components/table/table-templates-requester';
import TableTemplatesWorker from '../../../modules/template/components/table/table-templates-worker';

export default {
  name: 'AppSettingsProject',
  components: {
    TableTemplatesWorker,
    TableTemplatesRequester,
    TheUpdateCredentials,
    BasePageGroup,
    BasePageGroupDivider,
    BasePageSection,
    BasePage,
    ChangelogNotification,
    About,
    ImportBatch,
    TableMessagesReject,
    TableSettingsBatch,
    Budget,
    ComponentBlockLimit,
    ComponentClearSandbox,
  },
  data() {
    return {
      isActiveModeLight: this.$store.state.module_app.isActiveModeLight,
      isActiveAutosave: this.$store.state.module_app.isActiveAutosave,
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
      AppService.setLightMode(this.isActiveModeLight);
    },
    isActiveAutosave() {
      AppService.setAutosave(this.isActiveAutosave);
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
