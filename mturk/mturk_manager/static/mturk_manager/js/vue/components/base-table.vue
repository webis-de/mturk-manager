<template>
    <div>
        <v-data-table
            select-all
            v-bind:headers="array_headers"
            v-bind:items="array_page"
            v-bind:pagination.sync="pagination"
            v-bind:total-items="items_total"
            v-bind:loading="loading"
            item-key="id"
            class="my-3"
            v-bind:rows-per-page-items="[5,10,25,30,{text: 'All', value: null}]"
        >
            <template slot="headers" slot-scope="props">
                <tr
                    v-bind:style="stylesHeaderRow"
                >
                    <th
                        v-bind:style="stylesHeaderCell"
                    >
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
                        v-bind:style="stylesHeaderCell"
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
                <slot
                    v-bind:props="props"
                    v-bind:array_columns_selected="array_columns_selected"
                    v-bind:is-condensed="isCondensed"
                ></slot>
            </template>

            <template slot="footer">
                <tr>
                    <component-settings-table
                         v-bind:colspan="array_headers.length + 1"
                         v-bind:array_columns="array_columns"
                         v-bind:array_columns_selected="array_columns_selected"
                         v-bind:function_reset="function_reset_array_columns"
                         v-on:change="function_set_array_columns($event)"
                    ></component-settings-table>
                </tr>
            </template>
        </v-data-table>
    </div>
</template>

<script>
    import {update_sandbox} from "../mixins/update_sandbox";
    import {external_pagination} from "../mixins/external_pagination";
    import {table} from "../mixins/table";
    import ComponentSettingsTable from "./helpers/component-settings-table";

    export default {
        name: "base-table",
        components: {ComponentSettingsTable},
        mixins: [
            update_sandbox,
            external_pagination,
            table,
        ],
        props: {
            array_items: {
                type: Function,
                required: true,
            },

            array_columns: {
                type: Array,
                required: true,
            },
            array_columns_selected: {
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
            function_load_page: {
                type: Function,
                required: true,
            },

            object_items_selected: {
                type: Object,
                required: true,
            },
            function_set_items_selected: {
                type: Function,
                required: true,
            },
            function_clear_items_selected: {
                type: Function,
                required: true,
            },

            filters: {
                required: false,
                type: Object,
                default: () => { return {}},
            },

            isCondensed: {
                required: false,
                type: Boolean,
                default: true,
            }
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
            is_page_selected() {
                let is_page_selected = true;

                if(_.size(this.array_page) === 0) {return false;}

                _.forEach(this.array_page, (item) => {
                    if(!_.has(this.object_items_selected, item.id)) {
                        is_page_selected = false;
                        return false;
                    }
                });

                return is_page_selected;
            },
            array_page() {
                let array_items = this.array_items();
                return array_items === null ? [] : array_items;
            },
            stylesHeaderRow() {
                return {
                    height: this.isCondensed ? 'unset' : null,
                };
            },
            stylesHeaderCell() {
                return {
                    padding: this.isCondensed ? '5px' : null,
                };
            },
        },
        methods: {
            load_page() {
                this.loading = true;
                this.function_load_page(this.pagination, this.filters).then((items_total) => {
                    this.items_total = items_total;
                    this.loading = false;
                });
            },
            toggle_all() {
                this.function_set_items_selected({
                    add: !this.is_page_selected,
                    array_items: this.array_page,
                });
            },
        },
        beforeDestroy() {
            this.function_clear_items_selected();
        },
    }
</script>

<style lang="scss" scoped>
</style>