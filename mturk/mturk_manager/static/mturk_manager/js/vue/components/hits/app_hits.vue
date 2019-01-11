<template>
<span>
    <template 
        v-if="$route.name == 'hits'"
    >
        <component-list-hits
            v-bind:show_links="true"

            v-bind:array_columns_selected="array_columns_selected"
            v-bind:array_columns_selected_initial="array_columns_selected_initial"
            v-bind:function_reset_array_columns="function_reset_array_columns"
            v-bind:function_set_array_columns="function_set_array_columns"
        ></component-list-hits>
    </template>
    <template 
        v-else-if="$route.name == 'hit'"
    >
        <component-hit-detail
            v-bind:id_hit="id_hit"
        ></component-hit-detail>
    </template>
</span>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    
    // import ComponentCreateBatch from './create/component_create_batch.vue';
    import ComponentListHits from './list/component_list_hits.vue';
    import ComponentHitDetail from './detail/component_hit_detail.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
    ],
    props: {
        id_hit: {
        }
    },
    name: 'app-hits',
    data () {
        return {
        }
    },
    methods: {
        ...mapActions('moduleHITs', {
            'function_reset_array_columns': 'reset_array_columns_general',
        }),
        ...mapMutations('moduleHITs', {
            'function_set_array_columns': 'set_array_columns_general'
        }),
    },
    computed: {
        ...mapGetters('moduleHITs', {
            'array_columns_selected': 'get_array_columns_selected_general',
            'array_columns_selected_initial': 'get_array_columns_selected_initial_general',
        }),
    },
    created: function() {
    },

    components: {
     // ComponentCreateBatch,
     ComponentListHits,
     ComponentHitDetail,
    },
}
</script>