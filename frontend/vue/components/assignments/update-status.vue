<template>
  <v-layout>
    <v-flex>
      <v-btn-toggle
        v-model="statusNew"
      >
        <v-btn
          v-bind:disabled="!canBeApproved"
          value="approved"
          color="success"
        >
          Approve
        </v-btn>
        <v-btn
          v-bind:disabled="!canBeRejectedInternally"
          value="rejectedInternally"
          color="warning"
        >
          Reject Internally
        </v-btn>

        <v-divider
          class="ml-2 mr-2"
          vertical
        />

        <v-btn
          v-bind:disabled="!canBeRejected"
          value="rejected"
          color="error"
        >
          Reject
        </v-btn>
        <v-btn
          v-bind:disabled="!canBeApprovedInternally"
          value="approvedInternally"
          color="warning"
        >
          Approve Internally
        </v-btn>
      </v-btn-toggle>
    </v-flex>
  </v-layout>
</template>

<script>
import Assignment from '../../classes/assignment';
import { STATUS_EXTERNAL, STATUS_INTERNAL } from '../../classes/enums';

export default {
  name: 'UpdateStatus',
  props: {
    assignment: {
      required: true,
      type: Assignment,
    },
  },
  data() {
    return {
      statusNew: undefined,
      assignmentNew: new Assignment(this.assignment),
      STATUS_EXTERNAL,
      STATUS_INTERNAL,
    };
  },
  computed: {
    canBeApproved() {
      return this.assignment.status_external !== STATUS_EXTERNAL.APPROVED
        || this.assignment.status_internal !== null;
    },
    canBeRejectedInternally() {
      return this.assignment.status_external !== STATUS_EXTERNAL.APPROVED
        || this.assignment.status_internal !== STATUS_INTERNAL.REJECTED;
    },
    canBeRejected() {
      return !(this.assignment.status_external === STATUS_EXTERNAL.REJECTED
        && this.assignment.status_internal === null)
        && this.assignment.status_external !== STATUS_EXTERNAL.APPROVED;
    },
    canBeApprovedInternally() {
      return !(this.assignment.status_external === STATUS_EXTERNAL.REJECTED
        && this.assignment.status_internal === STATUS_INTERNAL.APPROVED)
        && this.assignment.status_external !== STATUS_EXTERNAL.APPROVED;
    },
  },
  watch: {
    statusNew() {
      switch (this.statusNew) {
        case 'approved':
          this.assignmentNew.status_external = STATUS_EXTERNAL.APPROVED;
          this.assignmentNew.status_internal = null;
          break;
        case 'rejectedInternally':
          this.assignmentNew.status_external = STATUS_EXTERNAL.APPROVED;
          this.assignmentNew.status_internal = STATUS_INTERNAL.REJECTED;
          break;
        case 'rejected':
          this.assignmentNew.status_external = STATUS_EXTERNAL.REJECTED;
          this.assignmentNew.status_internal = null;
          break;
        case 'approvedInternally':
          this.assignmentNew.status_external = STATUS_EXTERNAL.REJECTED;
          this.assignmentNew.status_internal = STATUS_INTERNAL.APPROVED;
          break;
        default:
      }

      this.$emit('update', this.assignmentNew);
    },
  },
  methods: {
    reset() {
      this.statusNew = undefined;
    },
  },
};
</script>

<style scoped>

</style>
