import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
export default {
	data() {
		return {
            pagination: { rowsPerPage:25 },
		}
	},
    watch: {
    },
	methods: {
        toggleAll(list_selected, list_items) {
            if(list_selected.length)
            {
                list_selected = [];
            } else {
                list_selected = list_items.slice();
            }
            return list_selected;
            // if (this.workers_selected.length) this.workers_selected = []
            // else this.workers_selected = this.list_workers.slice()
        },
        changeSort(column) {
            if(this.pagination.sortBy === column) 
            {
                this.pagination.descending = !this.pagination.descending;
            } else {
                this.pagination.sortBy = column;
                this.pagination.descending = false;
            }
        },
	},
    created() {
    },
    computed: {
    },
}