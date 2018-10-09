<template>
<span>
    hi
</span>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    // import ComponentCreateBatch from './create/component_create_batch.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    name: 'component-hit-detail',
    data () {
        return {
        }
    },
    methods: {
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
    },

    components: {
    },
}
</script>