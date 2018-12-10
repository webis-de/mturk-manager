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
	methods: {
	    is_page_selected(array_page, object_selected) {
	        let is_page_selected = true;

	        if(_.size(array_page) === 0) {return false;}

	        _.forEach(array_page, (item) => {
                if(!_.has(object_selected, item.id)) {
                    is_page_selected = false;
                    return false;
                }
            });
	        return is_page_selected;
        },
        sandbox_updated() {
            if(this.pagination.page !== 1) {
                this.pagination.page = 1;
            } else {
                this.load_page();
            }
        },
        toggle_all(array_items, set_selected, object_selected) {
            set_selected({
                add: !this.is_page_selected(array_items, object_selected),
                array_items: array_items,
            });
        }
	},
};