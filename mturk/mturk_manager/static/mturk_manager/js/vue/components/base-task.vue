<template>
  <v-list-tile>
    <v-list-tile-content>
      <v-list-tile-title v-text="getDescriptionTask" />
      <v-list-tile-sub-title>
        <v-progress-linear
          class="my-0"
          v-bind:indeterminate="isPending"
          v-bind:value="progress"
        />
      </v-list-tile-sub-title>
    </v-list-tile-content>
  </v-list-tile>
</template>

<script>
const descriptions = {
  create_batch: {
    pending: 'Pending...',
    progress: 'Uploading Batch...',
    finished: 'Finished',
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
    isFinished() {
      return this.task.status === 2;
    },
    isPending() {
      return this.task.datetime_started === null || this.progress === null;
    },
    progress() {
      if (this.isFinished) {
        return 100;
      }

      let { payload } = this.task;
      if (payload !== null) {
        payload = JSON.parse(payload);

        if (payload.current !== undefined) {
          return (payload.current / payload.total) * 100;
        }
      }

      return null;
    },
    getDescriptionTask() {
      let state;

      if (this.isPending) {
        state = 'pending';
      } else if (this.isFinished) {
        state = 'finished';
      } else {
        state = 'progress';
      }

      return descriptions[this.task.description][state];
    },
  },
};
</script>
