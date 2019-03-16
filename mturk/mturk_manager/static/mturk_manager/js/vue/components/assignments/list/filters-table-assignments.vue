<template>
  <v-layout wrap>
    <base-table-filter
      title="Show Only Submitted Assignments"
      v-bind:filters-active="filtersActive"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="show_only_submitted_assignments"
    >
      <v-switch
        v-model="filters.show_only_submitted_assignments"
        label="Only Submitted"
        hide-details
        class="mt-0"
      ></v-switch>
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
  name: 'FiltersTableAssignments',
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