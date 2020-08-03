<template>
  <div>
    <!--    <the-navigation-drawer-->
    <!--      v-bind:show-drawer.sync="show_drawer"-->
    <!--    />-->

    <v-progress-linear
      v-bind:active="get_show_progress_indicator"
      height="4"
      app
      indeterminate
      style="z-index: 50; position: absolute; margin: 0"
    />

    <v-app-bar
      app
      fixed
      clipped-left
      dense
      v-bind:style="object_styles_toolbar"
    >
      <!--      <v-app-bar-nav-icon-->
      <!--        v-on:click.stop="show_drawer = !show_drawer"-->
      <!--      />-->
      <v-toolbar-title>
        <v-row
          no-gutters
        >
          <v-col>
            <v-btn
              text
              class="text-none pa-0"
              style="text-indent: 0; font-size: inherit; letter-spacing: normal; font-weight: 400"
              v-bind:to="{ name: 'dashboard' }"
              exact
            >
              <template v-if="$vuetify.breakpoint.lgAndUp">
                MTurk Manager
              </template>
              <template v-else>
                <v-icon>mdi-home</v-icon>
              </template>
            </v-btn>
          </v-col>

          <v-col class="px-2">
            <v-divider vertical />
          </v-col>

          <v-col align-self="center">
            {{ $store.getters['moduleProjects/getProjectCurrent'].name }}
          </v-col>
        </v-row>
        <!--        <the-breadcrumb />-->
      </v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <create-batch>
          <template v-slot:default="{ on }">
            <v-btn
              text
              v-bind:color="$vuetify.theme.isDark === true && use_sandbox === false ? 'primary' : 'primary darken-3'"
              v-on="on"
            >
              <v-icon>mdi-plus</v-icon>
              <template v-if="$vuetify.breakpoint.lgAndUp">
                Create Batch
              </template>
            </v-btn>
          </template>
        </create-batch>

        <sync-with-mturk />

        <v-col class="px-2">
          <v-divider vertical />
        </v-col>

        <v-col class="shrink text-no-wrap">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-switch
                hide-details
                v-bind:label="use_sandbox ? 'Sandbox' : 'Sandbox'"
                v-bind:input-value="use_sandbox"
                color="primary darken-3"
                v-on:click.native="toggle_use_sandbox"
                v-on="on"
              />
            </template>
            <span>
              You are currently <b v-if="!use_sandbox">
                not
              </b> using the
              Sandbox
            </span>
          </v-tooltip>
        </v-col>

        <v-col class="px-2">
          <v-divider vertical />
        </v-col>

        <v-btn
          text
          v-bind:to="{name:'tasks'}"
        >
          Tasks
        </v-btn>
        <v-btn
          text
          v-bind:to="{name:'finances'}"
        >
          Finances
        </v-btn>
        <v-btn
          text
          v-bind:to="{name:'workers'}"
        >
          Workers
        </v-btn>
        <v-btn
          text
          v-bind:to="{name:'settings_project'}"
        >
          Settings
        </v-btn>
      </v-toolbar-items>

      <!--      <v-row-->
      <!--        align="center"-->
      <!--        justify="end"-->
      <!--        no-gutters-->
      <!--      >-->
      <!--        <v-col class="shrink text-no-wrap">-->
      <!--          <v-tooltip bottom>-->
      <!--            <template v-slot:activator="{ on }">-->
      <!--              <v-switch-->
      <!--                hide-details-->
      <!--                v-bind:label="use_sandbox ? 'Toggle Sandbox' : 'Toggle Sandbox'"-->
      <!--                v-bind:input-value="use_sandbox"-->
      <!--                v-on:click.native="toggle_use_sandbox"-->
      <!--                v-on="on"-->
      <!--              />-->
      <!--            </template>-->
      <!--            <span>-->
      <!--              You are currently <b v-if="!use_sandbox">-->
      <!--                not-->
      <!--              </b> using the-->
      <!--              Sandbox-->
      <!--            </span>-->
      <!--          </v-tooltip>-->
      <!--        </v-col>-->

      <!--        <v-divider-->
      <!--          class="mx-2"-->
      <!--          vertical-->
      <!--        />-->

      <!--        <v-col class="shrink">-->
      <!--          <component-->
      <!--            v-bind:is="currentTabComponent"-->
      <!--            v-bind:name_route="name_route_current"-->
      <!--          />-->
      <!--        </v-col>-->

      <!--        <v-divider-->
      <!--          class="mx-2"-->
      <!--          vertical-->
      <!--        />-->
      <!--        <v-menu-->
      <!--          v-bind:close-on-content-click="false"-->
      <!--          offset-y-->
      <!--        >-->
      <!--          <template v-slot:activator="{ on }">-->
      <!--            <v-btn-->
      <!--              icon-->
      <!--              v-on="on"-->
      <!--            >-->
      <!--              <v-icon>mdi-settings</v-icon>-->
      <!--            </v-btn>-->
      <!--          </template>-->

      <!--          <the-settings-app />-->
      <!--        </v-menu>-->
      <!--      </v-row>-->
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <the-tasks-bar />
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import TheNavigationDrawer from '../../components/the-navigation-drawer';
import ComponentToolbarQualifications from '../../components/qualifications/component-toolbar-qualifications';
import TheTasksBar from '../../components/the-tasks-bar';
import TheSettingsApp from '../../components/the-settings-app';
import TheBreadcrumb from '../../components/the-breadcrumb';
import CreateBatch from '../../components/batches/create/component_create_batch';
import SyncWithMturk from '../../components/batches/component_toolbar_batches';

export default {
  name: 'AppProject',
  components: {
    SyncWithMturk,
    CreateBatch,
    TheBreadcrumb,
    TheSettingsApp,
    TheTasksBar,
    TheNavigationDrawer,
  },
  data() {
    return {
      show_drawer: true,
      id_interval: undefined,
    };
  },
  computed: {
    object_styles_toolbar() {
      if (this.use_sandbox) {
        return { 'background-color': '#dd6e00' };
      }
      return {};
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
