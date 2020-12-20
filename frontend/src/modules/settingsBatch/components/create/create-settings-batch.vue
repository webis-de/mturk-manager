<template>
  <base-dialog
    title="Add batch profile"
    activator-label="Add batch profile"
    activator-icon="mdi-plus"
    v-bind:validation="useCreateSettingsBatch.v"
    v-on:submit="useCreateSettingsBatch.create"
    v-on:cancel="useCreateSettingsBatch.reset"
  >
    <base-text-input
      v-model="useCreateSettingsBatch.settingsBatchNew.name"
      v-bind:validation="useCreateSettingsBatch.v.name"
      v-bind:options="{
        label: 'Name',
      }"
    />

    <form-settings-batch
      v-bind.sync="useCreateSettingsBatch.settingsBatchNew"
      v-bind:validation="useCreateSettingsBatch.v"
    />
  </base-dialog>
</template>

<script lang="ts">
import FormSettingsBatch from '@/modules/settingsBatch/form-settings-batch.vue';
import { defineComponent } from '@vue/composition-api';
import BaseTextInput from '@/modules/app/base/inputs/base-text-input.vue';
import BaseDialog from '@/modules/app/base/base-dialog.vue';
import { useCreate } from '@/modules/settingsBatch/components/create/useCreate';

export default defineComponent({
  name: 'CreateSettingsBatch',
  components: { BaseDialog, BaseTextInput, FormSettingsBatch },
  setup(props, { emit }) {
    const useCreateSettingsBatch = useCreate({ emit });

    return {
      useCreateSettingsBatch,
    };
  },
});
</script>
