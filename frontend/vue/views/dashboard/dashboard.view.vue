<template>
  <v-content>
    <v-container fluid>
      <v-row no-gutters>
        <v-col>
          <v-menu
            v-model="dialog"
            v-bind:close-on-content-click="false"
            offset-y
          >
            <template v-slot:activator="{ on }">
              <v-btn
                absolute
                top
                right
                icon
                v-on="on"
              >
                <v-icon>mdi-settings</v-icon>
              </v-btn>
            </template>

            <the-settings-app v-on:updated-credentials="dialog = false" />
          </v-menu>

          <v-row no-gutters>
            <v-col>
              <component-create-project />
            </v-col>
          </v-row>

          <v-divider class="my-3" />

          <v-row no-gutters>
            <v-col>
              <open-project />
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="my-3" />

      <v-row
        no-gutters
        justify="end"
      >
        <v-col
          class="shrink"
        >
          <v-btn
            small
            color="secondary"
            v-bind:to="{ name: 'about' }"
          >
            About
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
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
