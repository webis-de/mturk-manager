<template>
<div>
    <v-tooltip top v-bind:disabled="is_valid_selection">
        <v-btn
            slot="activator"
            v-bind:loading="is_downloading_csv"
            v-bind:disabled="is_downloading_csv || count_batches_to_download === 0 || !is_valid_selection"
            color="primary"
            v-on:click="dialog = true"
        >
            <!--<template v-if="is_valid_selection">-->
                Download {{ count_batches_to_download }} Batch(es)
                <v-icon right>cloud_download</v-icon>
            <!--</template>-->
            <!--<template v-else>-->
                <!--Selected batches have an incompatible Structure-->
            <!--</template>-->
        </v-btn>
        Selected batches have an incompatible Structure
    </v-tooltip>
	<v-dialog
		v-model="dialog"
        max-width="80%"
	>
        <v-card>
          	<v-card-title>
          		Download Batch(es)
          	</v-card-title>
          	<v-card-text>
				<v-layout>
					<v-flex>
						Include the following values:
						<v-treeview
							v-model="headers_selected"
							v-bind:items="array_headers"
							selectable
						></v-treeview>
					</v-flex>
				</v-layout>
			    <v-layout row>
			        <v-flex>
            	<v-btn
            		color="primary"
            		v-on:click="download_csv"
        		>Download {{ count_batches_to_download }} Batch(es)</v-btn>
					</v-flex>
				</v-layout>
	            <!-- append-icon="clear"
	            v-on:click:append="limit = 0" -->
          	</v-card-text>
        </v-card>
    </v-dialog>
</div>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
    import Papa from 'papaparse';
    import {STATUS_EXTERNAL, STATUS_INTERNAL} from "../../classes/enums";
    import {Service_Batches} from "../../services/service_batches";
export default {
    name: 'component-download-batch',
    data() {
        return {
            dialog: false,
        	is_downloading_csv: false,
            is_valid_selection: true,

			array_headers: [],
			headers_selected: [],
        }
    },
    methods: {
    	download_csv: function() {
            this.is_downloading_csv = true;

			const headers_selected = [];
			console.log('this.headers_selected', this.headers_selected);
			_.forEach(this.headers_selected, (value) => {
			   if(_.isNumber(value)) return true;

			   headers_selected.push(value.split('__')[1]);
            });

    	    Service_Batches.download({
                batches: Object.keys(this.object_batches_selected),
                values: headers_selected,
            }).then(() => {
				this.headers_selected = [0, 1, 2];
                this.dialog = false;
                this.is_downloading_csv = false;
            });

            return;
    	},
    	normalize_answer(answer_raw) {
			let answer = {};
			if(Array.isArray(answer_raw['QuestionFormAnswers']['Answer']))
			{
				_.forEach(answer_raw['QuestionFormAnswers']['Answer'], function(value) {
					answer[value['QuestionIdentifier']] = value['FreeText'];
				});
			} else {
				answer[answer_raw['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = answer_raw['QuestionFormAnswers']['Answer']['FreeText'];
			}

			return answer;
		}
    },
    watch: {
        dialog() {
			this.headers_selected = [0, 1, 2];
		},
        object_batches_selected() {
			this.headers_selected = [0, 1, 2];

            if(_.size(this.object_batches_selected) === 0) {
                this.is_valid_selection = true;
                return;
            }

            this.is_downloading_csv = true;
            Service_Batches.get_download_info({
                batches: Object.keys(this.object_batches_selected),
            }).then((response) => {
                this.is_valid_selection = response.data.is_valid;
                this.is_downloading_csv = false;

                const array_headers = [];
                if(_.size(response.data.set_builtin) > 0) {
                    array_headers.push({
					    id: 0,
					    name: 'builtin',
						children: [],
					});
				}
                if(_.size(response.data.set_parameters) > 0) {
                    array_headers.push({
					    id: 1,
					    name: 'parameters',
						children: [],
					});
				}
                if(_.size(response.data.set_answer) > 0) {
                    array_headers.push({
					    id: 2,
					    name: 'answer',
						children: [],
					});
				}

				_.forEach(response.data.set_builtin, (value) => {
				   	array_headers[0].children.push({
						id: `${0}__${value}`,
						name: value
					});
				});

				_.forEach(response.data.set_parameters, (value, index) => {
				   	array_headers[1].children.push({
						id: `${1}__${index}`,
						name: index
					});
				});

				_.forEach(response.data.set_answer, (value) => {
				   	array_headers[2].children.push({
						id: `${1}__${value}`,
						name: value
					});
				});

				this.headers_selected = [0, 1, 2];

                this.array_headers = array_headers;
            });

        }
    },
    computed: {
    	count_batches_to_download: function() {
    		// if(_.size(this.array_batches_selected) == 0) {
    		// 	return 'all';
    		// } else {

        	return _.size(this.object_batches_selected);
            	// return _.sumBy(this.batches_selected, 'hits.length');
    		// }
    	},
        ...mapGetters('moduleBatches', {
            'object_batches_selected': 'get_object_batches_selected',
        }),

    },
    components: {

    },
}
</script>

<style scoped>
</style>