<template>
<div>
    <!-- <v-layout wrap>
        <v-flex xs12 md6>
            <component-show-money-spent></component-show-money-spent>
        </v-flex>

        <v-flex xs12 md6 text-md-right>
        </v-flex>
    </v-layout> -->

<v-layout>
    <v-flex>
        <component-show-balance></component-show-balance>
        <display-expenses></display-expenses>
    </v-flex>
</v-layout>
<v-divider class="my-3"></v-divider>
<v-layout>
    <v-flex>
        <h1 class="headline">Batches</h1>
        <list-batches
            v-bind:function_reset_array_columns="function_reset_array_columns"
            v-bind:function_set_array_columns="function_set_array_columns"
            v-bind:array_columns_selected="array_columns_selected"
        ></list-batches>
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
    // import ComponentListBatches from '../batches/list/component_list_batches.vue';
    import DisplayExpenses from './display-expenses.vue';
    import slug_project from '../../mixins/slug_project';
    import ListBatches from "../batches/list/list-batches";
    import {Service_App} from "../../services/service.app";
    import {update_sandbox} from "../../mixins/update_sandbox";
export default {
    mixins: [
        slug_project,
        update_sandbox,
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
        sandbox_updated() {
            Service_App.load_balance();
        },
        ...mapActions('moduleBatches', {
            'function_reset_array_columns': 'reset_array_columns_finances',
        }),
        ...mapMutations('moduleBatches', {
            'function_set_array_columns': 'set_array_columns_finances'
        }),
    },
    computed: {
        ...mapGetters('moduleBatches', {
            'array_columns_selected': 'get_array_columns_selected_finances',
        }),
    },
    created() {
        Service_App.load_balance();
    },

    components: {
        ListBatches,
        ComponentShowBalance,
        ComponentShowMoneySpent,
        ComponentShowBatches,
        // ComponentListBatches,
        DisplayExpenses,
    },
}
</script>