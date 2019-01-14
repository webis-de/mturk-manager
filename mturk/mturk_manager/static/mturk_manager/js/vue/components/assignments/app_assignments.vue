<template>
<span>
    <template 
        v-if="$route.name == 'assignments'"
    >
        <component-list-assignments
            v-bind:show_links="true"

            v-bind:array_columns_selected="array_columns_selected"
            v-bind:array_columns_selected_initial="array_columns_selected_initial"
            v-bind:function_reset_array_columns="function_reset_array_columns"
            v-bind:function_set_array_columns="function_set_array_columns"
        ></component-list-assignments>
        <component-annotate>
        </component-annotate>
    </template>
    <template 
        v-else-if="$route.name == 'assignment'"
    >
        <component-assignment-detail
            v-bind:id_assignment="id_assignment"
        ></component-assignment-detail>
    </template>
</span>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    
    // import ComponentCreateBatch from './create/component_create_batch.vue';
    import ComponentListAssignments from './list/component_list_assignments.vue';
    import ComponentAssignmentDetail from './detail/component_assignment_detail.vue';
    import ComponentAnnotate from './annotate/component_annotate.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    props: {
        id_assignment: {
        }
    },
    name: 'app-assignments',
    data () {
        return {
        }
    },
    methods: {
        ...mapActions('moduleAssignments', {
            'function_reset_array_columns': 'reset_array_columns_general',
        }),
        ...mapMutations('moduleAssignments', {
            'function_set_array_columns': 'set_array_columns_general'
        }),
    },
    computed: {
        ...mapGetters('moduleAssignments', {
            'array_columns_selected': 'get_array_columns_selected_general',
            'array_columns_selected_initial': 'get_array_columns_selected_initial_general',
        }),
    },
    created: function() {
    },

    components: {
     // ComponentCreateBatch,
     ComponentListAssignments,
     ComponentAssignmentDetail,
     ComponentAnnotate,
    },
}
</script>