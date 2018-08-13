<template>
    <span>
    <v-divider class="my-3"></v-divider>

        <!-- color="primary" -->
    <v-btn
        v-bind:disabled="is_disabled_back"
        flat
        v-on:click="$emit('back')"
    >Back</v-btn>

    <v-btn
        v-bind:disabled="!is_step_completed"
        color="primary"
        v-on:click="$emit('next')"
    >{{ label_submit }}</v-btn>

    <v-btn 
        flat 
        v-on:click="cancel"
    >Cancel</v-btn>
</span>
</template>

<script>
    // import { mapState, mapActions, mapGetters } from 'vuex';
    
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-create-batch-navigation',
    props: {
        reset: {
            required: false,
            type: Function,
        },
        is_step_completed: {
            required: false,
            type: Boolean,
            default: true,
        },
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
    computed: {
        label_submit() {
            if(this.step.number == 3)
            {
                return 'Submit';
            } else {
                return 'Continue';
            }
        },
        is_disabled_back() {
            return this.step.number == 1;
        },
    },
    methods: {
        cancel() {
            if(this.reset != null) 
            {
                this.reset();
            }

            this.$emit('cancel');
        },
    },
    components: {
      // ComponentCreateBatchNavigation,
    }
}
</script>