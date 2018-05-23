<template>
<v-app dark>
    <v-navigation-drawer
      v-model="drawer"
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
            <v-list-tile-title>Project</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
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


    <v-toolbar app fixed clipped-left>
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <v-toolbar-title>Finances for the "{{ name_project }}"-project</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
            <v-btn icon v-bind:loading="is_refreshing" v-on:click="refresh_data_custom" slot="activator">
              <v-icon>refresh</v-icon>
            </v-btn>
            <span>Refresh data</span>
        </v-tooltip>

    </v-toolbar>


    <v-content>
        <v-container fluid>
            <v-layout wrap>
                <v-flex xs12 lg6>
                    <component-show-money-spent></component-show-money-spent>
                </v-flex>

                <v-flex xs12 lg6>
                    <component-show-balance></component-show-balance>
                </v-flex>
            </v-layout>
            <v-divider class="my-3"></v-divider>
            <v-layout wrap>
                <v-flex>
                    <component-show-batches></component-show-batches>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>


    <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
        <v-card>
          <v-toolbar dark color="primary">
            <v-btn icon dark @click.native="dialog = false">
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>Settings</v-toolbar-title>
            <!-- <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn dark flat @click.native="dialog = false">Save</v-btn>
            </v-toolbar-items> -->
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
      </v-dialog>


    <v-snackbar
      v-model="show_snackbar"
      v-bind:timeout="2000"
    >
      {{ text_snackbar }}
      <v-btn flat color="pink" @click.native="show_snackbar = false">Close</v-btn>
    </v-snackbar>
</v-app>
</template>

<script>
    import ComponentShowBalance from './components/component-show-balance.vue';
    import ComponentShowMoneySpent from './components/component-show-money-spent.vue';
    import ComponentShowBatches from './components/component-show-batches.vue';
    import { mapState, mapActions } from 'vuex';
export default {
    name: 'app-money',
    data () {
        return {
            dialog: false,

            drawer: false,
            is_refreshing: false,
            show_snackbar: false,
            text_snackbar: 'Finished refreshing the data',
        }
    },
    computed: {
        setting_show_with_fee: {
            get: function() {
                return this.show_with_fee;
            },
            set: function(value) {
                this.set_show_with_fee(value);
            }
        },
        ...mapState(['name_project', 'url_project', 'show_with_fee']),
    },
    methods: {
        refresh_data_custom: function() {
            this.is_refreshing = true;
            this.refresh_data().then((result) => {
                this.is_refreshing = false;
                this.show_snackbar = true;
            });
        },
        ...mapActions(['init', 'refresh_data', 'set_show_with_fee']),
        // load_config: function() {
        //     const configElement = document.getElementById( 'config' );
        //     const config = JSON.parse( configElement.innerHTML );
        //     console.log(config);
        //     this.url_api_get_balance = config.url_api_get_balance;
        // },
    },
    created: function() {
        this.init();
        // this.load_config();
    },
    components: {
     ComponentShowBalance,
     ComponentShowMoneySpent,
     ComponentShowBatches,
    },
}
</script>

<style lang="scss" scoped>
</style>