<template>
  <tr
    v-bind:key="settingsBatch.id"
    class="text-no-wrap"
    v-bind:class="classes"
  >
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ settingsBatch.name }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      {{ settingsBatch.title }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <base-display-amount v-bind:amount="settingsBatch.reward" />
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      {{ settingsBatch.blockWorkers }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <component-edit-settings-batch
        v-bind:key="`edit-settings-batch-${settingsBatch.id}`"
        v-bind:settings-batch-current="settingsBatch"
        v-on:edited="$emit('edited')"
      />
      <component-delete-settings-batch
        v-bind:key="`delete-settings-batch-${settingsBatch.id}`"
        v-bind:settings-batch-current="settingsBatch"
        v-on:deleted="$emit('deleted')"
      />
    </td>
  </tr>
</template>

<script>
import ComponentEditSettingsBatch from './component_edit_settings_batch';
import ComponentDeleteSettingsBatch from './component_delete_settings_batch';
import BaseDisplayAmount from '../../base-display-amount';

export default {
  name: 'ItemSettingsBatch',
  components: { BaseDisplayAmount, ComponentDeleteSettingsBatch, ComponentEditSettingsBatch },
  props: {
    item: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
    classes: {
      required: false,
      type: Object | Array,
      default() {
        return {};
      },
    },
  },
  data() {
    return {};
  },
  computed: {
    settingsBatch() { return this.item; },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: 'unset !important',
          paddingLeft: '5px !important',
          paddingRight: '5px !important',
        };
      }
      return {};
    },
  },
};
</script>

<style scoped>

</style>
