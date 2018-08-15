<template>
<v-layout wrap>
    <v-flex>
        <v-layout wrap>
            <v-flex xs6 pr-3>
                <!-- {{valid}} -->
                <v-form v-model="valid" lazy-validation>
                    <!-- {{project_current}} -->
                    <v-text-field
                        required
                        v-model="title"
                        label="Title"
                        v-bind:rules="rules_title"
                        v-bind:hint="DESCRIPTIONS.TITLE_HIT"
                    ></v-text-field>

                    <v-text-field
                        required
                        v-model="description"
                        label="Description"
                        v-bind:rules="rules_description"
                        v-bind:hint="DESCRIPTIONS.DESCRIPTION_HIT"
                    ></v-text-field>

                    <v-text-field
                        required
                        type="number"
                        v-model="reward"
                        step="0.01"
                        label="Reward"
                        v-bind:rules="rules_description"
                        v-bind:hint="DESCRIPTIONS.REWARD_HIT"
                        append-icon="attach_money"
                    ></v-text-field>

                    <v-text-field
                        required
                        type="number"
                        v-model="assignments_max"
                        label="Number of Assignments"
                        v-bind:rules="rules_assignments_max"
                        v-bind:hint="DESCRIPTIONS.ASSIGNEMENTS_MAX_HIT"
                        min="1"
                    ></v-text-field>

                    <v-text-field
                        required
                        type="number"
                        v-bind:label="format_duration('Lifetime', lifetime)"
                        v-model="lifetime"
                        v-bind:rules="rules_lifetime"
                        v-bind:hint="DESCRIPTIONS.LIFETIME_HIT"
                        min="1"
                        suffix="s"
                    ></v-text-field>

                    <v-text-field
                        required
                        type="number"
                        v-model="duration"
                        v-bind:label="format_duration('Duration', duration)"
                        v-bind:rules="rules_duration"
                        v-bind:hint="DESCRIPTIONS.DURATION_HIT"
                        min="1"
                        suffix="s"
                    ></v-text-field>
                    <v-combobox
                        v-model="keywords"
                        v-bind:rules="rules_keywords"
                        label="Keywords (Separated with TAB)"
                        chips
                        clearable
                        v-bind:hint="DESCRIPTIONS.KEYWORDS_HIT"
                        multiple
                        counter
                        append-icon
                    >
                        <template slot="selection" slot-scope="data">
                            <v-chip
                                v-bind:selected="data.selected"
                                close
                                @input="remove(data.item)"
                            >
                                <strong>{{ data.item }}</strong>&nbsp;
                            </v-chip>
                        </template>
                    </v-combobox>
                </v-form>
            </v-flex>
            <v-flex xs6 pl-3>
                <h2>Summary</h2>
                <p>
                    The HITs will be <b>approximately</b> available until {{ format_lifetime_absolute }}.
                </p>
                <p>
                    This batch will cost <component-display-money v-bind:amount="costs_total_with_fee"></component-display-money> (without Amazon's fees: <component-display-money v-bind:amount="costs_total_without_fee"></component-display-money>).
                </p>
            </v-flex>
        </v-layout>
        <v-layout wrap>
            <v-flex>
                <component-create-batch-navigation
                    v-bind:step="step"
                    v-on:cancel="$emit('cancel')"
                    v-on:next="$emit('next')"
                    v-on:back="$emit('back')"
                ></component-create-batch-navigation>
            </v-flex>
        </v-layout>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import ComponentDisplayMoney from '..//component-display-money.vue';
    import ComponentCreateBatchNavigation from './component_create_batch_navigation.vue';
    import settings_batch from '../../mixins/settings_batch';
    
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    mixins: [
        settings_batch,
    ],
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
            current_time_ms: Date.now() ,
        }
    },
    methods: {
        remove(item) {
            this.keywords.splice(this.keywords.indexOf(item), 1)
            this.keywords = [...this.keywords]
        },
        reset() {
        },
    },
    computed: {
                // if(batch.count_assignments_per_hit < 10) {
                //     batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.2;
                // } else {
                //     batch.money_spent_max_with_fee = batch.money_spent_max_without_fee * 1.4;
                // }
        costs_total_without_fee() {
            console.log(this.object_csv_parsed)
            const reward = parseFloat(this.reward);
            if(this.object_csv_parsed != undefined)
            {
                return reward * this.assignments_max * this.object_csv_parsed.data.length;
            } else {
                return reward * this.assignments_max
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
            const lifetime_absolute = this.current_time_ms + this.lifetime * 1000.0;
            return new Date(lifetime_absolute).toLocaleString();
        },
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
        ...mapGetters('moduleBatches', {
            'object_csv_parsed': 'get_object_csv_parsed',
        }),
    },
    created() {
        setInterval(() => {this.current_time_ms = Date.now()}, 1000);
    },
    components: {
      ComponentCreateBatchNavigation,
      ComponentDisplayMoney,
    }
}
</script>