<template>
  <v-content>
    <v-container fluid>
      <v-layout wrap>
        <v-flex>
          <v-layout wrap>
            <v-flex>
              <component-create-project />
            </v-flex>
          </v-layout>

          <v-divider class="my-3" />

          <v-layout wrap>
            <v-flex>
              <open-project />
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>

      <v-divider class="my-3" />

      <v-layout column>
        <v-flex
          shrink
          align-self-end
        >
          <v-btn
            small
            color="secondary"
            v-bind:to="{ name: 'about' }"
          >
            About
          </v-btn>
        </v-flex>
      </v-layout>
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
