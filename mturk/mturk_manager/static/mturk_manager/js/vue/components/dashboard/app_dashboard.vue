<template>
<v-layout wrap>
    <v-flex>
        <v-layout wrap>
            <v-flex>
                <component-create-project>
                </component-create-project>
            </v-flex>
        </v-layout>
        <v-divider class="my-3"></v-divider>
        <v-layout wrap>
            <v-flex>
                <component-open-project>
                </component-open-project>
            </v-flex>
        </v-layout>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    import ComponentCreateProject from './component_create_project.vue';
    import ComponentOpenProject from './component_open_project.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    name: 'app-dashboard',

    data () {
        return {
        }
    },
    computed: {
    },
    methods: {
    },
    created: function() {
    },
    components: {
        ComponentCreateProject,
        ComponentOpenProject,
    }
}
</script>