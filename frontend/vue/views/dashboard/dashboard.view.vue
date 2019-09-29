<template>
  <v-content>
    <v-container fluid>
      <v-row no-gutters>
        <v-col>
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
import About from '../../components/about/about';

export default {
  name: 'AppDashboard',
  components: {
    About,
    OpenProject,
    ComponentCreateProject,
  },
};
</script>
