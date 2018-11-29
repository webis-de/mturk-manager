import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
export default {
	data() {
		return {
            pagination: { rowsPerPage:25 },
		}
	},
    watch: {
    },
	methods: {
        toggleAll(list_selected, list_items, pagination=undefined, props, show_only_submitted_assignments) {
            if(pagination)
            {
                list_items = _.orderBy(list_items, pagination.sortBy, pagination.descending ? 'desc' : 'asc');
                if(show_only_submitted_assignments)
                {
                    list_items = list_items.filter(e => e.status_external === null);
                }

                if(props.all)
                {
                    list_selected = [];
                } else {
                    list_selected = list_items.slice((pagination.page - 1) * pagination.rowsPerPage, pagination.page * pagination.rowsPerPage);
                }
                _.forEach(list_selected, (e) => {
                    // console.log('e', e.id_assignment);
                });
                return list_selected
            }

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