<template>
<div>
	<h1>Batches</h1>

      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>

	<v-data-table
		v-bind:items="list_batches"
		v-bind:headers="list_headers"
		v-bind:search="search"
		v-model="batches_selected"
		disable-initial-sort
	 	select-all
		expand
		v-bind:pagination.sync="pagination"
	>
		 <template slot="items" slot-scope="props">
			<td>
				<v-checkbox
					v-model="props.selected"
					primary
					hide-details
				></v-checkbox>
			</td>
			<td>{{ props.item.id }}</td>
			<!-- <td>{{ props.item.id_hit }}</td> -->
			<!-- <td>{{ props.item.id_assigment }}</td> -->
			<td>{{ props.item.datetime_creation.toLocaleString() }}</td>
			<!-- <td>{{ props.item.count_assignments }}</td> -->
			<td class="text-xs-right"><component-display-money v-bind:amount="props.item.money_spent"></component-display-money></td>
		</template>
		 <!-- <template slot="expand" slot-scope="props"> -->
	</v-data-table>

	<v-btn
		:loading="is_downloading_csv"
		:disabled="is_downloading_csv"
		color="primary"
		@click.native="download_csv"
	>
		Download CSV for {{ count_hits_to_download }} HITs
      	<v-icon right>cloud_download</v-icon>
    </v-btn>
</div>
</template>

<script> 
    import { mapState, mapGetters, mapActions } from 'vuex';
    import ComponentDisplayMoney from './component-display-money.vue';
	import axios from 'axios';
	import Papa from 'papaparse';
	import _ from 'lodash';

export default {
    name: 'component-show-batches',
    data () {
        return {
        	// set initial number of rows per page
		    pagination: {
		      rowsPerPage: 10,
		    },
        	batches_selected: [],
        	is_downloading_csv: false,
        	search: '',
        	list_headers: [
        		{
					text: 'ID',
					value: 'id',
				},
    //     		{
				// 	text: 'HIT',
				// 	value: 'id_hit',
				// },
    //     		{
				// 	text: 'Assignment',
				// 	value: 'id_assignment',
				// },
        		{
					text: 'created at',
					value: 'datetime_creation',
				},
        		{
					text: 'costs',
					value: 'money_spent',
					align: 'right'
				},
    //     		{
				// 	text: '#assignments',
				// 	value: 'count_assignments',
				// },
        	]
        }
    },
    computed: {
    	set_batches_selected: function() {
    		if(this.batches_selected.length == 0) {
    			return new Set(_.map(this.list_batches, o => o.id));
    		} else {
    			return new Set(_.map(this.batches_selected, o => o.id));
    		}
    	},
    	count_hits_to_download: function() {
    		if(this.batches_selected.length == 0) {
    			return 'all';
    		} else {
            	return _.sumBy(this.batches_selected, 'hits.length');
    		}
    	},
        ...mapGetters(['list_batches', 'list_hits_for_csv']),
    },
    methods: {
    	download_csv: function() {
    		this.is_downloading_csv = true;

    		// filter the selected hits
    		const hits_selected = _.filter(this.list_hits_for_csv, hit => this.set_batches_selected.has(hit[2]));

            const csv_string = Papa.unparse(
            {
                fields: ['id_hit', 'costs', 'id_batch'],
                data: _.map(hits_selected, o => _.slice(o, 0, 2)),
            });
            var blob = new Blob([csv_string]);
            var a = window.document.createElement("a");
            a.href = window.URL.createObjectURL(blob, {type: "text/plain"});
            a.download = "filename.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
    		this.is_downloading_csv = false;
    	}
    },
    components: {
        ComponentDisplayMoney,
    },
}
</script>

<style lang="scss" scoped>
</style>