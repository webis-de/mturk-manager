<template>
  <base-dialog
    title="Add reject message"
    v-bind:disabled="$v.$invalid"
    v-on:submit="save"
    v-on:cancel="reset"
  >
    <template v-slot:content>
      <v-combobox
        v-model="message"
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
    </template>
  </base-dialog>
</template>

<script>
import { MessageReject } from '@/modules/message/messageReject.model';
import { ServiceMessages } from '@/modules/message/message.service';
import { required } from 'vuelidate/lib/validators';
import { store } from '@/store/vuex';
import BaseDialog from '@/modules/app/components/base-dialog';

export default {
  name: 'CreateMessage',
  components: { BaseDialog },
  data() {
    return {
      message: '',
      items: [],
      isLoading: true,
      search: '',
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
    async save({ close }) {
      if (this.$v.$invalid === false) {
        let message;
        const projects = [store.getters['moduleProjects/get_project_current'].id];

        if (typeof this.message === 'string') {
          message = new MessageReject({
            projects,
            message: this.message,
          });
        } else {
          message = new MessageReject({
            projects,
            ...this.message,
          });
        }

        await ServiceMessages.create({
          message,
        });

        close();
      }
    },
    reset() {
      this.message = '';
    },
  },
  validations: {
    message: {
      required,
    },
  },
};
</script>

<style scoped>

</style>
