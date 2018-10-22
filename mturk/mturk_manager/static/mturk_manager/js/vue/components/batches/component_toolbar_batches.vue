<template>
    <v-tooltip bottom>
        <v-btn icon v-bind:loading="get_show_progress_indicator" v-on:click="refresh_data" slot="activator">
            <v-icon>refresh</v-icon>
        </v-btn>
        <span>Refresh batch data</span>
    </v-tooltip>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import slug_project from '../../mixins/slug_project';
    import load_data from '../../mixins/load_data';
export default {
    mixins: [
        // slug_project,
        load_data,
    ],
    name: 'component-toolbar-batches',
    data() {
        return {
    	}
    },
    computed: {
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_database': 'sync_database',
        	'sync_mturk': 'sync_mturk',
        }),
    }
}
</script>