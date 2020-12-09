<template>
  <v-dialog
    v-model="isDialogOpen"
    fullscreen
  >
    <template v-slot:activator="{ on: onDialog }">
      <v-tooltip top>
        <template
          v-slot:activator="{ on: onTooltip }"
          v-bind:disabled="!isDisabled"
        >
          <div v-on="onTooltip">
            <v-btn
              color="primary"
              small
              v-on="onDialog"
            >
              <v-icon>mdi-plus</v-icon> Add profile
            </v-btn>
          </div>
        </template>

        You have to create a worker template.
      </v-tooltip>
    </template>

    <v-card>
      <form v-on:submit.prevent="useCreateSettingsBatch.create">
        <v-card-title>
          <span class="headline">Add Batch Profile</span>
          <v-spacer />
          <v-btn
            icon
            v-on:click="isDialogOpen = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form>
            <base-text-field
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
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            class="ml-0"
            color="înfo"
            v-on:click="
              isDialogOpen = false;
            "
          >
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            text
            type="submit"
            class="ml-0"
            color="primary"
          >
            Save
          </v-btn>
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { ServiceSettingsBatch } from '@/modules/settingsBatch/settingsBatch.service';
import FormSettingsBatch from '@/modules/settingsBatch/form-settings-batch.vue';
import { defineComponent, ref, watch } from '@vue/composition-api';
import BaseTextField from '@/modules/app/base/inputs/base-text-field.vue';

export default defineComponent({
  name: 'CreateSettingsBatch',
  components: { BaseTextField, FormSettingsBatch },
  setup() {
    const isDialogOpen = ref(false);
    const useCreateSettingsBatch = ServiceSettingsBatch.useCreate();

    watch(isDialogOpen, (isOpen) => {
      if (isOpen) {
        useCreateSettingsBatch.reset();
      }
    });

    return {
      isDialogOpen,
      useCreateSettingsBatch,
    };
  },
});
</script>
