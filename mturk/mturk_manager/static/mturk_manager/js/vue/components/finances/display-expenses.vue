<template>
  <v-layout>
    <v-flex>
      <v-layout>
        <v-flex>
          Costs so far
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex>
          Max costs
        </v-flex>
      </v-layout>
    </v-flex>

    <v-flex
      class="ml-5"
    >
      <v-layout>
        <v-flex>
          <base-display-amount
            v-if="sum_costs_so_far !== null"

            v-bind:amount="sum_costs_so_far"
          />
          <v-progress-circular
            v-else
            indeterminate
            size="20"
            width="2"
          ></v-progress-circular>
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex>
          <base-display-amount
            v-if="sum_costs_max !== null"

            v-bind:amount="sum_costs_max"
          />
          <v-progress-circular
            v-else
            indeterminate
            size="20"
            width="2"
          ></v-progress-circular>
        </v-flex>
      </v-layout>
    </v-flex>

    <!--<v-flex>-->
      <!--<v-layout>-->
        <!--<v-flex>Max costs</v-flex>-->
        <!--<v-flex-->
          <!--&gt;<base-display-amount-->
            <!--v-bind:amount="sum_costs_max"-->
          <!--&gt;</base-display-amount-->
        <!--&gt;</v-flex>-->
      <!--</v-layout>-->
      <!--<v-layout>-->
        <!--<v-flex>Costs so far</v-flex>-->
        <!--<v-flex-->
          <!--&gt;<base-display-amount-->
            <!--v-bind:amount="sum_costs_so_far"-->
          <!--&gt;</base-display-amount-->
        <!--&gt;</v-flex>-->
      <!--</v-layout>-->
    <!--</v-flex>-->
  </v-layout>
</template>

<script>
import {
  mapState, mapGetters, mapMutations, mapActions,
} from 'vuex';
import BaseDisplayAmount from '../base-display-amount.vue';

export default {
  name: 'DisplayExpenses',
  components: {
    BaseDisplayAmount,
  },
  computed: {
    ...mapState('module_app', ['use_sandbox']),
    ...mapState('module_finances', [
      'sum_costs_max',
      'sum_costs_so_far',
    ]),
  },
};
</script>

<style scoped></style>
