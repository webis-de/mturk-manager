<template>
  <base-dialog
    title="Add reject message"
    activator-label="Add Message"
    activator-icon="mdi-plus"
    v-bind:disabled="vuelidate.$invalid"
    v-on:submit="save"
    v-on:cancel="reset"
  >
    <base-combobox
      v-model="message"
      v-bind:validation="vuelidate.message"
      v-bind:options="{
        label: 'Message',
        'item-text': 'message',
        'item-value':'message_lowercase',
        items,
        loading: isLoading,
      }"
      v-bind:search-input.sync="messageSearch"
    />
  </base-dialog>
</template>

<script lang="ts">
import { MessageReject } from '@/modules/message/messageReject.model';
import { ServiceMessages } from '@/modules/message/message.service';
import { store } from '@/store/vuex';
import BaseDialog from '@/modules/app/base/base-dialog.vue';
import debounce from 'lodash-es/debounce';
import { defineComponent, ref, watch } from '@vue/composition-api';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import type { BaseDialogParamsSubmit, ID } from '@/modules/app/types';
import BaseCombobox from '@/modules/app/base/inputs/base-combobox.vue';

export default defineComponent({
  name: 'CreateMessage',
  components: { BaseCombobox, BaseDialog },
  setup() {
    const message = ref<string | { id: ID, message: string }>('');
    const items = ref([]);
    const isLoading = ref(true);
    const messageSearch = ref<string | null>('');

    const vuelidate = useVuelidate({ message: { required } }, { message });

    const save = async ({ close }: BaseDialogParamsSubmit) => {
      if (vuelidate.value.$invalid === false) {
        let messageInternal;
        const projects = [store.getters['moduleProjects/get_project_current'].id];

        if (typeof message.value === 'string') {
          messageInternal = new MessageReject({
            projects,
            message: message.value,
          });
        } else {
          messageInternal = new MessageReject({
            projects,
            id: message.value.id,
            message: message.value.message,
          });
        }

        await ServiceMessages.create({
          message: messageInternal,
        });

        close();
      }
    };

    const searchDebounced = debounce(async (value) => {
      isLoading.value = true;
      items.value = await ServiceMessages.search({
        message: value,
        cls: MessageReject,
      });

      isLoading.value = false;
    }, 500);

    const reset = () => {
      message.value = '';
    };

    watch(messageSearch, async (value) => {
      if (value !== null && value.trim() !== '') {
        await searchDebounced(value);
      } else {
        searchDebounced.cancel();

        isLoading.value = true;
        items.value = await ServiceMessages.loadMessages({
          project: null,
          limit: 4,
          saveToStore: false,
        });

        isLoading.value = false;
      }
    });

    return {
      message,
      items,
      isLoading,
      messageSearch,
      searchDebounced,
      vuelidate,
      save,
      reset,
    };
  },
});
</script>

<style scoped>

</style>
