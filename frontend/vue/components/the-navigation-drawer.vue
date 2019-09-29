<template>
  <v-navigation-drawer
    v-bind:value="showDrawer"
    clipped
    fixed
    app
    v-on:input="$emit('update:show_drawer', $event)"
  >
    <!-- temporary -->
    <v-list
      dense
      nav
    >
      <v-list-item
        v-for="item_menu in list_items_menu"
        v-bind:key="item_menu.name"
        v-bind:to="{ name: item_menu.name }"
        v-bind:exact="item_menu.name === 'dashboard'"
      >
        <v-list-item-action>
          <v-icon>{{ item_menu.icon }}</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>{{ item_menu.label }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-list-item
        v-bind:to="{ name: 'aboutProject' }"
      >
        <v-list-item-action>
          <v-icon>mdi-information</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>
            About
          </v-list-item-title>
        </v-list-item-content>

        <v-list-item-action>
          <changelog-notification />
        </v-list-item-action>
      </v-list-item>
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
          icon: 'mdi-format-list-bulleted',
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
          icon: 'mdi-note',
        },
        {
          name: 'finances',
          label: 'Finances',
          icon: 'mdi-currency-usd',
        },
        {
          name: 'workers',
          label: 'Workers',
          icon: 'mdi-account',
        },
        {
          name: 'settings_project',
          label: 'Project Settings',
          icon: 'mdi-settings',
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
