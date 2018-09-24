<template>
<v-layout wrap>
    <v-flex>
        <v-list subheader>
            <v-subheader><h2>Summary</h2></v-subheader>
            <v-list-tile>
                <v-layout>
                    <v-flex xs3>
                        Valid CSV:  
                    </v-flex>
                    <v-flex>
                        <template v-if="is_valid_csv">
                            <v-icon color="success">check</v-icon>
                        </template>
                        <template v-else>
                            None
                        </template>
                    </v-flex>
                </v-layout>       
            </v-list-tile>

            <v-list-tile>
                <v-layout>
                    <v-flex xs3>
                        Number of variables:  
                    </v-flex>
                    <v-flex>
                        <template v-if="is_valid_csv">
                            {{ get_variables.length }} 

                            <v-tooltip top>
                                <v-icon
                                    slot="activator"
                                >info</v-icon>
                                <span>{{ get_variables.join(', ') }}</span>
                            </v-tooltip> 
                        </template>
                        <template v-else>
                            None
                        </template> 
                    </v-flex>
                </v-layout>       
            </v-list-tile>

            <v-list-tile>
                <v-layout>
                    <v-flex xs3>
                        Number of HITs: 
                    </v-flex>
                    <v-flex>
                        <template v-if="is_valid_csv">
                            {{ count_hits }}   
                        </template>
                        <template v-else>
                            None
                        </template> 
                    </v-flex>
                </v-layout>     
            </v-list-tile>

            <v-list-tile>
                <v-layout>
                    <v-flex xs3>
                        Available until: 
                    </v-flex>
                    <v-flex>
                        {{ format_lifetime_absolute }} ({{ lifetime_formatted }}) 
                    </v-flex>
                </v-layout>     
            </v-list-tile>

            <v-list-tile>
                <v-layout>
                    <v-flex xs3>
                        Costs: 
                    </v-flex>
                    <v-flex>
                        <template v-if="is_valid_csv">
                            <component-display-money v-bind:amount="costs_total_with_fee"></component-display-money> 
                            (without Amazon's fees: <component-display-money v-bind:amount="costs_total_without_fee"></component-display-money>) 
                        </template>
                        <template v-else>
                            None
                        </template> 
                    </v-flex>
                </v-layout>     
            </v-list-tile>
        </v-list>
        
    </v-flex>
</v-layout>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import Project from '../../../classes/project';
    import ComponentDisplayMoney from '../../component-display-money.vue';
    import humanizeDuration from 'humanize-duration';

    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    name: 'component-overview',
    props: {
        project: {
            required: true,
            type: Project|undefined,
        },
    },
    data () {
        return {
            current_time_ms: Date.now(),
        }
    },
    methods: {
    },
    computed: {
        lifetime_formatted() {
            if(this.project == undefined) return undefined;

            return humanizeDuration(this.project.lifetime * 1000)
        },
        costs_total_without_fee() {
            if(this.project == undefined) return 0;

            console.log(this.object_csv_parsed)
            const reward = parseFloat(this.project.reward);
            if(this.object_csv_parsed != undefined)
            {
                return reward * this.project.assignments_max * this.object_csv_parsed.data.length;
            } else {
                return reward * this.project.assignments_max
            }
        },
        costs_total_with_fee() {
            let costs_with_fee = undefined;

            if(this.assignments_max < 10)
            {
                costs_with_fee = this.costs_total_without_fee * 1.2;
            } else {
                costs_with_fee = this.costs_total_without_fee * 1.4;
            }

            return costs_with_fee;
        },
        format_lifetime_absolute() {
            if(this.project == undefined) return undefined;

            const lifetime_absolute = this.current_time_ms + this.project.lifetime * 1000.0;
            return new Date(lifetime_absolute).toLocaleString();
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

            return [];
        },
        data_csv() {
            if(this.is_valid_csv) 
            {
                return this.object_csv_parsed.data;
            }
            return null;
        },
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
        ...mapGetters('moduleBatches', {
            'object_csv_parsed': 'get_object_csv_parsed',
            'is_valid_csv': 'is_valid_csv',
        }),
    },
    created() {
        setInterval(() => {this.current_time_ms = Date.now()}, 1000);
    },
    components: {
      ComponentDisplayMoney,
    }
}
</script>

<style scoped>
    
</style>