<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title v-text="getDescriptionTask" />
      <v-list-item-subtitle>
        <v-progress-linear
          class="my-0"
          v-bind:color="progressColor"
          v-bind:indeterminate="isPending && !isFailed"
          v-bind:value="progress"
        />
      </v-list-item-subtitle>
    </v-list-item-content>

    <v-list-item-action>
      <v-btn
        v-if="isFinished || isFailed"
        icon
        v-on:click="deleteTask()"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
import { ServiceProjects } from '../services/projects.service';

const descriptions = {
  create_batch: {
    pending: 'Pending...',
    progress: 'Uploading: HIT {current} of {total}',
    finished: 'Finished',
    failed: 'Failed',
  },
};

export default {
  name: 'BaseTask',
  props: {
    task: {
      required: true,
      type: Object,
    },
  },
  computed: {
    progressColor() {
      if (this.isFinished) {
        return 'success';
      } if (this.isFailed) {
        return 'error';
      }
      return 'primary';
    },
    isFailed() {
      return this.task.status === 3;
    },
    isFinished() {
      return this.task.status === 2;
    },
    isPending() {
      return this.task.datetime_started === null || this.progress === null;
    },
    payload() {
      const payload = {};

      if (this.task.payload !== undefined) {
        Object.assign(payload, JSON.parse(this.task.payload));
      }

      if (this.task.payloadExtern !== undefined) {
        Object.assign(payload, JSON.parse(this.task.payloadExtern));
      }

      return payload;
    },
    progress() {
      if (this.isFinished) {
        return 100;
      }

      if (this.payload.current !== undefined) {
        return (this.payload.current / this.payload.total) * 100;
      }

      return null;
    },
    getDescriptionTask() {
      let state;

      if (this.isFinished) {
        state = 'finished';
      } else if (this.isFailed) {
        state = 'failed';
      } else if (this.isPending) {
        state = 'pending';
      } else {
        state = 'progress';
      }

      let description = '';

      if (this.task.description === 'create_batch') {
        description = `Batch ${this.payload.name_batch.toUpperCase()}
        ${descriptions[this.task.description][state].replace('{current}', this.payload.current).replace('{total}', this.payload.total)}`;
      }

      return description;
    },
  },
  methods: {
    deleteTask() {
      ServiceProjects.deleteTask({
        task: this.task,
      });
    },
  },
};
</script>
