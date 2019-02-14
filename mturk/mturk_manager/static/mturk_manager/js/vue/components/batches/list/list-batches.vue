<template>
    <base-table
         v-bind:array_items="array_items"

         v-bind:array_columns="array_columns"
         v-bind:array_columns_selected="array_columns_selected_computed"

         v-bind:function_reset_array_columns="function_reset_array_columns_computed"
         v-bind:function_set_array_columns="function_set_array_columns_computed"
         v-bind:function_load_page="function_load_page"

         v-bind:object_items_selected="object_items_selected"
         v-bind:function_set_items_selected="function_set_items_selected"
         v-bind:function_clear_items_selected="function_clear_items_selected"

         v-slot="{props, array_columns_selected, isCondensed}"
    >
        <component-item-batch
            v-bind:props="props"
            v-bind:array_columns_selected="array_columns_selected"
            v-bind:show_links="show_links"
            v-bind:is-condensed="isCondensed"
        ></component-item-batch>
    </base-table>
</template>

<script>
    import {mapActions, mapGetters, mapMutations} from "vuex";
    import {Service_Batches} from "../../../services/service_batches";
    import BaseTable from "../../base-table";
    import ComponentItemBatch from "./component_item_batch";

    export default {
        name: "list-batches",
        components: {ComponentItemBatch, BaseTable},
        props: {
            show_links: {
                required: false,
                type: Boolean,
                default: true,
            },
            function_reset_array_columns: {
                required: false,
                type: Function,
            },
            function_set_array_columns: {
                required: false,
                type: Function,
            },
            array_columns_selected: {
                required: false,
                type: Array,
            },
        },
        data () {
            return {
                function_load_page: Service_Batches.load_page,
            }
        },
        methods: {
            ...mapActions('moduleBatches', {
                'function_reset_array_columns_general': 'reset_array_columns_general',
            }),
            ...mapMutations('moduleBatches', {
                'function_set_items_selected': 'set_batches_selected',
                'function_clear_items_selected': 'clear_batches_selected',
                'function_set_array_columns_general': 'set_array_columns_general'
            }),
        },
        computed: {
            function_reset_array_columns_computed() {
                return this.function_reset_array_columns !== undefined ? this.function_reset_array_columns: this.function_reset_array_columns_general;
            },
            function_set_array_columns_computed() {
                return this.function_set_array_columns !== undefined ? this.function_set_array_columns: this.function_set_array_columns_general;
            },
            array_columns_selected_computed() {
                return this.array_columns_selected !== undefined ? this.array_columns_selected: this.array_columns_selected_general;
            },
            ...mapGetters('moduleBatches', {
                'array_items': 'get_array_batches',
                'object_items_selected': 'get_object_batches_selected',
                'array_columns': 'get_array_columns_general',
                'array_columns_selected_general': 'get_array_columns_selected_general',
            }),
        },
    }
</script>

<style scoped>

</style>