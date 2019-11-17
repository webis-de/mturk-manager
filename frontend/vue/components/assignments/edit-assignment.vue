<template>
  <v-dialog
    v-model="dialog"
    max-width="80%"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        class="my-0"
        icon
        x-small
      >
        <v-icon color="warning">
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        Edit Assignment {{ assignment.id_assignment }}
      </v-card-title>
      <v-card-text>
        <update-status
          ref="updateStatus"
          v-bind:assignment="assignment"
          v-on:update="updateAssignment($event)"
        />
<!--        {{assignmentNew.status_external}}-->
<!--        {{assignmentNew.status_internal}}-->
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="primary"
          v-on:click="save()"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import UpdateStatus from './update-status';
import Assignment from '../../classes/assignment';
import { Service_Assignments } from '../../services/service_assignments';

export default {
  name: 'EditAssignment',
  components: { UpdateStatus },
  props: {
    assignment: {
      required: true,
      type: Assignment,
    },
  },
  data() {
    return {
      dialog: false,
      assignmentNew: new Assignment(this.assignment),
    };
  },
  watch: {
    dialog(value) {
      if (value === false) {
        this.$refs.updateStatus.reset();
      }
    },
  },
  methods: {
    updateAssignment(assignment) {
      this.assignmentNew.status_external = assignment.status_external;
      this.assignmentNew.status_internal = assignment.status_internal;
    },
    async save() {
      if (!_.isEqual(this.assignment, this.assignmentNew)) {
        await Service_Assignments.edit({
          assignmentNew: this.assignmentNew,
          assignmentCurrent: this.assignment,
        });

        this.dialog = false;
      }
    },
  },
};
</script>

<style scoped>

</style>
