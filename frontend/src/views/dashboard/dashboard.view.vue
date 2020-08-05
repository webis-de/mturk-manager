<template>
  <div>
    <v-app-bar
      app
      fixed
      clipped-left
      dense
      v-bind:style="{
        'background-color': $store.state.module_app.use_sandbox === true ? '#dd6e00' : null
      }"
    >
      <v-toolbar-title>
        MTurk Manager
      </v-toolbar-title>

      <v-row
        align="center"
        justify="end"
        no-gutters
      >
        <v-col class="shrink">
          <v-menu
            v-bind:close-on-content-click="false"
            offset-y
          >
            <template v-slot:activator="{ on }">
              <v-btn
                text
                v-on="on"
              >
                Settings
              </v-btn>
            </template>

            <the-settings-app v-on:updated-credentials="dialog = false" />
          </v-menu>
        </v-col>
      </v-row>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <v-row no-gutters>
          <v-col>
            <v-row no-gutters>
              <v-col>
                <component-create-project />
              </v-col>
            </v-row>

            <!--            <v-divider class="my-3" />-->

            <v-row
              no-gutters
              class="mt-6"
            >
              <v-col>
                <open-project />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import ComponentCreateProject from '../../components/dashboard/component_create_project';
import OpenProject from '../../components/dashboard/openProject';
import TheSettingsApp from '../../components/the-settings-app';

export default {
  name: 'AppDashboard',
  components: {
    TheSettingsApp,
    OpenProject,
    ComponentCreateProject,
  },
  data() {
    return {
      dialog: false,
    };
  },
};
</script>
