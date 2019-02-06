import _ from 'lodash';
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
        // Reset pagination/load page if the sandbox status was changed
        sandbox_updated() {
            if(this.pagination.page !== 1) {
                this.pagination.page = 1;
            } else {
                this.load_page();
            }
        },
	},
};