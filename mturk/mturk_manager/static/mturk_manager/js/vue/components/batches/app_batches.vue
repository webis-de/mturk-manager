<template>
<div>
    <!-- <router-view></router-view> -->
    <template 
        v-if="$route.name === 'batches'"
    >
        <component-list-batches
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
    import { mapState, mapActions, mapGetters } from 'vuex';
    
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
    },
    computed: {
    },
    components: {
     ComponentCreateBatch,
     ComponentListBatches,
     ComponentBatchDetail,
     ComponentDownloadBatch,
    },
}
</script>