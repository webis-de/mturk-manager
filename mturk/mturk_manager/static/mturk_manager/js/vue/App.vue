<template>
<v-app dark>
    <router-view></router-view>
    <!--<template v-if="url_api === null || token_instance === null">-->
        <!--<v-spacer></v-spacer>-->
        <!--<add-credentials></add-credentials>-->
        <!--<v-spacer></v-spacer>-->
    <!--</template>-->
    <!--<template v-else>-->
        <!--<router-view v-if="has_loaded_projects">-->
        <!--</router-view>-->

        <!--<template v-else>-->
            <!--<v-spacer></v-spacer>-->
                <!--<div class="text-xs-center">-->
                    <!--<v-progress-circular-->
                        <!--indeterminate-->
                        <!--color="primary"-->
                    <!--&gt;</v-progress-circular>-->
                <!--</div>-->
            <!--<v-spacer></v-spacer>-->
        <!--</template>-->
    <!--</template>-->
</v-app>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import {Service_Endpoint} from "./services/service_endpoint";
    import {router} from "./services/service_router";
    import {Service_Projects} from "./services/service_projects";
    import AddCredentials from "./views/add-credentials/add-credentials";
    import {Service_App} from "./services/service.app";
    // import ComponentToolbarWorkers from './components/workers/component_toolbar_workers.vue';
export default {
    name: 'app',
    data() {
        return {
            has_loaded_projects: false,
        }
    },
    created: async function() {
        // return await Service_App.init();
        // await this.init();
        //
        // Service_Endpoint.init(
        //     this.token_instance,
        //     () => {
        //         router.push({name: 'connection_error'});
        //     }
        // );
        //
        // await Service_Projects.load_projects();
        //
        // Service_Projects.load_project_data();
        //
        // this.has_loaded_projects = true;
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
        ...mapGetters({
            'url_api': 'get_url_api',
            'token_instance': 'get_token_instance',
        }),
    },
    methods: {
        ...mapActions([
            'init', 
        ]),
    },
    components: {
        AddCredentials
    }
}
</script>