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
export default {
    name: 'component-toolbar-batches',
    data() {
        return {
    	}
    },
    computed: {
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
        refresh_data: function() {
            this.set_show_progress_indicator(true);

            // this.sync_database(true).then((result) => {
            this.sync_mturk(true).then((result) => {
            	this.set_show_progress_indicator(false);
            });
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_database': 'sync_database',
        	'sync_mturk': 'sync_mturk',
        }),
    }
}
</script>