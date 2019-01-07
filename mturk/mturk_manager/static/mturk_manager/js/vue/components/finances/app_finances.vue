<template>
<div>
    <!-- <v-layout wrap>
        <v-flex xs12 md6>
            <component-show-money-spent></component-show-money-spent>
        </v-flex>

        <v-flex xs12 md6 text-md-right>
            <component-show-balance></component-show-balance>
        </v-flex>
    </v-layout> -->

<v-layout>
    <v-flex>
        <display-expenses></display-expenses>
    </v-flex>
</v-layout>
<v-divider class="my-3"></v-divider>
<v-layout>
    <v-flex>
        <component-list-batches
             v-bind:array_columns="array_columns"
             v-bind:array_columns_selected="array_columns_selected"
             v-bind:array_columns_selected_initial="array_columns_selected_initial"
             v-bind:function_reset_array_columns="function_reset_array_columns"
             v-bind:function_set_array_columns="function_set_array_columns"
        ></component-list-batches>
    </v-flex>
</v-layout>
    <!--<v-divider class="my-3"></v-divider>-->
    <!--<div style="max-width: 100%">-->
        <!--<v-flex>-->
            <!--&lt;!&ndash;<component-show-batches></component-show-batches>&ndash;&gt;-->
        <!--</v-flex>-->
    <!--</div>-->
</div>
</template>

<script>
    import { mapState, mapGetters, mapMutations, mapActions } from 'vuex';
	
    import ComponentShowBalance from './component-show-balance.vue';
    import ComponentShowMoneySpent from './component-show-money-spent.vue';
    import ComponentShowBatches from './component-show-batches.vue';
    import ComponentListBatches from '../batches/list/component_list_batches.vue';
    import DisplayExpenses from './display-expenses.vue';
    import slug_project from '../../mixins/slug_project';
export default {
    mixins: [
        slug_project,
        // load_data,
    ],
    name: 'app-finances',
    data () {
        return {
            // dialog: false,

            // drawer: false,
            // is_refreshing: true,
            // show_snackbar: false,
            // text_snackbar: 'Finished refreshing the data',
        }
    },
    methods: {
        ...mapActions('moduleBatches', {
            'function_reset_array_columns': 'reset_array_columns_finances',
        }),
        ...mapMutations('moduleBatches', {
            'function_set_array_columns': 'set_array_columns_finances'
        }),
    },
    computed: {
        ...mapGetters('moduleBatches', {
            'array_columns': 'get_array_columns_general',
            'array_columns_selected': 'get_array_columns_selected_finances',
            'array_columns_selected_initial': 'get_array_columns_selected_initial_finances',
        }),
    },

    components: {
        ComponentShowBalance,
        ComponentShowMoneySpent,
        ComponentShowBatches,
        ComponentListBatches,
        DisplayExpenses,
    },
}
</script>