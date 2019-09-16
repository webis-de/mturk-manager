<template>
  <v-btn
    color="primary"
    small
    class="ml-0"
    v-on:click="openSandbox"
  >
    Open in Sandbox
  </v-btn>
</template>

<script>
import {
  mapGetters,
} from 'vuex';
import HIT from '../../../classes/hit';

export default {
  name: 'SandboxTemplate',
  props: {
    hit: {
      required: true,
      type: HIT,
    },
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  methods: {
    openSandbox() {
      console.warn('this.hit', this.hit);
      const url = `/sandbox/hit?slug_project=${this.project_current.slug}&id_hit=${this.hit.id}`;
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>

</style>
