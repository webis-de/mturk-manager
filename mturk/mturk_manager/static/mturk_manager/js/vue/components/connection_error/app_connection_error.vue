<template>
<v-container>
	<v-layout wrap>
	    <v-flex class="text-xs-center">
			<h3 class="display-1">Connection Error</h3>
			<p>
				No connection to the database could be established!
			</p>
            <v-btn 
                block 
                color="primary"
                v-on:click="retry" 
            >
                Retry
            </v-btn>
		</v-flex>
	</v-layout>
</v-container>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
	import axios from 'axios';

    import { required, minLength, between } from 'vuelidate/lib/validators'
export default {
    name: 'component-connection-error',
    data () {
        return {
        }
    },
    methods: {
        async retry() {
            this.set_show_progress_indicator(true);
            if(await this.init())
            {
                this.$router.push({name: 'dashboard'});
            } else {
                console.log('still error')
            }
            // this.set_show_progress_indicator(false);
            // console.log('dwad')
        },
        ...mapActions([
            'init', 
            'set_show_progress_indicator', 
        ]),
    },
    computed: {
    },
    created: function() {
    },
    components: {
    },
}
</script>