<template>
  <v-layout wrap>
    <base-table-filter
      title="Worker ID"
      v-bind:filters-active="filtersActive"
      v-bind:filters="filters"
      v-bind:breakpoints="{'sm12': true, 'md6': true}"
      name-filter="workersSelected"
    >
      <v-combobox
        v-model="filters.workersSelected"
        label="Filter workers by their ID"
        multiple
        chips
        deletable-chips
        clearable
        hide-details
        dense
      />
    </base-table-filter>

    <!--<base-table-filter-->
      <!--title="Worker Blocks"-->
      <!--v-bind:filters-active="filtersActive"-->
      <!--v-bind:breakpoints="{'sm6': true, 'md3': true}"-->
      <!--name-filter="statesBlock"-->
    <!--&gt;-->
      <!--<template v-slot:header>-->
        <!--<v-switch-->
          <!--class="mt-0 pt-0"-->
          <!--v-model="filters.combineWithAnd"-->
          <!--label="Use AND"-->
          <!--hide-details-->
        <!--/>-->
      <!--</template>-->

      <!--<v-layout class="ma-0">-->
        <!--<v-flex-->
          <!--class="pa-0"-->
          <!--shrink-->
        <!--&gt;-->
          <!--<v-switch-->
            <!--v-model="filters.statesBlock"-->
            <!--label="Project Block"-->
            <!--value="block_project"-->
            <!--hide-details-->
          <!--/>-->
        <!--</v-flex>-->
        <!--<v-flex-->
          <!--class="font-weight-bold primary&#45;&#45;text ml-1 pb-0 subheading"-->
          <!--align-self-end-->
        <!--&gt;-->
          <!--{{ filters.combineWithAnd ? 'AND' : 'OR' }}-->
        <!--</v-flex>-->
      <!--</v-layout>-->
      <!--<v-layout class="ma-0">-->
        <!--<v-flex-->
          <!--class="pa-0"-->
          <!--shrink-->
        <!--&gt;-->
          <!--<v-switch-->
            <!--v-model="filters.statesBlock"-->
            <!--label="Soft Block"-->
            <!--value="block_soft"-->
            <!--hide-details-->
          <!--/>-->
        <!--</v-flex>-->
        <!--&lt;!&ndash;<v-flex&ndash;&gt;-->
          <!--&lt;!&ndash;class="font-weight-bold primary&#45;&#45;text ml-1 pb-0 subheading"&ndash;&gt;-->
          <!--&lt;!&ndash;align-self-end&ndash;&gt;-->
        <!--&lt;!&ndash;&gt;&ndash;&gt;-->
          <!--&lt;!&ndash;{{ filters.combineWithAnd ? 'AND' : 'OR' }}&ndash;&gt;-->
        <!--&lt;!&ndash;</v-flex>&ndash;&gt;-->
      <!--</v-layout>-->
      <!--&lt;!&ndash;<v-layout class="ma-0">&ndash;&gt;-->
        <!--&lt;!&ndash;<v-flex&ndash;&gt;-->
          <!--&lt;!&ndash;class="pa-0"&ndash;&gt;-->
        <!--&lt;!&ndash;&gt;&ndash;&gt;-->
          <!--&lt;!&ndash;<v-switch&ndash;&gt;-->
            <!--&lt;!&ndash;v-model="filters.statesBlock"&ndash;&gt;-->
            <!--&lt;!&ndash;label="Hard Block"&ndash;&gt;-->
            <!--&lt;!&ndash;value="block_hard"&ndash;&gt;-->
            <!--&lt;!&ndash;hide-details&ndash;&gt;-->
          <!--&lt;!&ndash;/>&ndash;&gt;-->
        <!--&lt;!&ndash;</v-flex>&ndash;&gt;-->
      <!--&lt;!&ndash;</v-layout>&ndash;&gt;-->
    <!--</base-table-filter>-->
  </v-layout>
</template>

<script>
import BaseTableFilter from '../../base-table-filter';
export default {
  name: 'FiltersTableWorkers',
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