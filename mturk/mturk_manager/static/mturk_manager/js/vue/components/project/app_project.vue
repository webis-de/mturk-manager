<template>
<div>
    <component-navigation-drawer    
        v-bind:show_drawer.sync="show_drawer"
    ></component-navigation-drawer>
    
    <v-progress-linear 
        v-bind:active="get_show_progress_indicator" 
        height="4" 
        app 
        indeterminate 
        style="z-index: 50; position: absolute; margin: 0"
    ></v-progress-linear>

    <v-toolbar 
        app 
        fixed 
        clipped-left
        v-bind:style="object_styles_toolbar"
    >
        <v-toolbar-side-icon @click.stop="show_drawer = !show_drawer"></v-toolbar-side-icon>
        <v-toolbar-title>"{{ project_current.name }}" - {{name_route_current}}</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-layout align-center justify-end>
            <v-flex shrink>
                <v-tooltip bottom>
                    <v-switch 
                        hide-details 
                        slot="activator" 
                        v-bind:label="use_sandbox ? 'Toggle Sandbox' : 'Toggle Sandbox'" 
                        v-bind:input-value="use_sandbox" 
                        v-on:click.native="toggle_use_sandbox"
                    ></v-switch>
                    <span>You are currently <b v-if="!use_sandbox">not</b> using the Sandbox</span>
                </v-tooltip>
            </v-flex>

            <v-divider 
                class="mx-2"
                inset
                vertical
            ></v-divider>

            <v-flex shrink>
                <component  
                    v-bind:name_route="name_route_current"
                    v-bind:is="currentTabComponent"
                ></component>
            </v-flex>
        </v-layout>
    </v-toolbar>

    <v-content>
        <v-container fluid>
            <router-view></router-view>
        </v-container>
    </v-content>
</div>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentNavigationDrawer from '../component-navigation-drawer.vue';
    import ComponentToolbarBatches from '../batches/component_toolbar_batches.vue';
    import ComponentToolbarQualifications from '../qualifications/component-toolbar-qualifications.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
        // load_data,
    ],
    // props: {
    //     // id_batch: {
    //     // },
    // },
    name: 'app-project',
    data () {
        return {
            show_drawer: true,
            id_interval: undefined,
        }
    },
    methods: {
        toggle_use_sandbox: function() {
            this.set_use_sandbox(!this.use_sandbox);
        },
        ...mapActions([
            'set_use_sandbox',
        ]),
    },
    computed: {
        object_styles_toolbar: function() {
            if(this.use_sandbox) {
                return {'background-color': '#dd6e00'};
            } else {
                return {};
            }
        },
        currentTabComponent: function() {
            console.log('this.route', this.$route)
            switch(this.$route.name) 
            {
                case 'finances':
                case 'batches':
                case 'batch':
                case 'hits':
                case 'hit':
                case 'assignments':
                case 'assignment':
                case 'workers':
                    return ComponentToolbarBatches;
                case 'qualifications':
                    return ComponentToolbarQualifications;
                // case 'workers':
                //     return ComponentToolbarWorkers;
            }
        },
        name_route_current: function() {
            // return this.$router.currentRoute;
            return this.$route.meta.name;
        },
        ...mapState(['use_sandbox']),
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
            'slug_project_current': 'get_slug_project_current',
            'object_projects': 'get_object_projects',
        }),
        ...mapGetters(['get_show_progress_indicator']),
    },
    components: {
        ComponentNavigationDrawer,
    },
}
</script>

<style lang="scss" scoped>
    // sandbox switch
    .v-input--selection-controls {
        padding-top: 0;
    }
</style>