import _ from 'lodash';

export const table = {
  methods: {
    // Reset pagination/load page if the sandbox status was changed
    sandbox_updated() {
      if (this.pagination.page !== 1) {
        this.pagination.page = 1;
      } else {
        this.load_page(this.filters);
      }
    },
  },
};
