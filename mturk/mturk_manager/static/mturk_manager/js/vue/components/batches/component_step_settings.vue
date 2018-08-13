<template>
    <span>
        <!-- {{valid}} -->
    <v-form v-model="valid" lazy-validation>
        {{get_object_project}}
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
            v-model="lifetime"
            label="Lifetime"
            v-bind:rules="rules_lifetime"
            v-bind:hint="DESCRIPTIONS.LIFETIME_HIT"
            min="1"
            suffix="s"
        ></v-text-field>

        <v-text-field
            required
            type="number"
            v-model="duration"
            label="Duration"
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

        <!-- <v-text-field
            type="number"
            v-model="name"
            :rules="nameRules"
            :counter="10"
            label="Name"
            required
        ></v-text-field> -->
    </v-form>
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
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import ComponentCreateBatchNavigation from './component_create_batch_navigation.vue';
    import { VALIDATIONS, DESCRIPTIONS } from '../../classes/enums';
    
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
            valid: false,
            title: '',
            rules_title: [
                VALIDATIONS.REQUIRED,
            ],
            description: '',
            rules_description: [
                VALIDATIONS.REQUIRED,
            ],
            reward: 0,
            rules_reward: [
                VALIDATIONS.REQUIRED,
            ],
            assignments_max: 1,
            rules_assignments_max: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            lifetime: 1,
            rules_lifetime: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            duration: 1,
            rules_duration: [
                VALIDATIONS.REQUIRED,
                VALIDATIONS.POSITIVE,
            ],
            keywords: [],
            rules_keywords: [
            ],

            DESCRIPTIONS: DESCRIPTIONS,
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
        ...mapGetters('moduleProjects', {
            'get_object_project': 'get_object_project',
        }),
    },
    components: {
      ComponentCreateBatchNavigation,
    }
}
</script>