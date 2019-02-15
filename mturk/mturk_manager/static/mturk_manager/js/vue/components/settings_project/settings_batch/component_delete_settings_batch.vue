<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-btn slot="activator" icon small>
      <v-icon color="error">delete</v-icon>
    </v-btn>

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
          settings_batch_current.name
        }}'?
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat color="error" v-on:click="remove()">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { Service_Settings_Batch } from '../../../services/service_settings_batch';

export default {
  name: 'component-delete-settings-batch',
  props: {
    settings_batch_current: {},
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    remove() {
      Service_Settings_Batch.delete({
        project: this.project_current,
        settings_batch: this.settings_batch_current,
        callback: () => {
          this.$emit('deleted');
          this.dialog = false;
        },
      });
    },
    ...mapActions('moduleProjects', {
      delete_settings_batch: 'delete_settings_batch',
    }),
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  components: {},
};
</script>

<style scoped></style>
