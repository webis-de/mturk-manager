<template>
  <v-dialog v-model="dialog" max-width="500">
    <template v-slot:activator="{ on }">
    <v-btn
      v-on="on"
      class="my-0"
      icon x-small
    >
      <v-icon color="error">mdi-delete</v-icon>
    </v-btn>
    </template>

    <v-card>
      <v-card-text>
        Do you really want to delete the message '{{ item.message }}'?
      </v-card-text>

      <v-card-actions>
        <v-spacer/>
        <v-btn text color="error" v-on:click="remove()">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ServiceMessages } from '../services/messages-reject.service';

export default {
  name: 'BaseDeleteMessage',
  props: {
    item: {
      required: true,
      type: Object,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    async remove() {
      await ServiceMessages.delete({
        idMessage: this.item.id,
      });

      this.$emit('delete');

      this.dialog = false;
    },
  },
};
</script>
