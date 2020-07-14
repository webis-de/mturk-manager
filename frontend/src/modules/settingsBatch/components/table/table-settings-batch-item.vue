<template>
  <base-table-item
    v-bind:key="settingsBatch.id"
    v-bind:item="settingsBatch"
  >
    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="settingsBatch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="title"
      class="text-left text-capitalize"
      v-bind:item="settingsBatch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.title }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="reward"
      class="text-left text-capitalize"
      v-bind:item="settingsBatch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <base-display-amount v-bind:amount="item.reward" />
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="blockWorkers"
      class="text-left text-capitalize"
      v-bind:item="settingsBatch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.blockWorkers }}
    </base-table-cell>

    <base-table-cell
      name="actions"
      class="text-left text-capitalize"
      v-bind:item="settingsBatch"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <update-settings-batch v-bind:settings-batch="settingsBatch" />
      <delete-settings-batch v-bind:settings-batch="settingsBatch" />
      <!--      <component-edit-settings-batch-->
      <!--        v-bind:key="`edit-settings-batch-${settingsBatch.id}`"-->
      <!--        v-bind:settings-batch-current="settingsBatch"-->
      <!--        v-on:edited="$emit('edited')"-->
      <!--      />-->
      <!--      <component-delete-settings-batch-->
      <!--        v-bind:key="`delete-settings-batch-${settingsBatch.id}`"-->
      <!--        v-bind:settings-batch-current="settingsBatch"-->
      <!--        v-on:deleted="$emit('deleted')"-->
      <!--      />-->
    </base-table-cell>
  </base-table-item>
</template>

<script lang="ts">
import BaseDisplayAmount from '@/components/base-display-amount';
import BaseTableItem from '@/components/base-table-item.vue';
import BaseTableCell from '@/components/base-table-cell.vue';
import { SettingsBatch } from '@/modules/settingsBatch/settingsBatch.model';
import UpdateSettingsBatch from '@/modules/settingsBatch/components/update/update-settings-batch.vue';
import DeleteSettingsBatch from '@/modules/settingsBatch/components/delete/delete-settings-batch.vue';

export default {
  name: 'TableSettingsBatchItem',
  components: {
    DeleteSettingsBatch,
    UpdateSettingsBatch,
    BaseTableCell,
    BaseTableItem,
    BaseDisplayAmount,
  },
  props: {
    settingsBatch: {
      type: SettingsBatch,
      required: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
};
</script>

<style scoped>

</style>
