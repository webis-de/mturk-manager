<template>
  <base-dialog
    title="Add batch profile"
    activator-label="Edit batch profile"
    activator-icon="mdi-plus"
    v-bind:validation="useUpdateSettingsBatch.v"
    v-on:submit="useUpdateSettingsBatch.create"
    v-on:cancel="useUpdateSettingsBatch.reset"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        class="my-0"
        icon
        x-small
        v-on="on"
      >
        <v-icon color="warning">
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>

    <base-text-input
      v-model="useUpdateSettingsBatch.settingsBatchUpdated.name"
      v-bind:validation="useUpdateSettingsBatch.v.name"
      v-bind:options="{
        label: 'Name',
      }"
    />

    <form-settings-batch
      v-bind.sync="useUpdateSettingsBatch.settingsBatchUpdated"
      v-bind:validation="useUpdateSettingsBatch.v"
    />
  </base-dialog>
</template>
<script lang="ts">
import BaseDialog from '@/modules/app/base/base-dialog.vue';
import BaseTextInput from '@/modules/app/base/inputs/base-text-input.vue';
import FormSettingsBatch from '@/modules/settingsBatch/form-settings-batch.vue';
import { computed, defineComponent } from '@vue/composition-api';
import { useUpdate } from '@/modules/settingsBatch/components/update/useUpdate';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';

export default defineComponent({
  name: 'UpdateSettingsBatch',
  components: { BaseDialog, BaseTextInput, FormSettingsBatch },
  props: {
    settingsBatch: {
      required: true,
      type: SettingsBatch,
    },
  },
  setup(props, { emit }) {
    const settingsBatch = computed(() => props.settingsBatch);

    const useUpdateSettingsBatch = useUpdate({ settingsBatch, emit });

    return {
      useUpdateSettingsBatch,
    };
  },
});
// export default {
//   name: 'UpdateSettingsBatch',
//   components: {
//     FormSettingsBatch,
//     BaseTextInput,
//     BaseDialog,
//   },
//   mixins: [validations, settingsBatch],
//   props: {
//     settingsBatch: {
//       required: true,
//       type: SettingsBatch,
//     },
//   },
//   data(): Record<string, unknown> {
//     return {
//       dialog: false,
//       disable_unique_name: true,
//       name_not_unique: true,
//     };
//   },
//   watch: {
//     dialog(): void {
//       this.reset();
//     },
//   },
//   created(): void {
//     this.$v.$touch();
//   },
//   methods: {
//     update(): void {
//       if (this.$refs.form.validate()) {
//         // this.settings_batch.project = this.$store.getters['moduleProjects/get_project_current'].id;
//         ServiceSettingsBatch.update({
//           settingsBatch: this.settings_batch,
//         });
//
//         this.dialog = false;
//         this.$emit('edited');
//         this.reset();
//       }
//     },
//     reset(): void {
//       this.update_fields();
//       this.$v.$reset();
//       this.$v.$touch();
//     },
//     ...mapActions('moduleProjects', {
//       edit_settings_batch: 'edit_settings_batch',
//     }),
//   },
// };
</script>
