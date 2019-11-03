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
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'TheNavigationDrawer',
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
          icon: 'mdi-format-list-bulleted-square',
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
          icon: 'mdi-note-multiple',
          children: [
            {
              name: 'batches',
              label: 'Batches',
            },
            {
              name: 'hits',
              label: 'HITs',
            },
            {
              name: 'assignments',
              label: 'Assignments',
            },
          ],
        },
        {
          name: 'finances',
          label: 'Finances',
          icon: 'mdi-currency-usd',
        },
        {
          name: 'workers',
          label: 'Workers',
          icon: 'mdi-account-group',
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
