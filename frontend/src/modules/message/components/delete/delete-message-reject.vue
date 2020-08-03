<template>
  <base-dialog
    title="Delete reject message"
    small
    color-button-submit="error"
    label-button-submit="Delete"
    v-on:submit="remove"
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

    <template v-slot:content>
      Do you really want to delete the template '{{
        message.message
      }}'?
    </template>
  </base-dialog>
</template>

<script lang="ts">
import { MessageBase } from '@/modules/message/messageBase.model';
import BaseDialog from '@/modules/app/components/base-dialog.vue';
import { ServiceMessages } from '@/modules/message/message.service';

export default {
  name: 'DeleteMessageReject',
  components: { BaseDialog },
  props: {
    message: {
      required: true,
      type: MessageBase,
    },
  },
  methods: {
    remove() {
      ServiceMessages.delete({
        message: this.message,
      });
    },
  },
};
</script>

<style scoped></style>
