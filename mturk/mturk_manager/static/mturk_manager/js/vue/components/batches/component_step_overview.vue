<template>
<span>
    
    <!-- {{data_csv}} -->
    <!-- <v-divider class="my-3"></v-divider> -->
    <!-- <v-btn
        color="primary"
        v-on:click="$emit('next')"
        v-bind:disabled="!is_step_completed"
    >
        Continue
    </v-btn>
    <v-btn flat v-on:click="cancel">Cancel</v-btn> -->
        <!-- v-bind:list_steps="list_steps" -->
    <component-create-batch-navigation
        v-bind:step="step"
        v-bind:reset="reset"
        v-on:cancel="$emit('cancel')"
        v-on:next="$emit('next')"
        v-on:back="$emit('back')"
    ></component-create-batch-navigation>
</span>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import UploadBtn from 'vuetify-upload-button';
    import ComponentCreateBatchNavigation from './component_create_batch_navigation.vue';

    import Papa from 'papaparse';
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-step-overview',
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
            file_csv: null,
            parsed_csv: null,
            is_parsing_csv: false,
        }
    },
    methods: {
        file_changed(file) {
            this.file_csv = file;

            if(file == null) 
            {
                this.reset();
                return;
            };

            this.is_parsing_csv = true;
            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: (results, file) => {
                    this.parsed_csv = results;
                    console.log(this.parsed_csv);
                    this.is_parsing_csv = false;
                }
            });
        },
        reset() {
            this.file_csv = null;
            this.parsed_csv = null;
            this.is_parsing_csv = false;
        },
    },
    computed: {
        tmp_name_file() {
            if(this.file_csv != null)
            {
                return this.file_csv.name;
            } 
            return null;
        },
        count_hits() {
            if(this.is_valid_csv)
            {
                return this.data_csv.length;
            }
            return null;
        },
        get_variables() {
            if(this.is_valid_csv)
            {
                return Object.keys(this.data_csv[0]);
            }
            return null;
        },
        data_csv() {
            if(this.is_valid_csv) 
            {
                return this.parsed_csv.data;
            }
            return null;
        },
        is_valid_csv() {
            if(this.parsed_csv == null) 
            {
                return false;
            } else {
                return this.parsed_csv.errors.length == 0;
            }
        },
        is_step_completed() {
            return this.is_valid_csv;
        },
    },
    components: {
      UploadBtn,
      ComponentCreateBatchNavigation,
    }
}
</script>

<style scoped>
    
</style>