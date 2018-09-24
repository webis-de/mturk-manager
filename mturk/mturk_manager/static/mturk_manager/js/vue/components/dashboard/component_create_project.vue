<template>
<v-layout wrap>
    <v-flex class="text-xs-center">
		<v-layout wrap>
			<v-flex>
				<span class="headline">Create New Project</span>
			</v-flex>
		</v-layout>
		<!-- {{$v}} -->
		<v-layout wrap>
			<v-spacer></v-spacer>
			<v-flex xs3>
		        	<!-- v-model.trim="$v.name.$model" -->
		        <v-text-field
  					v-bind:value="name"
  					v-on:input="update_name($event); name_instant = $event"      	
		        	label="Name"
		        	v-bind:error-messages="errors"
		        	v-bind:loading="$v.$pending"
		        ></v-text-field>
			</v-flex>
			<v-flex shrink>
				<v-btn 
					v-on:click="create_project(name)"
					color="primary"
					v-bind:disabled="$v.pending || $v.$invalid || name_instant.trim() == ''"
				>Create</v-btn>
			</v-flex>
			<v-spacer></v-spacer>
		</v-layout>
	</v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
	import axios from 'axios';

    import { required, minLength, between } from 'vuelidate/lib/validators'
export default {

    name: 'component-create-project',

    data () {
        return {
        	name: '',
        	// name: undefined,
        	name_instant: '',
        	// rules: [
        	// 	this.check_uniqueness,
        	// ],
        }
    },
    computed: {
      errors () {
        const errors = [];
        if(!this.$v.name.$dirty || this.$v.$pending)
        {
        	return errors;
		}

        if(this.$v.name.required == false)
        {
        	errors.push('Required!');
        }
        if(this.$v.name.is_unique == false)
        {
        	errors.push('Name has to be unique!');
        }

        return errors;
      },
    },
    methods: {
    	update_name: _.debounce(function(value) {
    		this.name = value.trim();
    		this.$v.name.$touch();
    	}, 500),
        ...mapActions('moduleProjects', {
            'validate_name': 'validate_name',
            'create_project': 'create_project',
        }),
    },
    validations: {
    	name: {
    		required,
      // 		minLength: minLength(4),
      		async is_unique(name) {
      			if(name === '' || name == undefined) return true;

      			let response = await this.validate_name(name);
      			console.log(response.data)
      			return response.data;
      		}
    	}
    },
    created: function() {
    },
    components: {
    },
}
</script>