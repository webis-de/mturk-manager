<template>
<span>
    <v-layout>
        <v-flex xs1>
            <upload-btn
                :fileChangedCallback="file_changed"
                title="Upload CSV"
                :loading="true"
            ></upload-btn>
        </v-flex>
        <v-flex>
             {{ tmp_name_file }}
        </v-flex>
    </v-layout>
    <template v-if="is_valid_csv">
        <v-divider class="my-3"></v-divider>
        <v-list 
            
            subheader
        >
            <v-subheader>Statistics</v-subheader>
            <v-list-tile>
                <v-layout>
                    <v-flex xs1>
                        Is Valid:  
                    </v-flex>
                    <v-flex xs1 class="text-xs-center">
                        <v-icon color="success">check</v-icon>
                    </v-flex>
                </v-layout>       
            </v-list-tile>
            <v-list-tile>
                <v-layout>
                    <v-flex xs1>
                        Number of variables:  
                    </v-flex>
                    <v-flex xs1 class="text-xs-center">
                        {{ get_variables.length }} 

                        <v-tooltip top>
                            <v-icon
                                slot="activator"
                            >info</v-icon>
                            <span>{{ get_variables.join(', ') }}</span>
                        </v-tooltip>  

                    </v-flex>
                </v-layout>       
            </v-list-tile>
            <v-list-tile>
                <v-layout>
                    <v-flex xs1>
                        Number of HITs: 
                    </v-flex>
                    <v-flex xs1 class="text-xs-center">
                        {{ count_hits }}   
                    </v-flex>
                </v-layout>     
            </v-list-tile>
        </v-list>
    </template>
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
        v-bind:is_step_completed="is_step_completed"
        v-bind:reset="reset"
        v-on:cancel="$emit('cancel')"
        v-on:next="$emit('next')"
        v-on:back="$emit('back')"
    ></component-create-batch-navigation>

    <v-dialog
      v-model="is_parsing_csv"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="primary"
        dark
      >
        <v-card-text>
          Parsing CSV...
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
</span>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import UploadBtn from 'vuetify-upload-button';
    import ComponentCreateBatchNavigation from './component_create_batch_navigation.vue';

    import Papa from 'papaparse';
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-step-upload-csv',
    props: {
        step: {
            required: true,
            type: Object,
        },
    },
    data () {
        return {
            file_csv: null,
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
                    this.is_parsing_csv = false;
                    this.set_csv_parsed(results);
                }
            });
        },
        reset() {
            this.file_csv = null;
            this.is_parsing_csv = false;
            this.set_csv_parsed(undefined);
        },
        ...mapMutations('moduleBatches', {
            'set_csv_parsed': 'set_csv_parsed',
        }),
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
                return this.get_object_csv_parsed.data;
            }
            return null;
        },
        is_valid_csv() {
            if(this.get_object_csv_parsed == null) 
            {
                return false;
            } else {
                return this.get_object_csv_parsed.errors.length == 0;
            }
        },
        is_step_completed() {
            return this.is_valid_csv;
        },
        ...mapGetters('moduleBatches', {
            'get_object_csv_parsed': 'get_object_csv_parsed',
        }),
    },
    components: {
      UploadBtn,
      ComponentCreateBatchNavigation,
    }
}
</script>

<style scoped>
    input[type=file] {
        position: absolute;
        left: -99999px;
    }
</style>