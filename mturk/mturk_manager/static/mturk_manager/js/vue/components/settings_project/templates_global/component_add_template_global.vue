<template>
<div>
	<v-dialog v-model="dialog">
		<v-btn 
			slot="activator" 
			color="primary"
			small
		><v-icon>add</v-icon> Add Template</v-btn>
      	<v-card>
	        <v-card-title>
	            <span class="headline">Add Global Template</span>
	            <v-spacer></v-spacer>
	            <v-btn icon v-on:click="dialog = false">
	                <v-icon>close</v-icon>
	            </v-btn>
	        </v-card-title>
	        <v-card-text>
	      		<v-form ref="form">
					<v-text-field
			            required
			            label="Name"
			  			v-bind:value="name"
			            v-on:input="name=$event; $v.name.$touch()"
		        		v-bind:error-messages="validation_errors.name"
			        ></v-text-field>
					<v-textarea
			            required
			            rows="20"
			  			v-bind:value="template"
			            v-on:input="template=$event; $v.template.$touch()"
			            label="Template"
		        		v-bind:error-messages="validation_errors.template"
			        ></v-textarea>

			        <!-- <component-form-settings-batch
			        	v-bind.sync="settings_batch"
			        ></component-form-settings-batch> -->
		    	</v-form>
			    <v-btn
			        class="ml-0"
			        color="primary"
			        v-on:click="create()"
					v-bind:disabled="$v.$invalid"
			    >Create</v-btn>
			</v-card-text>
    	</v-card>
	</v-dialog>
</div>
</template>

<script>
	// import ComponentFormSettingsBatch from './component_form_settings_batch';
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';

	import { required, minValue } from 'vuelidate/lib/validators'
	import validations from '../../../mixins/validations';
    import {Service_Templates} from "../../../services/service_templates";
export default {
    mixins: [
        validations,
    ],
    data() {
    	return {
    		name: undefined,
    		template: undefined,

			dialog: false,
    	}
    },
    watch: {
    	dialog() {
    		this.reset();
    	},
    },
    validations: {
    	name: {
    		required,
    	},
    	template: {
    		required,
    	},
    },
    methods: {
    	reset() {
    		this.name = undefined;
    		this.template = undefined;
    		this.$v.$reset();
    	},
		create() {
            if(this.$refs.form.validate()) 
            {
                Service_Templates.create({
					type_template: 'global',
    				template: {
    					name: this.name,
    					template: this.template,
    				},
    				project: this.project_current,
				}).then(() => {
    				this.$emit('created');
                    this.dialog = false;
                    this.reset();
                });
            }
		},		
		...mapActions('moduleProjects', {
			'create_template_global': 'create_template_global',
		}),
    },
    computed: {
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
	components: {
	},
}
</script>