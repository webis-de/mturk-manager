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
      <!-- <v-card-title>
            <span class="headline">Add Profile</span>
            <v-spacer></v-spacer>
            <v-btn icon v-on:click="dialog = false">
                <v-icon>close</v-icon>
            </v-btn>
        </v-card-title> -->
      <v-card-text>
        Do you really want to delete the global template '{{
          template_global.name
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
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { ServiceTemplates } from '../../../services/service_templates';

export default {
  name: 'ComponentDeleteTemplateGlobal',
  props: {
    template_global: {},
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    remove() {
      ServiceTemplates.delete({
        typeTemplate: 'global',
        project: this.project_current,
        template: this.template_global,
        callback: () => {
          ServiceTemplates.cleanup({
            typeTemplate: 'globalAll',
            component: this,
            nameEvent: 'deleted',
            template: this.template_global,
          });
        },
      });
    },
    ...mapActions('moduleProjects', {
      delete_template_global: 'delete_template_global',
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
