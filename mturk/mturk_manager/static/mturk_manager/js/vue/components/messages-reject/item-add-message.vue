<template>
  <v-dialog v-model="dialog">
    <v-btn
      slot="activator"
      color="primary"
      small
    >
      <v-icon>add</v-icon> Add Message
    </v-btn>

    <v-card>
      <v-card-title>
        <span class="headline">
          Add Reject Message
        </span>
        <v-spacer/>
        <v-btn
          icon
          v-on:click="dialog = false"
        >
          <v-icon>close</v-icon>
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
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { ServiceMessages } from '../../services/Service_Messages_Reject';

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

      if (value !== this.model) {
        this.items = await ServiceMessages.loadAll({
          search: value,
        });
      }

      this.isLoading = false;
    },
    async model(value) {
      const object = {};

      if (typeof value === 'string') {
        object.message = value;
      } else {
        object.id = value.id;
      }

      await ServiceMessages.save({
        message: object,
      });

      this.$emit('create');

      this.dialog = false;
    },
  },
};
</script>
