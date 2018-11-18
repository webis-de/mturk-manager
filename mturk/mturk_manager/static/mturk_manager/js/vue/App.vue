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
    // import ComponentToolbarWorkers from './components/workers/component_toolbar_workers.vue';
export default {
    name: 'app',
    data() {
        return {

        }
    },
    created: async function() {
        console.log('init')
        this.set_show_progress_indicator(true);
        await this.init()
        this.set_show_progress_indicator(false);
    },
    computed: {
        ...mapState(['has_loaded_projects']),
    },
    methods: {
        ...mapActions([
            'init', 
            'set_show_progress_indicator', 
        ]),
    },
    components: {
    }
}
</script>