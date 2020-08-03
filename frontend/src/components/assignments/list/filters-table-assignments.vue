<template>
  <v-layout wrap>
    <base-table-filter
      title="Assignment ID"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="assignmentsSelected"
    >
      <v-combobox
        v-model="filters.assignmentsSelected"
        label="Filters assignments by ID"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
    </base-table-filter>

    <base-table-filter
      title="HIT ID"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="hitsSelected"
    >
      <v-combobox
        v-model="filters.hitsSelected"
        label="Filters HITs by ID"
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

    <base-table-filter
      title="Worker ID"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="workersSelected"
    >
      <v-combobox
        v-model="filters.workersSelected"
        label="Filters workers by ID"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
    </base-table-filter>

    <base-table-filter
      title="Show Only Submitted Assignments"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
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