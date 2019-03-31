<template>
  <span>
    <v-tooltip top>
      <v-btn
        slot="activator"
        class="my-0"
        icon
        small
        v-bind:disabled="disabled"
        v-on:click.stop="dialog = true"
      >
        <v-icon color="error">
          delete
        </v-icon>
      </v-btn>

      You are not allowed to delete this template because it has at least one batch using this template.
    </v-tooltip>

    <v-dialog
      v-model="dialog"
      max-width="500"
    >

      <v-card>
        <v-card-text>
          Do you really want to delete the assignment template '{{
            templateWorker.name
          }}'?
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            flat
            color="error"
            v-on:click="remove()"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </span>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { Service_Templates } from '../../../services/service_templates';

export default {
  name: 'ComponentDeleteTemplateWorker',
  props: {
    templateWorker: {
      required: true,
      type: Object,
    },
    disabled: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {
      dialog: false,
      tooltip: false,
    };
  },
  methods: {
    remove() {
      Service_Templates.delete({
        typeTemplate: 'worker',
        project: this.project_current,
        template: this.templateWorker,
        callback: () => {
          Service_Templates.cleanup({
            typeTemplate: 'workerAll',
            component: this,
            nameEvent: 'deleted',
            template: this.templateWorker,
          });
        },
      });
    },
    ...mapActions('moduleProjects', {
      delete_template_worker: 'delete_template_worker',
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
