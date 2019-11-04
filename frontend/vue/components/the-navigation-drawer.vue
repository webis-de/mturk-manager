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
      <template
        v-for="item_menu in list_items_menu"
      >
        <v-list-item
          v-if="item_menu.children === undefined"
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
        <!--
          children
        -->
        <v-list-group
          v-else
          v-bind:key="`${item_menu.name}_children`"
          v-bind:value="true"
          disabled
          no-action
          color="white"
          v-bind:ripple="false"
          exact
          class="navigation-drawer-list-group"
        >
          <template
            v-slot:activator
          >
            <v-list-item-action>
              <v-icon>{{ item_menu.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-title>{{ item_menu.label }}</v-list-item-title>
          </template>

          <v-list-item
            v-for="child in item_menu.children"
            v-bind:key="child.name"
            v-bind:to="{ name: child.name }"
            dense
          >
            <v-list-item-content class="pl-3">
              <v-list-item-title>{{ child.label }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </template>
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
              name: 'tasksBatches',
              label: 'Batches',
            },
            {
              name: 'tasksHITs',
              label: 'HITs',
            },
            {
              name: 'tasksAssignments',
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

<style lang="scss">
  .navigation-drawer-list-group .v-list-item__icon.v-list-group__header__append-icon {
    display: none;
  }
</style>
