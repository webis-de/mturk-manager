<template>
<div>
    <v-btn
        v-bind:loading="is_downloading_csv"
        v-bind:disabled="is_downloading_csv || count_hits_to_download == 0"
        color="primary"
        v-on:click.native="download_csv"
    >
        Download data for {{ count_hits_to_download }} Batch(es)
        <v-icon right>cloud_download</v-icon>
    </v-btn>
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
        	is_downloading_csv: false,
        }
    },
    methods: {
    	download_csv: function() {
    	    Service_Batches.download({
                // batches: [3,4,5],
                batches: Object.keys(this.object_batches_selected),
                // values: ['id_worker'],
            });

    	    return;
    		// this.is_downloading_csv = true;

    		let array_header = [
    			'id_assignment',
    			'id_hit',
    			'id_worker',
    			'sandbox',
    			'creation',
    			'expiration',
    			'status_external',
    			'status_internal',
    		];
    		const array_assignments = [];
    		let is_header_set_parameters = false;
    		let is_header_set_answers = false;

    		const status_external_inverted = _.invert(STATUS_EXTERNAL);
    		const status_internal_inverted = _.invert(STATUS_INTERNAL);

    		_.forEach(this.object_batches_selected, (batch) => {
    			console.log(batch)
    			_.forEach(batch.object_hits, (hit) => {
    				const parameters = JSON.parse(hit.parameters);
    				const ordered_keys_parameters = _.orderBy(Object.keys(parameters));

    				if(is_header_set_parameters == false) {
    					array_header = _.concat(array_header, ordered_keys_parameters);
    					is_header_set_parameters = true;
    				}

	    			_.forEach(hit.object_assignments, (assignment) => {
	    				const answer_normalized = this.normalize_answer(assignment.answer);
    					const ordered_keys_answers = _.orderBy(Object.keys(answer_normalized));

	    				if(is_header_set_answers == false) {
	    					array_header = _.concat(array_header, ordered_keys_answers);
	    					is_header_set_answers = true;
	    				}

	    				const array_assignment = [];

	    				array_assignment.push(assignment.id_assignment);
	    				array_assignment.push(assignment.hit.id_hit);
	    				array_assignment.push(assignment.worker.id_worker);
	    				array_assignment.push(assignment.hit.batch.use_sandbox);
	    				array_assignment.push(assignment.hit.datetime_creation);
	    				array_assignment.push(assignment.hit.datetime_expiration);
	    				array_assignment.push(status_external_inverted[assignment.status_external]);
	    				array_assignment.push(status_internal_inverted[assignment.status_internal]);

	    				_.forEach(ordered_keys_parameters, (key) => {
	    					array_assignment.push(_.get(parameters, key, undefined));
	    				});

	    				_.forEach(ordered_keys_answers, (key) => {
	    					array_assignment.push(_.get(answer_normalized, key, undefined));
	    				});

	    				array_assignments.push(array_assignment);
	    			})
    			})
    		});

    		// filter the selected hits
    		// const hits_selected = _.filter(this.list_hits_for_csv, hit => this.set_batches_selected.has(hit[2]));
    		// console.log(hits_selected)
            const csv_string = Papa.unparse(
            {
                fields: array_header,
                data: array_assignments,
                // data: _.map(hits_selected, o => _.slice(o, 0, 2)),
            });
            let blob = new Blob([csv_string]);
            let a = window.document.createElement("a");
            a.href = window.URL.createObjectURL(blob, {type: "text/plain"});
            a.download = "filename.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
    		this.is_downloading_csv = false;
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
    computed: {
    	count_hits_to_download: function() {
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