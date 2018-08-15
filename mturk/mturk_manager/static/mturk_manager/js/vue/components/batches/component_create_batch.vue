<template>
<v-dialog
    v-model="is_creating_batch"
    persistent
    transition="slide-y-transition"
>
    <v-fab-transition slot="activator">
        <v-btn
            v-show="!is_creating_batch"
            color="pink"
            fab
            left
            bottom
            fixed
            large
            v-on:click="is_creating_batch = true"
        >
            <v-icon>add</v-icon>
        </v-btn>
    </v-fab-transition>

    <v-stepper v-show="is_creating_batch" v-model="number_step_current">
        <v-stepper-header>
            <template
                v-for="(step, index) in list_steps"
            >
                <v-stepper-step 
                    v-bind:key="`${index}_step`"
                    v-bind:complete="number_step_current > step.number" 
                    v-bind:step="step.number"
                >
                    {{ step.label }}
                </v-stepper-step>
                <v-divider
                    v-bind:key="index"
                    v-if="index != list_steps.length - 1"
                ></v-divider>
            </template>
        </v-stepper-header>
        <v-stepper-items>
            <v-stepper-content 
                v-for="step in list_steps"
                v-bind:step="step.number"
            >
                    <!-- v-bind:list_steps="list_steps" -->
                <component 
                    v-bind:is="step.component"
                    v-bind:ref="step.number"
                    v-bind:step="step_current"
                    v-on:cancel="cancel()"
                    v-on:next="next()"
                    v-on:back="back()"
                ></component>
            </v-stepper-content>
        </v-stepper-items>
    </v-stepper>
</v-dialog>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    
    import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    import ComponentStepSettings from './component_step_settings.vue';
    import ComponentStepOverview from './component_step_overview.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-create-batch',
    data () {
        return {
            is_creating_batch: false,
            number_step_current: 1,
            list_steps: [
                {
                    number: 1,
                    label: 'Upload CSV',
                    component: ComponentStepUploadCSV,

                },
                {
                    number: 2,
                    label: 'Settings',
                    component: ComponentStepSettings,

                },
                {
                    number: 3,
                    label: 'Done',
                    component: ComponentStepOverview,

                },
            ],

            data_csv: undefined,
        }
    },
    methods: {
        cancel() {
            this.is_creating_batch = false;
            this.number_step_current = 1;
            this.data_csv = undefined;
            this.$refs[1][0].reset()
        },
        next() {
            this.number_step_current += 1;
        },
        back() {
            this.number_step_current -= 1;
        },
    //     refresh_data() {
    //         this.set_show_progress_indicator(true);
    //         this.set_show_progress_indicator(true);

    //         this.sync_database().then(() => {
    //             this.set_show_progress_indicator(false);
    //         });
            
    //         this.update_balance().then(() => {
    //             this.set_show_progress_indicator(false);
    //         });
    //     },
    //     ...mapActions(['set_show_progress_indicator']),
    //     ...mapActions('moduleBatches', {
    //         'sync_database': 'sync_database', 
    //     }),
    //     ...mapActions('moduleMoney', {
    //         'update_balance': 'update_balance'
    //     }),
    // },
    // watch: {
    //     use_sandbox: function() {
    //         this.refresh_data();
    //     },
    },
    computed: {
        step_current: function() {
            return this.list_steps[this.number_step_current - 1];
        },
    //     ...mapState(['use_sandbox']),
    },
    // created: function() {
    //     this.refresh_data();
    // },

    components: {
     // ComponentShowMoneySpent,
     // ComponentShowBatches,
    },
}
</script>

<style scoped>
   div.v-dialog__content {
align-items: flex-start;
margin-top: 10vh;
} 
</style>