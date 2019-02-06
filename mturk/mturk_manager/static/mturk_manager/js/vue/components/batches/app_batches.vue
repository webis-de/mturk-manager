<template>
<div>
    <!-- <router-view></router-view> -->
    <template 
        v-if="$route.name === 'batches'"
    >

        <h1 class="headline">Batches</h1>
        <list-batches></list-batches>

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
    import ComponentBatchDetail from './detail/component_batch_detail.vue';
    import ComponentDownloadBatch from './component_download_batch.vue';
    import slug_project from '../../mixins/slug_project';
    import DataTable from "../data-table";
    import ComponentItemBatch from "./list/component_item_batch";
    import {Service_Batches} from "../../services/service_batches";
    import ListBatches from "./list/list-batches";
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
    components: {
        ListBatches,
        ComponentItemBatch,
        DataTable,
        ComponentCreateBatch,
        ComponentBatchDetail,
        ComponentDownloadBatch,
    },
}
</script>