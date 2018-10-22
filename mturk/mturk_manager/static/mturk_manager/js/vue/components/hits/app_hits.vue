<template>
<span>
    <template 
        v-if="$route.name == 'hits'"
    >
        <component-list-hits
            v-bind:show_links="true"
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
    import { mapState, mapActions, mapGetters } from 'vuex';
    
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
    },
    watch: {
    },
    computed: {
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