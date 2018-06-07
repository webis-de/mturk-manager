<template>
    <v-tooltip bottom>
        <v-btn icon v-bind:loading="show_progress_indicator" v-on:click="refresh_data" slot="activator">
            <v-icon>refresh</v-icon>
        </v-btn>
        <span>Refresh batch data</span>
    </v-tooltip>
</template>

<script>
    import { mapState, mapActions } from 'vuex';
export default {
    name: 'component-toolbar-batches',
    props: {
    	show_progress_indicator: {
    		required: true,
    		type: Boolean,
    	}
    } ,
    data() {
        return {
    	}
    },
    methods: {
        refresh_data: function() {
            this.set_show_progress_indicator(true);

            this.sync_database(true).then((result) => {
            	this.set_show_progress_indicator(false);
            });
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
        	'sync_database': 'sync_database',
        }),
    }
}
</script>