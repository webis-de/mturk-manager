<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn
        color="primary"
        small
        v-on="on"
      >
        <v-icon>mdi-plus</v-icon> Add Message
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">
          Add Reject Message
        </span>
        <v-spacer />

        <v-btn
          icon
          v-on:click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-combobox
          v-model="model"
          v-bind:items="items"
          v-bind:loading="isLoading"
          v-bind:search-input.sync="search"

          label="Message"
          autofocus
          dense
          item-text="message"
          item-value="message_lowercase"
          no-filter

          v-on:input="input($event)"
        />
      </v-card-text>
      <v-card-actions />
    </v-card>
  </v-dialog>
</template>

<script>
import { MessageReject } from '@/modules/message/MessageReject.model';
import { ServiceMessages } from '@/services/messages-reject.service';

export default {
  name: 'ItemAddMessage',
  data() {
    return {
      dialog: false,
      model: '',
      items: [],
      search: '',
      isLoading: false,
    };
  },
  watch: {
    async search(value) {
      this.isLoading = true;
      // TODO show most used messages initially (if value === null)
      if (value !== null && value !== this.model) {
        this.items = await ServiceMessages.search({
          message: value,
          cls: MessageReject,
        });
      }

      this.isLoading = false;
    },
  },
  methods: {
    async input(value) {
      if (value === null || value === '') {
        return;
      }

      const object = {};

      if (typeof value === 'string') {
        object.message = value;
      } else {
        object.id = value.id;
      }

      await ServiceMessages.save({
        message: object,
      });

      // emit create event
      this.$emit('create');
      this.model = '';
      this.dialog = false;
    },
  },
};
</script>
