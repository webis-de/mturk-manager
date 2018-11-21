<template>
        <div>
            <h1 class="headline">Batches</h1>
            <!-- {{list_batches}} -->
            <v-data-table
                select-all
                v-bind:pagination.sync="pagination"
                v-bind:headers="list_headers"
                v-bind:items="list_batches"
                v-bind:search="search"
                v-model="batches_selected"
                item-key="id"
                class="my-3"
            >
                <template slot="headers" slot-scope="props">
                    <tr id="row_header">
                        <th>
                            <v-checkbox
                                v-bind:input-value="props.all"
                                v-bind:indeterminate="props.indeterminate"
                                primary
                                hide-details
                                v-on:click.native="batches_selected = toggleAll(batches_selected, list_batches)"
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
                            v-on="header.sortable != false ? {click: () => changeSort(header.value)} : {}"
                        >
                            <v-icon small v-if="header.sortable != false">arrow_upward</v-icon>
                            {{ header.text }}
                            <!-- v-on:click="changeSort(header.value)" -->
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
                    value: 'hits.length',
                    align: 'center',
                },
                {
                    text: 'Creation',
                    value: 'datetime_creation',
                    align: 'center',
                },
                {
                    text: '#Assignments Per HIT',
                    value: 'settings_batch.count_assignments',
                    align: 'center',
                },
                {
                    text: 'Progress',
                    value: 'progress',
                    align: 'center',
                },
                {
                    text: '',
                    value: 'actions',
                    sortable: false,
                },
            ],
        }
    },
    computed: {
        batches_selected: {
            get() {
                return this.array_batches_selected;
            },
            set(value) {
                this.set_batches_selected(value);
                // this.$store.commit('set_batches_selected', value);
            }
        },
        ...mapGetters('moduleBatches', {
            'list_batches': 'list_batches',
        }),
        ...mapState('moduleBatches', {
            'array_batches_selected': 'array_batches_selected',
        }),
    },
    methods: {
        // ...mapActions('moduleWorkers', {
            // 'update_status_block': 'update_status_block',
        // }),
        ...mapMutations('moduleBatches', {
            'set_batches_selected': 'set_batches_selected',
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

    components: {
        ComponentItemBatch,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>