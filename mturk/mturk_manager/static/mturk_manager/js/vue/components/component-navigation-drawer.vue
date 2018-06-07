<template>
	<v-navigation-drawer
      v-bind:value="show_drawer"
      @input="$emit('update:show_drawer', $event)"
      clipped
      fixed
      temporary
      app
    >
        <v-list>
            <v-list-tile v-bind:href="url_project">
                <v-list-tile-action>
                    <v-icon>dashboard</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>Dashboard</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
            <v-list-tile 
                v-for="item_menu in list_items_menu"
                v-bind:key="item_menu.path"
                v-bind:to="item_menu.path">
                <v-list-tile-action>
                    <v-icon>{{ item_menu.icon }}</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>{{ item_menu.name }}</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
            <v-divider></v-divider>
            <v-list-tile @click="dialog = true">
                <v-list-tile-action>
                    <v-icon>settings</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>Settings</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
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
	                name: 'Finances',
	                path: '/finances',
	                icon: 'attach_money',
	            },
	            {
	                name: 'Workers',
	                path: '/workers',
	                icon: 'person',
	            },
	            {
	                name: 'Policies',
	                path: '/policies',
	                icon: 'stars',
	            },
	        ],
        }
    },
    computed: {
    	...mapState(['url_project']),
    },

}

</script>