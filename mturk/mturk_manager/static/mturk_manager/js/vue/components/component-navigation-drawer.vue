<template>
	<v-navigation-drawer
      v-bind:value="show_drawer"
      @input="$emit('update:show_drawer', $event)"
      clipped
      fixed
      app
    >
      <!-- temporary -->
        <v-list>
            <v-list-tile 
                v-for="item_menu in list_items_menu"
                v-bind:key="item_menu.name"
                v-bind:to="{ name: item_menu.name }"
                exact
            >
                <v-list-tile-action>
                    <v-icon>{{ item_menu.icon }}</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>{{ item_menu.label }}</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
            <v-divider></v-divider>
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
    import { mapState, mapActions } from 'vuex';
export default {
    name: 'component-navigation-drawer',
    props: {
    	show_drawer: {
    		required: true,
    		type: Boolean,
    	}
    },
    data() {
        return {
            list_items_menu: [
                {
                    label: 'Dashboard',
                    name: 'dashboard',
                    icon: 'dashboard',
                    // icon: 'ballot',
                },
                {
                    label: 'Batches',
                    name: 'batches',
                    icon: 'notes',
                    // icon: 'ballot',
                },
                {
                    label: 'HITs',
                    name: 'hits',
                    icon: 'notes',
                    // icon: 'ballot',
                },
                {
                    label: 'Finances',
                    name: 'finances',
                    icon: 'attach_money',
                },
                {
                    label: 'Workers',
                    name: 'workers',
                    icon: 'person',
                },
                {
                    label: 'Project Settings',
                    name: 'settings_project',
                    icon: 'settings_applications',
                },
	            // {
	            //     name: 'Qualifications',
	            //     path: '/qualifications',
	            //     icon: 'stars',
	            // },
	        ],
        }
    },
    computed: {
    	...mapState(['url_project']),
    },

}

</script>