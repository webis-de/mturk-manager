export default {
  watch: {
    pagination: {
      handler() {
        this.load_page();
      },
      deep: true,
    },
  },
};
