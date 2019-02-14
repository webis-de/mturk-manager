<template>
  <!-- <div>wda</div> -->

  <v-layout wrap>
    <v-flex>
      <!-- {{object_batches}} -->
      <h2 class="headline">
        Assignment {{ assignment.id_assignment }}
        <v-btn
          slot="activator"
          class="my-0"
          icon
          small
          v-bind:to="{ name: 'assignments' }"
        >
          <v-icon>arrow_upward</v-icon>
        </v-btn>
      </h2>
    </v-flex>
  </v-layout>
</template>
<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  name: "component-assignment-detail",
  // props: {
  // 	id_batch: {
  // 		required: true,
  // 	},
  // },
  props: {
    id_assignment: {
      required: true,
      type: Number
    }
  },
  data() {
    return {};
  },
  // watch: {
  //     'worker.is_blocked': function() {
  //         console.log(this.worker.is_blocked)
  //     },
  // },
  computed: {
    assignment() {
      const object_assignments = this.get_object_assignments();
      if (object_assignments == null) {
        return {};
      } else {
        return object_assignments[this.id_assignment];
      }
    },

    // status_block() {
    //     if(this.worker.is_blocked == undefined)
    //     {
    //         return {
    //             description: 'Loading',
    //             color: 'success',
    //             icon: '',
    //         };
    //     }

    //     switch(this.worker.is_blocked)
    //     {
    //         case STATUS_BLOCK.NONE:
    //             return {
    //                 description: 'Not Blocked',
    //                 color: 'success',
    //                 icon: 'check',
    //             };
    //         case STATUS_BLOCK.SOFT:
    //             return {
    //                 description: 'Soft Blocked',
    //                 color: 'warning',
    //                 icon: 'block',
    //             };
    //         case STATUS_BLOCK.HARD:
    //             return {
    //                 description: 'Hard Blocked',
    //                 color: 'error',
    //                 icon: 'block',
    //             };
    //     }
    // },
    ...mapGetters("moduleAssignments", {
      get_object_assignments: "get_object_assignments"
    }),
    ...mapGetters(["get_show_progress_indicator"])
  },
  methods: {},
  components: {}
};
</script>

<style lang="scss" scoped>
td {
  height: unset !important;
}
td .v-input--selection-controls {
  padding: unset;
}
</style>
