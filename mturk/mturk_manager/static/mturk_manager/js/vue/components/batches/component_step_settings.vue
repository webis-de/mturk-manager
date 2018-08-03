<template>
    <span>
awdawd
    <!-- <v-divider class="my-3"></v-divider>

    <v-btn
        color="primary"
        v-on:click="$emit('next')"
    >
        Continue
    </v-btn>

    <v-btn flat v-on:click="cancel">Cancel</v-btn> -->

        <!-- v-bind:reset="reset" -->
        <!-- v-bind:list_steps="list_steps" -->
    <component-create-batch-navigation
        v-bind:step="step"
        v-on:cancel="$emit('cancel')"
        v-on:next="$emit('next')"
        v-on:back="$emit('back')"
    ></component-create-batch-navigation>
</span>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import ComponentCreateBatchNavigation from './component_create_batch_navigation.vue';
    
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-step-settings',
    props: {
        step: {
            required: true,
            type: Object,
        },
        // list_steps: {
        //     required: true,
        //     type: Array,
        // },
    },
    data () {
        return {
        }
    },
    methods: {
        reset() {

        },
    },
    components: {
      ComponentCreateBatchNavigation,
    }
}
</script>