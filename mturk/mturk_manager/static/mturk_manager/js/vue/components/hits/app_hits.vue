<template>
<span>
    <template 
        v-if="$route.name == 'hits'"
    >
        <component-list-hits
            v-bind:show_links="false"
        ></component-list-hits>
    </template>
    <template 
        v-else-if="$route.name == 'hit'"
    >
        <component-hit-detail
        ></component-hit-detail>
    </template>
</span>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    // import ComponentCreateBatch from './create/component_create_batch.vue';
    import ComponentListHits from './list/component_list_hits.vue';
    import ComponentHitDetail from './component_hit_detail.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    name: 'app-hits',
    data () {
        return {
        }
    },
    methods: {
        refresh_data() {
            this.set_show_progress_indicator(true);

            this.sync_batches().then(() => {
                this.set_show_progress_indicator(false);
            });
        },
        ...mapActions(['set_show_progress_indicator']),
        ...mapActions('moduleBatches', {
            'sync_batches': 'sync_batches', 
        }),
        // ...mapActions('moduleMoney', {
        //     'update_balance': 'update_balance'
        // }),
    },
    watch: {
        // use_sandbox: function() {
        //     this.refresh_data();
        // },
    },
    computed: {
        ...mapState(['use_sandbox']),
    },
    created: function() {
        this.refresh_data();
        console.log(this.$route)
    },

    components: {
     // ComponentCreateBatch,
     ComponentListHits,
     ComponentHitDetail,
    },
}
</script>