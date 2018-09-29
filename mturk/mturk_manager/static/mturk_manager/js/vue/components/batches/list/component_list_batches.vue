<template>
        <span>
            <!-- {{list_batches}} -->
            <v-data-table
                select-all
                v-bind:pagination.sync="pagination"
                v-bind:headers="list_headers"
                v-bind:items="list_batches"
                v-bind:search="search"
                v-model="batches_selected"
                item-key="id"

            >
                <template slot="headers" slot-scope="props">
                    <tr id="row_header">
                        <th>
                            <v-checkbox
                                v-bind::input-value="props.all"
                                v-bind::indeterminate="props.indeterminate"
                                primary
                                hide-details
                                v-on:click.native="toggleAll"
                            ></v-checkbox>
                        </th>
                        <th
                            v-for="header in props.headers"
                            v-bind:key="header.value"
                            v-bind:width="header.width"
                            v-bind:class="[
                                'column sortable', 
                                pagination.descending ? 'desc' : 'asc', 
                                header.value === pagination.sortBy ? 'active' : ''
                            ]"
                            v-on:click="changeSort(header.value)"
                        >
                            <v-icon small>arrow_upward</v-icon>
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
                <template 
                    slot="expand" 
                    slot-scope="props"
                >
                    <v-card flat>
                        <component-item-batch-details
                            v-bind:props="props"
                        >
                        </component-item-batch-details>
                    </v-card>
                </template>
            </v-data-table>
            <!-- {{list_workers}} -->
    </span>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemBatch from './component_item_batch.vue';
    import ComponentItemBatchDetails from './component_item_batch_details.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import table from '../../../mixins/table';
export default {
    mixins: [
        table,
    ],
    name: 'component-list-batches',
    data () {
        return {
            batches_selected: [],
            pagination: { rowsPerPage: 25 },

            search: '',

            // search: 'A10BOAO1EONNS7',
            // policy_new: new Policy({
            //     QualificationTypeStatus: 'Active',
            // }),

            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
                {
                    text: '#HITs',
                    value: 'count_hits',
                    align: 'center',
                },
                {
                    text: '#Assignments Per HIT',
                    value: 'count_assignments',
                    align: 'center',
                },
            ],
        }
    },
    computed: {
        ...mapGetters('moduleBatches', {
            'list_batches': 'list_batches',
        }),
        // ...mapGetters('moduleProjects', {
        //     'project_current': 'get_project_current',
        // }),
    },
    methods: {
        // ...mapActions('moduleWorkers', {
            // 'update_status_block': 'update_status_block',
        // }),
    },
    created: function() {

            // this.update_status_block({
            //     worker: {name: 'A7W013PM199BS'},
            //     status_block_new: 1,
            //     status_block_old: 2,
            // });
    },

    components: {
        ComponentItemBatch,
        ComponentItemBatchDetails,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>