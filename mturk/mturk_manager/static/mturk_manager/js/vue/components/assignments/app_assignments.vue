<template>
<span>
    <template 
        v-if="$route.name == 'assignments'"
    >
        <component-list-assignments
            v-bind:show_links="true"
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
    import { mapState, mapActions, mapGetters } from 'vuex';
    
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
    },
    watch: {
    },
    computed: {
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