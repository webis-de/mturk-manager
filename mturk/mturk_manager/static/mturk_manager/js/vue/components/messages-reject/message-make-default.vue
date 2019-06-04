<template>
  <v-hover>
    <v-btn
      slot-scope="{ hover }"
      class="my-0"
      small
      icon

      v-bind:loading="loading"

      v-on:click="setDefault"
    >
      <v-icon
        v-bind:color="isDefault ? 'warning' : 'white'"
      >
        {{ hover || isDefault ? 'star' : 'star_border' }}
      </v-icon>
    </v-btn>
  </v-hover>
</template>

<script>

import { Service_Projects } from '../../services/service_projects';

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

      if (projectCurrent.message_reject_default === null) {
        return false;
      }

      return projectCurrent.message_reject_default.id === this.item.id;
    },
  },
  methods: {
    async setDefault() {
      // if (this.isDefault === true) {
      //   return;
      // }

      this.loading = true;

      await Service_Projects.setMessageRejectDefault({
        message: this.isDefault ? null : this.item,
      });

      this.loading = false;
    },
  },
};
</script>
