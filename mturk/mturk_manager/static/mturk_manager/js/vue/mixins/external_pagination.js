export default {
  watch: {
    pagination: {
      handler() {
        console.warn('watcher')
        this.load_page();
      },
      deep: true,
    },
  },
};
