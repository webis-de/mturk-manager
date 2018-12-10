import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
import _ from 'lodash';
import {external_pagination} from "./external_pagination";
export const table = {
    watch: {
        filters: {
            handler() {
                this.load_page();
            },
            deep: true,
        },
    },
    computed: {
        array_page() {
            let array_items = this.array_items();

            return array_items === null ? [] : array_items;
        },
	    is_page_selected() {
	        let is_page_selected = true;

	        if(_.size(this.array_page) === 0) {return false;}

	        _.forEach(this.array_page, (item) => {
                if(!_.has(this.object_items_selected, item.id)) {
                    is_page_selected = false;
                    return false;
                }
            });

	        return is_page_selected;
        },
    },
	methods: {
        sandbox_updated() {
            if(this.pagination.page !== 1) {
                this.pagination.page = 1;
            } else {
                this.load_page();
            }
        },
        toggle_all() {
            this.set_items_selected({
                add: !this.is_page_selected,
                array_items: this.array_page,
            });
        },
	},
};