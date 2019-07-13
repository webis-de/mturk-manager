<template>
  <v-bottom-sheet
    v-model="open"
    persistent
    inset
    hide-overlay
  >
    <v-card>
      <v-list>
        <base-task
          v-for="task in arrayTasks"
          v-bind:key="task.id"
          v-bind:task="task"
        />
      </v-list>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
import BaseTask from './base-task';

export default {
  name: 'TheTasksBar',
  components: { BaseTask },
  data() {
    return {
      open: true,
    };
  },
  computed: {
    arrayTasks() {
      return this.$store.state.moduleProjects.arrayTasks;
    },
  },
};
</script>
