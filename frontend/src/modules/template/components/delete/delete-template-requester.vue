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
        <span class="headline">Delete template</span>
        <v-spacer />
        <v-btn
          icon
          v-on:click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        Do you really want to delete the template '{{
          template.name
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
import { TemplateBase } from '@/modules/template/templateBase.model';
import { ServiceTemplates } from '@/modules/template/template.service';

export default {
  name: 'DeleteTemplateRequester',
  props: {
    template: {
      required: true,
      type: TemplateBase,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    remove() {
      ServiceTemplates.delete({
        template: this.template,
      });
    },
  },
};
</script>

<style scoped></style>
