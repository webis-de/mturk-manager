<template>
  <v-layout wrap>
    <base-table-filter
      title="HIT ID"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="hitsSelected"
    >
      <v-combobox
        v-model="filters.hitsSelected"
        label="Filters hits by ID"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
    </base-table-filter>

    <base-table-filter
      title="Batch Name"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="batchesSelected"
    >
      <v-combobox
        v-model="filters.batchesSelected"
        label="Filters batches by name"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
    </base-table-filter>
  </v-layout>
</template>

<script>
import BaseTableFilter from '../../base-table-filter';

export default {
  name: 'FiltersTableHits',
  components: {BaseTableFilter},
  props: {
    filters: {
      required: true,
      type: Object,
    },
    filtersActive: {
      required: true,
      type: Object,
    },
  },
};
</script>

<style scoped>

</style>