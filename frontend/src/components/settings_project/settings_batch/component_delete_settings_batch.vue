<template>
  <v-dialog
    v-model="dialog"
    max-width="500"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        class="my-0"
        icon
        x-small
      >
        <v-icon color="error">
          mdi-delete
        </v-icon>
      </v-btn>
    </template>

    <v-card>
      <!-- <v-card-title>
                <span class="headline">Add Profile</span>
                <v-spacer></v-spacer>
                <v-btn icon v-on:click="dialog = false">
                    <v-icon>close</v-icon>
                </v-btn>
            </v-card-title> -->
      <v-card-text>
        Do you really want to delete the batch profile '{{
          settingsBatchCurrent.name
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

<script>
import {
  mapActions, mapGetters,
} from 'vuex';
import { ServiceSettingsBatch } from '../../../services/service_settings_batch';

export default {
  name: 'ComponentDeleteSettingsBatch',
  props: {
    settingsBatchCurrent: {},
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  methods: {
    remove() {
      ServiceSettingsBatch.delete({
        project: this.project_current,
        settings_batch: this.settingsBatchCurrent,
        callback: () => {
          this.$emit('deleted');
          this.dialog = false;
        },
      });
    },
  },
};
</script>

<style scoped></style>
