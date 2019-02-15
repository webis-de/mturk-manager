export const external_pagination = {
  watch: {
    pagination: {
      handler() {
        this.load_page();
      },
      deep: true,
    },
  },
};
