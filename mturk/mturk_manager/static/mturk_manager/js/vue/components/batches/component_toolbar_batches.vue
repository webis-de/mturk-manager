<template>
<v-layout align-center justify-end>
    <v-flex shrink>
        <v-tooltip bottom>
            <v-btn 
                flat
                v-bind:loading="get_show_progress_indicator" 
                v-on:click="refresh_data(true)" 
                slot="activator"
            >
                <v-icon>refresh</v-icon>
                Refresh Data
            </v-btn>
            <span>Refresh batch data</span>
        </v-tooltip>
    </v-flex>
    <v-flex shrink>
        <v-tooltip bottom>
            <v-btn 
                flat
                v-bind:loading="is_syncing_mturk" 
                v-on:click="sync_mturk(true)" 
                slot="activator"
            >
                <v-icon>sync</v-icon>
                Sync with MTurk
            </v-btn>
            <span>Refresh batch data</span>
        </v-tooltip>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import slug_project from '../../mixins/slug_project';
    import load_data from '../../mixins/load_data';
    import {Service_Batches} from "../../services/service_batches";
export default {
    mixins: [
        // slug_project,
        load_data,
    ],
    name: 'component-toolbar-batches',
    props: {
        name_route: {
        },
    },
    data() {
        return {
    	}
    },
    created() {
        // console.log($route);
    },
    computed: {
        ...mapGetters(['get_show_progress_indicator']),
        ...mapGetters('moduleBatches', {
            'is_syncing_mturk': 'get_is_syncing_mturk',
        }),
    },
    methods: {
        sync_mturk() {
            Service_Batches.sync_mturk();
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_database': 'sync_database',
        }),
    }
}
</script>