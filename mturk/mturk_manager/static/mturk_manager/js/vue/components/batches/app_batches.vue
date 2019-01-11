<template>
<div>
    <!-- <router-view></router-view> -->
    <template 
        v-if="$route.name === 'batches'"
    >
        <component-list-batches
             v-bind:array_columns_selected="array_columns_selected"
             v-bind:array_columns_selected_initial="array_columns_selected_initial"
             v-bind:function_reset_array_columns="function_reset_array_columns"
             v-bind:function_set_array_columns="function_set_array_columns"
        ></component-list-batches>

        <component-download-batch
        ></component-download-batch>

        <component-create-batch></component-create-batch>
    </template>
    <template 
        v-else-if="$route.name === 'batch'"
    >
        <component-batch-detail
            v-bind:id_batch="id_batch"
        ></component-batch-detail>
    </template>
</div>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    
    import ComponentCreateBatch from './create/component_create_batch.vue';
    import ComponentListBatches from './list/component_list_batches.vue';
    import ComponentBatchDetail from './detail/component_batch_detail.vue';
    import ComponentDownloadBatch from './component_download_batch.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
        // load_data,
    ],
    props: {
        id_batch: {
        },
    },
    name: 'app-batches',
    data () {
        return {
        }
    },
    created() {
    },
    methods: {
        ...mapActions('moduleBatches', {
            'function_reset_array_columns': 'reset_array_columns_general',
        }),
        ...mapMutations('moduleBatches', {
            'function_set_array_columns': 'set_array_columns_general'
        }),
    },
    computed: {
        ...mapGetters('moduleBatches', {
            'array_columns_selected': 'get_array_columns_selected_general',
            'array_columns_selected_initial': 'get_array_columns_selected_initial_general',
        }),
    },
    components: {
     ComponentCreateBatch,
     ComponentListBatches,
     ComponentBatchDetail,
     ComponentDownloadBatch,
    },
}
</script>