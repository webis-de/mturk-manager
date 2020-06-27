<template>
  <base-table
    title="Requester templates"

    v-bind:array-items="$store.getters['moduleTemplates/templatesRequester']"

    name-vuex-module="moduleTemplates"
    name-state-pagination="paginationRequester"
    name-local-storage-pagination="paginationTemplatesRequester"

    name-state-columns="arrayColumns"
    name-state-columns-selected="objectColumnsSelectedInitial"
  >
    <template
      v-slot:default="{ item, objectColumnsSelected, isCondensed }"
    >
      <!--      <item-templates-assignment-->
      <!--        v-bind:item="item"-->
      <!--        v-bind:object-columns-selected="objectColumnsSelected"-->
      <!--        v-bind:is-condensed="isCondensed"-->

      <!--        v-on:edited="snackbarEdited = true"-->
      <!--        v-on:deleted="snackbarDeleted = true"-->
      <!--      />-->
    </template>

    <!--    <template v-slot:actions>-->
    <!--      <component-add-template-assignment-->
    <!--        v-on:created="snackbarCreated = true"-->
    <!--      />-->
    <!--    </template>-->
  </base-table>
</template>

<script>
import BaseTable from '../../../../components/base-table';

export default {
  name: 'TableTemplatesRequester',
  components: { BaseTable },
};
</script>

<style scoped>

</style>
