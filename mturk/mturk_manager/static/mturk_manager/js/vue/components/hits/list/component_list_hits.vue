<template>
<v-layout wrap>
    <v-flex>
        <!-- {{list_batches}} -->
        <h1 class="headline">HITs</h1>
        <v-data-table
            select-all
            v-bind:pagination.sync="pagination"
            v-bind:headers="array_headers"
            v-bind:items="array_page"
            v-bind:total-items="items_total"
            item-key="id"
            class="my-3"
            v-bind:loading="loading"
            v-bind:rows-per-page-items="[5,10,25,30,{text: 'All', value: null}]"
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
                            'column sortable', 
                            pagination.descending ? 'desc' : 'asc', 
                            header.value === pagination.sortBy ? 'active' : ''
                        ]"
                        v-on="header.sortable != false ? {click: () => {pagination.sortBy = header.value; pagination.descending = !pagination.descending}} : {}"
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
                <component-item-hit
                    v-bind:props="props"
                    v-bind:show_links="show_links"
                    v-bind:array_columns_selected="array_columns_selected"
                >
                </component-item-hit>
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
        </v-data-table>
        <!-- {{list_workers}} -->
    </v-flex>
</v-layout>
</template>
<script>
    import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
    // import { Policy } from '../../store/modules/policies.js';
    import ComponentItemHit from './component_item_hit.vue';
    import ComponentSettingsTable from '../../helpers/component-settings-table';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import {table} from '../../../mixins/table';
    import {update_sandbox} from "../../../mixins/update_sandbox";
    import {external_pagination} from "../../../mixins/external_pagination";
    import {Service_HITs} from "../../../services/service_hits";
    import Batch from "../../../classes/batch";
    import _ from 'lodash';
export default {
    mixins: [
        update_sandbox,
        external_pagination,
        table,
    ],
    name: 'component-list-hits',
    props: {
        id_batch: {
            required: false,
            type: Number,
        },
        show_links: {
            required: false,
            type: Boolean,
            default: true,
        },
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
            hits_selected: [],
            pagination: { rowsPerPage: 25, sortBy: 'datetime_creation', descending: true },

            search: '',

            items_total: undefined,

            loading: false,

        }
    },
    computed: {
        array_headers() {
            const set = new Set(this.array_columns_selected);
            return _.filter(this.array_columns, (column) => set.has(column.value));
        },
        ...mapGetters('moduleHITs', {
            'array_columns': 'get_array_columns_general',
            'array_items': 'get_array_hits',
            'object_items_selected': 'get_object_hits_selected',
        }),
    },
    methods: {
        load_page() {
            this.loading = true;
            Service_HITs.load_page(this.pagination, {
                id_batch: this.id_batch,
            }).then((items_total) => {
                this.items_total = items_total;
                this.loading = false;
            });
        },
        ...mapMutations('moduleHITs', {
            'function_set_items_selected': 'set_hits_selected',
            'clear_batches_selected': 'clear_hits_selected',
        }),
    },
    created: function() {

            // this.update_status_block({
            //     worker: {name: 'A7W013PM199BS'},
            //     status_block_new: 1,
            //     status_block_old: 2,
            // });
    },

    components: {
        ComponentItemHit,
        ComponentSettingsTable,
    },
}
</script>

<style lang="scss" scoped>
    #row_header {
        height: 48px;
    }
</style>