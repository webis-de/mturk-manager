<template>
    <data-table
         v-bind:array_items="array_items"

         v-bind:array_columns="array_columns"
         v-bind:array_columns_selected="array_columns_selected"

         v-bind:function_reset_array_columns="function_reset_array_columns"
         v-bind:function_set_array_columns="function_set_array_columns"
         v-bind:function_load_page="function_load_page"

         v-bind:object_items_selected="object_items_selected"
         v-bind:function_set_items_selected="function_set_items_selected"
         v-bind:function_clear_items_selected="function_clear_items_selected"

         v-bind:filters="{
            id_hit
         }"

         v-slot="{props, array_columns_selected}"
    >
        <component-item-assignment
            v-bind:props="props"
            v-bind:array_columns_selected="array_columns_selected"
            v-bind:show_links="show_links"
        ></component-item-assignment>
    </data-table>
</template>

<script>
    import {mapActions, mapGetters, mapMutations} from "vuex";
    import {Service_Assignments} from "../../../services/service_assignments";
    import DataTable from "../../data-table";
    import ComponentItemAssignment from "./component_item_assignment";

    export default {
        name: "list-assignments",
        components: {ComponentItemAssignment, DataTable},
        props: {
            id_hit: {
                required: false,
                type: Number,
            },
            show_links: {
                required: false,
                type: Boolean,
                default: true,
            },
        },
        data () {
            return {
                function_load_page: Service_Assignments.load_page,
            }
        },
        methods: {
            ...mapActions('moduleAssignments', {
                'function_reset_array_columns': 'reset_array_columns_general',
            }),
            ...mapMutations('moduleAssignments', {
                'function_set_items_selected': 'set_assignments_selected',
                'function_clear_items_selected': 'clear_assignments_selected',
                'function_set_array_columns': 'set_array_columns_general'
            }),
        },
        computed: {
            ...mapGetters('moduleAssignments', {
                'array_items': 'get_array_assignments',
                'object_items_selected': 'get_object_assignments_selected',
                'array_columns': 'get_array_columns_general',
                'array_columns_selected': 'get_array_columns_selected_general',
            }),
        },
    }
</script>

<style scoped>

</style>