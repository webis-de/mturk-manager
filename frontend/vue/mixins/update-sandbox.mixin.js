import { mapState, mapActions } from 'vuex';

export const updateSandbox = {
  methods: {
    ...mapActions(['set_show_progress_indicator']),
  },
  computed: {
    ...mapState('module_app', ['use_sandbox']),
  },
  watch: {
    use_sandbox(useSandbox) {
      this.sandboxUpdated(useSandbox);
    },
  },
};
