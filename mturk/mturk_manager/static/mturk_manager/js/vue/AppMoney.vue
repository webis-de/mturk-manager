<template>
<v-app dark>
    <v-toolbar>
        <v-toolbar-title>Finances for the "{{ name_project }}"-project</v-toolbar-title>
        <v-spacer></v-spacer>
        
        <v-tooltip bottom>
            <v-btn icon v-on:click="refresh_data_custom" slot="activator">
              <v-icon>refresh</v-icon>
            </v-btn>
            <span>Refresh data</span>
        </v-tooltip>


        <v-toolbar-items>
            <v-btn v-bind:href="url_project" flat>Project</v-btn>
        </v-toolbar-items>
    </v-toolbar>
    <v-progress-linear indeterminate v-bind:active="is_refreshing == true" absolute class="my-0"></v-progress-linear>

    <v-content>
        <v-container fluid>
            <v-layout wrap>
                <v-flex xs12 lg6>
                    <component-show-money-spent></component-show-money-spent>
                </v-flex>
            <!-- </v-layout>
            <v-layout> -->
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
            is_refreshing: false,
            show_snackbar: false,
            text_snackbar: 'Finished refreshing the data',
        }
    },
    computed: {
        ...mapState(['name_project', 'url_project']),
    },
    methods: {
        refresh_data_custom: function() {
            this.is_refreshing = true;
            this.refresh_data().then((result) => {
                this.is_refreshing = false;
                this.show_snackbar = true;
            });
        },
        ...mapActions(['init', 'refresh_data']),
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