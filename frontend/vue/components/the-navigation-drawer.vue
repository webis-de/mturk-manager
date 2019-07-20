<template>
  <v-navigation-drawer
    v-bind:value="showDrawer"
    clipped
    fixed
    app
    v-on:input="$emit('update:show_drawer', $event)"
  >
    <!-- temporary -->
    <v-list>
      <v-list-tile
        v-for="item_menu in list_items_menu"
        v-bind:key="item_menu.name"
        v-bind:to="{ name: item_menu.name }"
        v-bind:exact="item_menu.name === 'dashboard'"
      >
        <v-list-tile-action>
          <v-icon>{{ item_menu.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ item_menu.label }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-divider />
      <v-list-tile
        v-bind:to="{ name: 'aboutProject' }"
      >
        <v-list-tile-action>
          <v-icon>info</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>
            About
          </v-list-tile-title>
        </v-list-tile-content>

        <v-list-tile-action>
          <changelog-notification />
        </v-list-tile-action>
      </v-list-tile>
      <!-- <v-list-tile>
                <v-list-tile-action>
                    <v-icon>settings</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>Settings</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile> -->
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapState } from 'vuex';
import ChangelogNotification from './about/changelog-notification';

export default {
  name: 'TheNavigationDrawer',
  components: { ChangelogNotification },
  props: {
    showDrawer: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {
      list_items_menu: [
        {
          name: 'dashboard',
          label: 'Projects',
          icon: 'list',
          // icon: 'ballot',
        },
        // {
        //     name: 'dashboard',
        //     label: 'Projects',
        //     icon: 'list',
        //     // icon: 'ballot',
        // },
        {
          name: 'tasks',
          label: 'Tasks',
          icon: 'notes',
        },
        {
          name: 'finances',
          label: 'Finances',
          icon: 'attach_money',
        },
        {
          name: 'workers',
          label: 'Workers',
          icon: 'person',
        },
        {
          name: 'settings_project',
          label: 'Project Settings',
          icon: 'settings_applications',
        },
        // {
        //     name: 'Qualifications',
        //     path: '/qualifications',
        //     icon: 'stars',
        // },
      ],
    };
  },
  computed: {
    ...mapState(['url_project']),
  },
};
</script>
