<template>
<v-app dark>

    <component-navigation-drawer
        v-bind:show_drawer.sync="show_drawer"
    ></component-navigation-drawer>

    <v-progress-linear 
        v-bind:active="show_progress_indicator" 
        height="4" 
        app 
        indeterminate 
        style="z-index: 50; position: absolute; margin: 0"
    ></v-progress-linear>

    <v-toolbar 
        app 
        fixed 
        clipped-left
    >
        <v-toolbar-side-icon @click.stop="show_drawer = !show_drawer"></v-toolbar-side-icon>
        <v-toolbar-title>"{{ name_project }}" - {{name_route_current}}</v-toolbar-title>
        <v-spacer></v-spacer>
        <component 
            v-bind:is="currentTabComponent"
            v-bind:show_progress_indicator="show_progress_indicator"
        ></component>

    </v-toolbar>


    <v-content>
        <v-container fluid>
            <router-view></router-view>
        </v-container>
    </v-content>


<!--     <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click.native="dialog = false">
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>Settings</v-toolbar-title>
          </v-toolbar>
            <v-list three-line subheader>
                <v-subheader>General</v-subheader>
                <v-list-tile avatar>
                    <v-list-tile-action>
                        <v-checkbox v-model="setting_show_with_fee"></v-checkbox>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Show amounts with fee</v-list-tile-title>
                        <v-list-tile-sub-title>Show the displayed amounts of money with regard to the Amazon fee</v-list-tile-sub-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-card>
    </v-dialog> -->


   <!--  <v-snackbar
      v-model="show_snackbar"
      v-bind:timeout="2000"
    >
        {{ text_snackbar }}
        <v-btn flat color="pink" @click.native="show_snackbar = false">Close</v-btn>
    </v-snackbar> -->
</v-app>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentNavigationDrawer from './components/component-navigation-drawer.vue';
    import ComponentToolbarBatches from './components/batches/component-toolbar-batches.vue';
    import ComponentToolbarQualifications from './components/qualifications/component-toolbar-qualifications.vue';
export default {
    name: 'app',
    data() {
        return {
            dialog: false,

            show_drawer: false,
            show_snackbar: false,
            text_snackbar: 'Finished refreshing the data',

        }
    },
    computed: {
        currentTabComponent: function() {
            switch(this.$route.name) 
            {
                case 'Finances':
                    return ComponentToolbarBatches;
                case 'Policies':
                    return ComponentToolbarQualifications;
                case 'Workers':
                    return ComponentToolbarBatches;
            }
        },
        show_progress_indicator: function() {
            return this.get_show_progress_indicator();
        },
        name_route_current: function() {
            // return this.$router.currentRoute;
            return this.$route.name;
        },
        setting_show_with_fee: {
            get: function() {
                return this.show_with_fee;
            },
            set: function(value) {
                this.set_show_with_fee(value);
            }
        },
        ...mapState(['name_project', 'show_with_fee']),
    },
    methods: {
        // refresh_data: function() {
        //     this.is_refreshing = true;
        //     this.sync_database(true).then((result) => {
        //         this.is_refreshing = false;
        //         this.show_snackbar = true;
        //     });
        // },
        ...mapActions(['init', 'set_show_with_fee', 'set_show_progress_indicator']),
        ...mapGetters(['get_show_progress_indicator']),
        // load_config: function() {
        //     const configElement = document.getElementById( 'config' );
        //     const config = JSON.parse( configElement.innerHTML );
        //     console.log(config);
        //     this.url_api_get_balance = config.url_api_get_balance;
        // },
    },
    created: function() {
        this.set_show_progress_indicator(true);
        this.init().then(() => {
            this.set_show_progress_indicator(false);
        });
    },
    components: {
        ComponentNavigationDrawer,
    }
}
</script>

<style lang="scss" scoped>
</style>