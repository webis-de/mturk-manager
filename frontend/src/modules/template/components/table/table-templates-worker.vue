<template>
  <base-table
    title="Worker templates"

    v-bind:array-items="$store.getters['moduleTemplates/templatesWorker']"

    name-vuex-module="moduleTemplates"
    name-state-pagination="paginationWorker"
    name-local-storage-pagination="paginationTemplatesWorker"

    name-state-columns="arrayColumnsWorker"
    name-state-columns-selected="objectColumnsSelectedInitialGeneral"

    v-bind:show-select="false"
  >
    <template
      #default="{ item, objectColumnsSelected, isCondensed }"
    >
      <table-templates-worker-item
        v-bind:template="item"
        v-bind:object-columns-selected="objectColumnsSelected"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template #actions>
      <create-template-worker />
    </template>
  </base-table>
</template>

<script lang="ts">
import BaseTable from '@/components/base-table.vue';
import TableTemplatesWorkerItem from '@/modules/template/components/table/table-templates-worker-item.vue';
import CreateTemplateWorker from '@/modules/template/components/create/create-template-worker.vue';

export default {
  name: 'TableTemplatesWorker',
  components: { CreateTemplateWorker, TableTemplatesWorkerItem, BaseTable },
};
</script>

<style scoped>

</style>
