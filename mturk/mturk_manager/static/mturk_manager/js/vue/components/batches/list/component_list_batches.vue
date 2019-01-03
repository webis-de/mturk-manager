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
                    >
                    </component-item-batch>
                </template>

                <template slot="footer">
                        <component-settings-table
                             v-bind:colspan="array_headers.length + 1"
                             v-bind:array_columns="array_columns"
                             v-bind:array_columns_selected="array_columns_selected"
                             v-bind:array_columns_selected_initial="array_columns_selected_initial"
                             v-on:change="set_array_columns($event)"
                        ></component-settings-table>
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
            {{array_columns_selected}}
            {{array_columns_selected_initial}}
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
    data () {
        return {
            pagination: { rowsPerPage: 25, sortBy: 'datetime_creation', descending: true },

            loading: false,
            search: '',
            items_total: undefined,

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

            // list_headers: [
            //     {
            //         text: 'Name',
            //         value: 'name',
            //     },
            //     {
            //         text: '#HITs',
            //         value: 'count_hits',
            //         align: 'center',
            //     },
            //     {
            //         text: 'Creation',
            //         value: 'datetime_creation',
            //         align: 'center',
            //     },
            //     {
            //         text: '#Assignments Per HIT',
            //         value: 'settings_batch.count_assignments',
            //         align: 'center',
            //         sortable: false,
            //     },
            //     {
            //         text: 'Reward',
            //         value: 'reward',
            //         align: 'center',
            //     },
        	// 	{
			// 		text: '#Assignments',
			// 		value: 'count_assignments_total',
			// 	},
        	// 	{
			// 		text: '#Approved assignments',
			// 		value: 'count_assignments_approved',
			// 	},
        	// 	{
			// 		text: '#Rejected assignments',
			// 		value: 'count_assignments_rejected',
			// 	},
        	// 	{
			// 		text: 'Max costs',
			// 		value: 'money_spent_max_with_fee',
			// 		align: 'right'
			// 	},
            //     {
            //         text: 'Progress',
            //         value: 'progress',
            //         align: 'center',
            //         sortable: false,
            //     },
            //     {
            //         text: '',
            //         value: 'actions',
            //         sortable: false,
            //     },
            // ],
        }
    },
    computed: {
        ...mapGetters('moduleBatches', {
            'array_items': 'get_array_batches',
            'object_items_selected': 'get_object_batches_selected',
            'array_columns': 'get_array_columns',
            'array_columns_selected': 'get_array_columns_selected',
            'array_columns_selected_initial': 'get_array_columns_selected_initial',
        }),
        array_headers() {
            const set = new Set(this.array_columns_selected);
            return _.filter(this.array_columns, (column) => set.has(column.value));
        },
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
        // ...mapActions('moduleWorkers', {
            // 'update_status_block': 'update_status_block',
        // }),
        ...mapMutations('moduleBatches', {
            'set_items_selected': 'set_batches_selected',
            'clear_batches_selected': 'clear_batches_selected',
            'set_array_columns': 'set_array_columns'
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