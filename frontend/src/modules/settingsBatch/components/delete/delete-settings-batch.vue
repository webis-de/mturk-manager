<template>
  <v-dialog
    v-model="dialog"
    max-width="500"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="my-0"
        icon
        x-small
        v-on="on"
      >
        <v-icon color="error">
          mdi-delete
        </v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Delete batch profile</span>
        <v-spacer />
        <v-btn
          icon
          v-on:click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        Do you really want to delete the batch profile '{{
          settingsBatch.name
        }}'?
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          color="error"
          v-on:click="remove()"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';

export default {
  name: 'DeleteSettingsBatch',
  props: {
    settingsBatch: {
      required: true,
      type: SettingsBatch,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    remove() {
      ServiceSettingsBatch.delete({
        settingsBatch: this.settingsBatch,
      });
    },
  },
};
</script>

<style scoped></style>
