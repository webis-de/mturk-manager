<template>
  <div>
    <the-navigation-drawer
      v-bind:show_drawer.sync="show_drawer"
    />

    <v-progress-linear
      v-bind:active="get_show_progress_indicator"
      height="4"
      app
      indeterminate
      style="z-index: 50; position: absolute; margin: 0"
    />

    <v-toolbar
      app
      fixed
      clipped-left
      v-bind:style="object_styles_toolbar"
    >
      <v-toolbar-side-icon
        v-on:click.stop="show_drawer = !show_drawer"
      />
      <v-toolbar-title>
        {{ namePage }}
      </v-toolbar-title>

      <v-spacer />

      <v-layout
        align-center
        justify-end
      >
        <v-flex shrink>
          <v-tooltip bottom>
            <v-switch
              slot="activator"
              hide-details
              v-bind:label="use_sandbox ? 'Toggle Sandbox' : 'Toggle Sandbox'"
              v-bind:input-value="use_sandbox"
              v-on:click.native="toggle_use_sandbox"
            />
            <span>
              You are currently <b v-if="!use_sandbox">
                not
              </b> using the
              Sandbox
            </span>
          </v-tooltip>
        </v-flex>

        <v-divider
          class="mx-2"
          inset
          vertical
        />

        <v-flex shrink>
          <component
            v-bind:is="currentTabComponent"
            v-bind:name_route="name_route_current"
          />
        </v-flex>
      </v-layout>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import TheNavigationDrawer from '../../components/the-navigation-drawer';
import ComponentToolbarBatches from '../../components/batches/component_toolbar_batches';
import ComponentToolbarQualifications from '../../components/qualifications/component-toolbar-qualifications';
import slug_project from '../../mixins/slug_project';

export default {
  name: 'AppProject',
  components: {
    TheNavigationDrawer,
  },
  mixins: [
    slug_project,
  ],
  data() {
    return {
      show_drawer: true,
      id_interval: undefined,
    };
  },
  computed: {
    namePage() {
      return `"${this.project_current.name}" -
        ${this.$route.meta.name}`;
    },
    object_styles_toolbar() {
      if (this.use_sandbox) {
        return { 'background-color': '#dd6e00' };
      }
      return {};
    },
    currentTabComponent() {
      switch (this.$route.name) {
        case 'finances':
        case 'batches':
        case 'batch':
        case 'hits':
        case 'hit':
        case 'assignments':
        case 'assignment':
        case 'workers':
          return ComponentToolbarBatches;
        case 'qualifications':
          return ComponentToolbarQualifications;
        default:
          return null;
        // case 'workers':
        //     return ComponentToolbarWorkers;
      }
    },
    name_route_current() {
      // return this.$router.currentRoute;
      return this.$route.meta.name;
    },
    ...mapState('module_app', ['use_sandbox']),
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
      slug_project_current: 'get_slug_project_current',
      object_projects: 'get_object_projects',
    }),
    ...mapGetters(['get_show_progress_indicator']),
  },
  methods: {
    toggle_use_sandbox() {
      this.set_use_sandbox(!this.use_sandbox);
    },
    ...mapActions('module_app', ['set_use_sandbox']),
  },
};
</script>

<style lang="scss" scoped>
// sandbox switch
.v-input--selection-controls {
  padding-top: 0;
}
</style>
