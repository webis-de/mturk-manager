<template>
  <base-table
    title="Batch profiles"

    v-bind:array-items="$store.getters['moduleSettingsBatch/settingsBatchSortedByName']"

    name-vuex-module="moduleSettingsBatch"
    name-state-pagination="paginationGeneral"
    name-local-storage-pagination="paginationSettingsBatchGeneral"

    name-state-columns="arrayColumns"
    name-state-columns-selected="objectColumnsSelectedInitialGeneral"

    v-bind:show-select="false"
  >
    <template
      #default="{ item, objectColumnsSelected, isCondensed }"
    >
      <table-settings-batch-item
        v-bind:settings-batch="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template #actions>
      <create-settings-batch />
    </template>
  </base-table>
</template>

<script lang="ts">
import BaseTable from '@/components/base-table.vue';
import TableSettingsBatchItem from '@/modules/settingsBatch/components/table/table-settings-batch-item.vue';
import CreateSettingsBatch from '@/modules/settingsBatch/components/create/create-settings-batch.vue';

export default {
  name: 'TableSettingsBatch',
  components: {
    CreateSettingsBatch,
    TableSettingsBatchItem,
    BaseTable,
  },
};
</script>

<style scoped>

</style>
