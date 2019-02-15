<template>
  <v-layout>
    <v-flex>
      <v-layout>
        <v-flex sm1>Max costs</v-flex>
        <v-flex
          ><base-display-amount
            v-bind:amount="sum_costs_max"
          ></base-display-amount
        ></v-flex>
      </v-layout>
      <v-layout>
        <v-flex sm1>Costs so far</v-flex>
        <v-flex
          ><base-display-amount
            v-bind:amount="sum_costs_so_far"
          ></base-display-amount
        ></v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import {
  mapState, mapGetters, mapMutations, mapActions,
} from 'vuex';
import BaseDisplayAmount from '../base-display-amount.vue';

export default {
  name: 'display-expenses',
  computed: {
    sum_costs_max() {
      return (
        (this.use_sandbox === true
          ? this.project_current.sum_costs_max_sandbox
          : this.project_current.sum_costs_max) || 0
      );
    },
    sum_costs_so_far() {
      return (
        (this.use_sandbox === true
          ? this.project_current.sum_costs_so_far_sandbox
          : this.project_current.sum_costs_so_far) || 0
      );
    },
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
    ...mapState('module_app', ['use_sandbox']),
  },
  components: {
    BaseDisplayAmount,
  },
};
</script>

<style scoped></style>
