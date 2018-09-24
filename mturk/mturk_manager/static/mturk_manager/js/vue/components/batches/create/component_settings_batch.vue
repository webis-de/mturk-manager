<template>
<v-layout wrap>
    <v-flex>
        <!-- {{valid}} -->
        <v-form ref="form" v-model="valid" lazy-validation>
            <h2>General Settings</h2>
            <!-- {{project_current}} -->
            <v-text-field
                required
                v-model="project.title"
                label="Title"
                v-bind:rules="rules_title"
                v-bind:hint="DESCRIPTIONS.TITLE_HIT"
            ></v-text-field>

            <v-text-field
                required
                v-model="project.description"
                label="Description"
                v-bind:rules="rules_description"
                v-bind:hint="DESCRIPTIONS.DESCRIPTION_HIT"
            ></v-text-field>

            <v-text-field
                required
                type="number"
                v-model="project.reward"
                step="0.01"
                label="Reward"
                v-bind:rules="rules_description"
                v-bind:hint="DESCRIPTIONS.REWARD_HIT"
                append-icon="attach_money"
            ></v-text-field>

            <v-text-field
                required
                type="number"
                v-model="project.assignments_max"
                label="Number of Assignments"
                v-bind:rules="rules_assignments_max"
                v-bind:hint="DESCRIPTIONS.ASSIGNEMENTS_MAX_HIT"
                min="1"
            ></v-text-field>

            <v-text-field
                required
                type="number"
                v-bind:label="format_duration('Lifetime', project.lifetime)"
                v-model="project.lifetime"
                v-bind:rules="rules_lifetime"
                v-bind:hint="DESCRIPTIONS.LIFETIME_HIT"
                min="1"
                suffix="s"
            ></v-text-field>

            <v-text-field
                required
                type="number"
                v-model="project.duration"
                v-bind:label="format_duration('Duration', project.duration)"
                v-bind:rules="rules_duration"
                v-bind:hint="DESCRIPTIONS.DURATION_HIT"
                min="1"
                suffix="s"
            ></v-text-field>    

            <v-select
                v-model="project.template"
                v-bind:items="project.templates"
                v-bind:rules="rules_template_worker"
                label="Worker Template"
                item-text="name"
                item-value="id"
            ></v-select>

            <v-switch
                v-bind:label="`Limit Block and Project Block for Workers (${project.block_workers ? 'enabled': 'disabled'})`"
                v-model="project.block_workers"
            ></v-switch>

            <v-combobox
                v-model="project.keywords"
                v-bind:rules="rules_keywords"
                label="Keywords (Separated with TAB)"
                v-bind:hint="DESCRIPTIONS.KEYWORDS_HIT"

                hide-selected
                chips
                clearable
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
                        <strong>{{ data.item.text != undefined ? data.item.text : data.item }}</strong>&nbsp;
                    </v-chip>
                </template>
            </v-combobox>
            
            <v-divider class="my-3"></v-divider>
            <h2>Qualifications</h2>
            <v-switch
                v-bind:label="`Contains Adult Content`"
                v-model="project.has_content_adult"
            ></v-switch>

            <v-text-field
                required
                type="number"
                v-model.number="project.qualification_assignments_approved"
                step="1"
                max="100"
                min="0"
                label="Approved Assignments"
                append-icon="%"
            ></v-text-field>

            <v-text-field
                required
                type="number"
                v-model.number="project.qualification_hits_approved"
                step="1"
                min="0"
                label="Approved HITs"
            ></v-text-field>

            <v-combobox
                v-model="project.qualification_locale"
                label="Locale (Separated with TAB)"
                hide-selected
                chips
                clearable
                multiple
                counter
                append-icon
            >
                <template slot="selection" slot-scope="data">
                    <v-chip
                        v-bind:selected="data.selected"
                        close
                        @input="remove_qualification_locale(data.item)"
                    >
                        <strong>{{ data.item.text != undefined ? data.item.text : data.item }}</strong>&nbsp;
                    </v-chip>
                </template>
            </v-combobox>
        </v-form>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import settings_batch from '../../../mixins/settings_batch';
    
    // import ComponentStepUploadCSV from './component_step_upload_csv.vue';
    // import ComponentShowMoneySpent from './component-show-money-spent.vue';
    // import ComponentShowBatches from './component-show-batches.vue';
export default {
    mixins: [
        settings_batch,
    ],
    name: 'component-settings-batch',
    props: {
        // project: {
        //     required: true,
        // },
    },
    data () {
        return {
        }
    },
    methods: {
        ...mapMutations('moduleBatches', {
            'set_component_form': 'set_component_form',
        }),
    },
    computed: {
    },
    mounted() {
        this.set_component_form(this.$refs.form)
    },
    components: {
    }
}
</script>