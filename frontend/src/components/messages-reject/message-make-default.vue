<template>
  <v-hover>
    <v-btn
      slot-scope="{ hover }"
      class="my-0"
      x-small
      icon

      v-bind:loading="loading"

      v-on:click="setDefault"
    >
      <v-icon
        v-bind:color="isDefault ? 'warning' : 'white'"
      >
        {{ hover || isDefault ? 'mdi-star' : 'mdi-star-outline' }}
      </v-icon>
    </v-btn>
  </v-hover>
</template>

<script>

import { ServiceProjects } from '../../services/projects.service';

export default {
  name: 'MessageMakeDefault',
  props: {
    item: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    isDefault() {
      const projectCurrent = this.$store.getters['moduleProjects/get_project_current'];

      if (projectCurrent.message_reject_default === null || projectCurrent.message_reject_default === undefined) {
        return false;
      }

      return projectCurrent.message_reject_default.id === parseInt(this.item.id, 10);
    },
  },
  methods: {
    async setDefault() {
      // if (this.isDefault === true) {
      //   return;
      // }

      this.loading = true;

      await ServiceProjects.setMessageRejectDefault({
        message: this.isDefault ? null : this.item,
      });

      this.loading = false;
    },
  },
};
</script>
