<template>
        <div>
            <h1 class="headline">Batches</h1>
            <!-- {{list_batches}} -->
                <!--v-bind:search="search"-->
            <v-data-table
                select-all
                v-bind:headers="array_headers"
                v-bind:items="array_page"
                v-bind:pagination.sync="pagination"
                v-bind:total-items="items_total"
                v-bind:loading="loading"
                item-key="id"
                class="my-3"
            >
                <template slot="headers" slot-scope="props">
                    <tr id="row_header">
                        <th>
                            <v-checkbox
                                v-bind:input-value="is_page_selected"
                                v-bind:indeterminate="props.indeterminate"
                                primary
                                hide-details
                                v-on:click.native="toggle_all()"
                            ></v-checkbox>
                        </th>
                        <th
                            v-for="header in props.headers"
                            v-bind:key="header.value"
                            v-bind:width="header.width"
                            v-bind:class="[
                                'column',
                                {sortable: header.sortable != false}, 
                                pagination.descending ? 'desc' : 'asc', 
                                header.value === pagination.sortBy ? 'active' : ''
                            ]"
                            v-on="header.sortable != false ? {click: () => {pagination.sortBy = header.value; pagination.descending = !pagination.descending}} : {}"
                        >
                            <v-icon small v-if="header.sortable != false">arrow_upward</v-icon>
                            {{ header.text }}
                        </th>
                    </tr>
                </template>

                <template
                    slot="items"
                    slot-scope="props"
                >
                    <component-item-batch
                        v-bind:props="props"
                        v-bind:array_columns_selected="array_columns_selected"
                    >
                    </component-item-batch>
                </template>

                <template slot="footer">
                    <tr>
                        <component-settings-table
                             v-bind:colspan="array_headers.length + 1"
                             v-bind:array_columns="array_columns"
                             v-bind:array_columns_selected="array_columns_selected"
                             v-bind:array_columns_selected_initial="array_columns_selected_initial"
                             v-bind:function_reset="function_reset_array_columns"
                             v-on:change="function_set_array_columns($event)"
                        ></component-settings-table>
                    </tr>
                </template>
                <!-- <template 
                    slot="expand" 
                    slot-scope="props"
                >
                    <v-card flat>
                        <component-item-batch-details
                            v-bind:props="props"
                        >
                        </component-item-batch-details>
                    </v-card>
                </template> -->
            </v-data-table>
            <!-- {{list_workers}} -->
    </div>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemBatch from './component_item_batch.vue';
    import ComponentSettingsTable from '../../helpers/component-settings-table';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import _ from 'lodash';
    import {table} from '../../../mixins/table';
    import {update_sandbox} from "../../../mixins/update_sandbox";
    import {external_pagination} from "../../../mixins/external_pagination";
    import {Service_Batches} from "../../../services/service_batches";
export default {
    mixins: [
        update_sandbox,
        external_pagination,
        table,
    ],
    name: 'component-list-batches',
    props: {
        array_columns_selected: {
            type: Array,
            required: true,
        },
        array_columns_selected_initial: {
            type: Array,
            required: true,
        },
        function_reset_array_columns: {
            type: Function,
            required: true,
        },
        function_set_array_columns: {
            type: Function,
            required: true,
        },
    },
    data () {
        return {
            pagination: { rowsPerPage: 25, sortBy: 'datetime_creation', descending: true },

            loading: false,
            search: '',
            items_total: undefined,
        }
    },
    computed: {
        array_headers() {
            const set = new Set(this.array_columns_selected);
            return _.filter(this.array_columns, (column) => set.has(column.value));
        },
        ...mapGetters('moduleBatches', {
            'array_columns': 'get_array_columns_general',
            'array_items': 'get_array_batches',
            'object_items_selected': 'get_object_batches_selected',
        }),
    },
    methods: {
        load_page() {
            this.loading = true;
            Service_Batches.load_page(this.pagination, {
            }).then((items_total) => {
                this.items_total = items_total;
                this.loading = false;
            });
        },
        // pagination_updated(pagination) {
        //     this.loading = true;
        //     Service_Batches.load_page(pagination).then((items_total) => {
        //         this.items_total = items_total;
        //         this.loading = false;
        //     });
        // },
        // sandbox_updated() {
        //     this.pagination_updated(this.pagination);
        // },
        ...mapMutations('moduleBatches', {
            'set_items_selected': 'set_batches_selected',
            'clear_batches_selected': 'clear_batches_selected',
        }),
    },
    created: function() {
        // console.log(this.list_batches)
            // this.update_status_block({
            //     worker: {name: 'A7W013PM199BS'},
            //     status_block_new: 1,
            //     status_block_old: 2,
            // });
    },
    beforeDestroy() {
        this.clear_batches_selected();
    },
    components: {
        ComponentItemBatch,
        ComponentSettingsTable,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>