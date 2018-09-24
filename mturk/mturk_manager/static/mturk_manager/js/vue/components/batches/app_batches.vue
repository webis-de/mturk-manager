<template>
<span>
    <!-- <component-create-batch></component-create-batch> -->
    <component-list-batches></component-list-batches>
</span>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    import ComponentCreateBatch from './create/component_create_batch.vue';
    import ComponentListBatches from './list/component_list_batches.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    name: 'app-batches',
    data () {
        return {
        }
    },
    methods: {
        refresh_data() {
            this.set_show_progress_indicator(true);
            this.set_show_progress_indicator(true);

            this.sync_database().then(() => {
                this.set_show_progress_indicator(false);
            });

            this.sync_batches().then(() => {
                this.set_show_progress_indicator(false);
            });
            
            this.update_balance().then(() => {
                this.set_show_progress_indicator(false);
            });
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_database': 'sync_database', 
            'sync_batches': 'sync_batches', 
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
        // this.refresh_data();
    },

    components: {
     ComponentCreateBatch,
     ComponentListBatches,
    },
}
</script>