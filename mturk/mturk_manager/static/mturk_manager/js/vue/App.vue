<template>
<v-app dark>
    <router-view v-if="has_loaded_projects">
    </router-view>

    <template v-else>
        <v-spacer></v-spacer>
            <div class="text-xs-center">
                <v-progress-circular
                    indeterminate
                    color="primary"
                ></v-progress-circular>
            </div>
        <v-spacer></v-spacer>
    </template>
</v-app>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import {Service_Endpoint} from "./services/service_endpoint";
    import {router} from "./services/service_router";
    import {Service_Projects} from "./services/service_projects";
    // import ComponentToolbarWorkers from './components/workers/component_toolbar_workers.vue';
export default {
    name: 'app',
    data() {
        return {
            has_loaded_projects: false,
        }
    },
    created: async function() {
        await this.init();

        Service_Endpoint.init(
            this.token_instance,
            () => {
                router.push({name: 'connection_error'});
            }
        );

        await Service_Projects.load_projects();

        Service_Projects.load_project_data();

        this.has_loaded_projects = true;
    },
    watch: {
        slug_project_current() {
            Service_Projects.load_project_data();
        }
    },
    computed: {
        ...mapState(['token_instance']),
        ...mapGetters('moduleProjects', {
            'slug_project_current': 'get_slug_project_current',
        }),
    },
    methods: {
        ...mapActions([
            'init', 
        ]),
    },
    components: {
    }
}
</script>