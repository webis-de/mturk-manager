<template>
    <component-create-batch>
    </component-create-batch>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    import ComponentCreateBatch from './component_create_batch.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'app-batches',

    data () {
        return {
            dialog: false,

            drawer: false,
            is_refreshing: true,
            show_snackbar: false,
            text_snackbar: 'Finished refreshing the data',
        }
    },
    methods: {
        refresh_data() {
            this.set_show_progress_indicator(true);
            this.set_show_progress_indicator(true);

            this.sync_database().then(() => {
                this.set_show_progress_indicator(false);
            });
            
            this.update_balance().then(() => {
                this.set_show_progress_indicator(false);
            });
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_database': 'sync_database', 
        }),
        ...mapActions('moduleMoney', {
            'update_balance': 'update_balance'
        }),
    },
    watch: {
        use_sandbox: function() {
            this.refresh_data();
        },
    },
    computed: {
        ...mapState(['use_sandbox']),
    },
    created: function() {
        this.refresh_data();
    },

    components: {
     ComponentCreateBatch,
     // ComponentShowMoneySpent,
     // ComponentShowBatches,
    },
}
</script>