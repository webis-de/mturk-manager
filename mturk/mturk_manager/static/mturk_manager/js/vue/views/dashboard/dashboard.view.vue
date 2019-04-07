<template>
  <v-content>
    <v-container fluid>
      <v-layout wrap>
        <v-flex>
          <v-layout wrap>
            <v-flex>
              <component-create-project> </component-create-project>
            </v-flex>
          </v-layout>
          <v-divider class="my-3"></v-divider>
          <v-layout wrap>
            <v-flex>
              <open-project></open-project>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import ComponentCreateProject from '../../components/dashboard/component_create_project';
import OpenProject from '../../components/dashboard/openProject';

export default {
  name: 'AppDashboard',
  components: {
    OpenProject,
    ComponentCreateProject,
  },
};
</script>
