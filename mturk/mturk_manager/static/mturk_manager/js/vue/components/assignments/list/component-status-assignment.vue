<template>
  <span v-html="status_formatted"> </span>
</template>

<script>
import { STATUS_EXTERNAL, STATUS_INTERNAL } from '../../../classes/enums';

export default {
  name: 'component-status-assignment',
  props: {
    assignment: {
      required: true,
    },
  },
  computed: {
    status_formatted() {
      if (this.status_external === STATUS_EXTERNAL.APPROVED) {
        if (this.status_internal === null) {
          return '<span class="success--text">Approved</span>';
        }
        return '<span class="error--text">Rejected Internally</span>';
      } if (this.status_external === STATUS_EXTERNAL.REJECTED) {
        if (this.status_internal === null) {
          return '<span class="error--text">Rejected</span>';
        }
        return '<span class="success--text">Approved Internally</span>';
      } if (this.status_external === null) {
        return '<span >Submitted</span>';
      }
    },
    status_external() {
      return this.assignment.status_external;
    },
    status_internal() {
      return this.assignment.status_internal;
    },
  },
};
</script>

<style scoped></style>
