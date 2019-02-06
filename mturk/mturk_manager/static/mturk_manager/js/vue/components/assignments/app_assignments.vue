<template>
<span>
    <template 
        v-if="$route.name == 'assignments'"
    >
        <list-assignments></list-assignments>
        <component-annotate></component-annotate>
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
    import ComponentAssignmentDetail from './detail/component_assignment_detail.vue';
    import ComponentAnnotate from './annotate/component_annotate.vue';
    import slug_project from '../../mixins/slug_project';
    import ListAssignments from "./list/list-assignments";
export default {
    mixins: [
        slug_project,
    ],
    props: {
        id_assignment: {
        }
    },
    name: 'app-assignments',

    components: {
        ListAssignments,
        ComponentAssignmentDetail,
        ComponentAnnotate,
    },
}
</script>