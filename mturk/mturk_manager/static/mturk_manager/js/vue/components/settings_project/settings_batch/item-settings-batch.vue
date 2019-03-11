<template>
  <tr
    v-bind:key="settingsBatch.id"
    class="text-no-wrap"
  >
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      {{ settingsBatch.name }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      {{ settingsBatch.title }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <base-display-amount v-bind:amount="settingsBatch.reward"></base-display-amount>
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      {{ settingsBatch.block_workers }}
    </td>

    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <component-edit-settings-batch
        v-bind:key="`edit-settings-batch-${props.item.id}`"
        v-bind:settings-batch-current="settingsBatch"
        v-on:edited="$emit('edited')"
      />
      <component-delete-settings-batch
        v-bind:key="`delete-settings-batch-${props.item.id}`"
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
  components: {BaseDisplayAmount, ComponentDeleteSettingsBatch, ComponentEditSettingsBatch },
  props: {
    props: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {};
  },
  computed: {
    settingsBatch() { return this.props.item; },
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
