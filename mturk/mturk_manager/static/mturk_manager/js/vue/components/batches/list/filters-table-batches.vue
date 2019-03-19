<template>
  <v-layout wrap>
    <base-table-filter
      title="Batch ID"
      v-bind:filters-active="filtersActive"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="batchesSelected"
    >
      <v-combobox
        v-model="filters.batchesSelected"
        label="Filters batches by ID"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
      <!--<v-combobox-->
        <!--v-model="filters.show_only_submitted_assignments"-->
        <!--label="Search by Worker ID"-->
        <!--multiple-->
        <!--chips-->
        <!--deletable-chips-->
        <!--clearable-->
        <!--hide-details-->
        <!--dense-->
      <!--/>-->
    </base-table-filter>
  </v-layout>
</template>

<script>
import BaseTableFilter from '../../base-table-filter';

export default {
  name: 'FiltersTableBatches',
  components: { BaseTableFilter },
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