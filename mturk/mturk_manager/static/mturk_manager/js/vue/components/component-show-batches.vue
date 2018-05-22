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
		disable-initial-sort
		expand
	>
		 <template slot="items" slot-scope="props">
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
		Download CSV
      	<v-icon right>cloud_download</v-icon>
    </v-btn>
</div>
</template>

<script> 
    import { mapState, mapGetters, mapActions } from 'vuex';
    import ComponentDisplayMoney from './component-display-money.vue';
	import axios from 'axios';
	import Papa from 'papaparse';

export default {
    name: 'component-show-batches',
    data () {
        return {
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
        ...mapGetters(['list_batches', 'list_hits_for_csv']),
        ...mapState(['url_download_csv']),
    },
    methods: {
    	download_csv: function() {
    		this.is_downloading_csv = true;

            const csv_string = Papa.unparse(
            {
                fields: ['id_hit', 'costs'],
                data: this.list_hits_for_csv,
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