<template>
<div>
	<h1>Batch Settings</h1>
	<v-form v-model="valid" lazy-validation>
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
            v-bind:label="format_duration('Lifetime', lifetime)"
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

        <!-- <v-text-field
            type="number"
            v-model="name"
            :rules="nameRules"
            :counter="10"
            label="Name"
            required
        ></v-text-field> -->
    </v-form>
</div>
</template>

<script>
	import settings_batch from '../../mixins/settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
    mixins: [
        settings_batch,
    ],
	name: 'component_settings_batch',
	data () {
		return {
		}
	},
	methods: {
	},
    computed: {
    },
}
</script>

<style scoped>
</style>