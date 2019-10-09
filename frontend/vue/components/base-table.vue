<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-data-table
    show-select
    v-bind:headers="arrayHeaders"
    v-bind:items="arrayItems"
    v-bind:server-items-length="items_total"
    v-bind:loading="loading"
    item-key="id"
    v-bind:dense="isCondensed"
    header-key="value"
    v-bind:items-per-page="pagination.itemsPerPage"
    v-bind:page="page"
    v-bind:sort-by="pagination.sortBy"
    v-bind:sort-desc="pagination.sortDesc"
    must-sort

    v-bind:footer-props="{
      'items-per-page-options': [5, 10, 25, { text: 'All', value: null }]
    }"

    v-on:update:options="updatedOptions($event)"
  >
    <template
      v-slot:header.data-table-select
    >
      <v-checkbox
        class="pa-0 ma-0"
        primary
        hide-details
        v-on:change="toggle_all"
      />
    </template>
<!--        <template-->
<!--          v-for="slot in arraySlotsItems"-->
<!--          v-slot:[slot]-->
<!--        >-->
<!--          <slot v-bind:name="slot"></slot>-->
<!--        </template>-->

<!--        <template-->
<!--          slot="headers"-->
<!--          slot-scope="props"-->
<!--        >-->
<!--          <tr>-->
<!--            <th-->
<!--              v-if="nameStateItemsSelected !== undefined"-->
<!--            >-->
<!--              <v-checkbox-->
<!--                v-bind:input-value="is_page_selected"-->
<!--                v-bind:indeterminate="props.indeterminate"-->
<!--                primary-->
<!--                hide-details-->
<!--                v-on:click.native="toggle_all()"-->
<!--              />-->
<!--            </th>-->
<!--            <th-->
<!--              v-for="header in props.headers"-->
<!--              v-bind:key="header.value"-->
<!--              v-bind:class="[-->
<!--                'column',-->
<!--                { sortable: header.sortable !== false },-->
<!--                pagination.sortDesc ? 'desc' : 'asc',-->
<!--                header.value === pagination.sortBy ? 'active' : '',-->
<!--                ...header.classes,-->
<!--              ]"-->
<!--              v-bind:style="{-->
<!--                width: header.width,-->
<!--              }"-->
<!--              v-on="-->
<!--                header.sortable !== false-->
<!--                  ? {-->
<!--                    click: () => {-->
<!--                      updatedPagination({-->
<!--                        sortBy: header.value,-->
<!--                        sortDesc: !pagination.sortDesc,-->
<!--                        page: 1,-->
<!--                        itemsPerPage: pagination.itemsPerPage,-->
<!--                      });-->
<!--                    }-->
<!--                  }-->
<!--                  : {}-->
<!--              "-->
<!--            >-->
<!--              {{ header.text }}-->
<!--              <v-icon-->
<!--                v-if="header.sortable !== false"-->
<!--                small-->
<!--                style="position: absolute"-->
<!--              >-->
<!--                arrow_upward-->
<!--              </v-icon>-->
<!--            </th>-->
<!--          </tr>-->
<!--        </template>-->

    <template
      v-slot:item="{ item }"
    >
      <slot
        v-bind:item="item"
        v-bind:objectColumnsSelected="columnsSelected"
        v-bind:is-condensed="isCondensed"
        v-bind:refresh="refresh"
      />
    </template>

    <template
      v-if="showFooter"
      v-slot:top
    >
      <v-row
        dense
        align="center"
      >
        <v-col
          class="py-0 pl-5 headline"
        >
          {{ title }}
        </v-col>
        <v-col class="shrink">
          <slot
            name="actions"
            v-bind:refresh="refresh"
          />
        </v-col>
        <v-col class="shrink">
          <base-table-filters
            v-if="filters !== undefined"

            v-bind:filters="filters"
            v-bind:filters-default="filtersDefault"
            v-bind:name-state-filters="nameStateFilters"
            v-bind:name-local-storage-filters="nameLocalStorageFilters"
            v-bind:set-state="setState"

            v-on:filtersChanged="updatedPagination({
              sortBy: pagination.sortBy,
              sortDesc: pagination.sortDesc,
              page: 1,
              itemsPerPage: pagination.itemsPerPage,
            })"
          >
            <template
              v-slot:filters="{ filters, filtersActive }"
            >
              <slot
                name="filters"
                v-bind:filters="filters"
                v-bind:filters-active="filtersActive"
              />
            </template>
          </base-table-filters>
        </v-col>
        <v-col class="shrink pr-2">
          <component-settings-table
            v-if="nameLocalStorageColumnsSelected !== undefined"
            v-bind:colspan="arrayHeaders.length + 1"
            v-bind:columns="columns"
            v-bind:object-columns-selected="columnsSelected"

            v-bind:name-vuex-module="nameVuexModule"
            v-bind:name-state-columns-selected="nameStateColumnsSelected"
            v-bind:name-state-columns-selected-initial="nameStateColumnsSelectedInitial"
            v-bind:name-local-storage-columns-selected="nameLocalStorageColumnsSelected"
          />
        </v-col>
      </v-row>
    </template>
  </v-data-table>
</template>

<script>
import * as _ from 'lodash';
import { updateSandbox } from '../mixins/update-sandbox.mixin';
import ComponentSettingsTable from './common/component-settings-table';
import BaseTableFilters from './base-table-filters';

export default {
  name: 'BaseTable',
  components: {BaseTableFilters, ComponentSettingsTable },
  mixins: [updateSandbox],
  props: {
    title: {
      required: false,
      type: String,
      default: null,
    },
    nameVuexModule: {
      required: true,
      type: String,
    },
    // Pagination
    nameStatePagination: {
      required: true,
      type: String,
    },
    nameLocalStoragePagination: {
      required: true,
      type: String,
    },
    // Selected columns
    nameStateColumns: {
      required: true,
      type: String,
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: undefined,
    },
    nameStateColumnsSelected: {
      required: true,
      type: String,
    },
    nameStateColumnsSelectedInitial: {
      required: false,
      type: String,
      default: undefined,
    },
    // Selected Items
    nameStateItemsSelected: {
      required: false,
      type: String,
      default: undefined,
    },





    arrayItems: {
      type: Array,
      required: true,
    },
    functionLoadPage: {
      type: Function,
      required: true,
    },

    functionSetItemsSelected: {
      type: Function,
      required: false,
      default: undefined,
    },
    functionClearItemsSelected: {
      type: Function,
      required: false,
      default: () => {},
    },

    // filters: {
    //   required: false,
    //   type: Object,
    //   default: () => {},
    // },

    isCondensed: {
      required: false,
      type: Boolean,
      default: true,
    },

    filters: {
      required: false,
      type: Object,
      default: () => {},
    },
    filtersDefault: {
      required: false,
      type: Object,
      default: () => {},
    },
    nameStateFilters: {
      required: false,
      type: String,
      default: '',
    },
    nameLocalStorageFilters: {
      required: false,
      type: String,
      default: '',
    },
    setState: {
      required: false,
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      // pagination: {
      //   itemsPerPage: 25,
      //   sortDesc: true,
      // },
      loading: false,
      search: '',
      items_total: undefined,
      page: 1,

      columns: this.$store.state[this.nameVuexModule][this.nameStateColumns],
    };
  },
  computed: {
    columnsSelected() {
      if (this.$store.state[this.nameVuexModule][this.nameStateColumnsSelected] === null) {
        return this.$store.state[this.nameVuexModule][this.nameStateColumnsSelectedInitial];
      }

      return this.$store.state[this.nameVuexModule][this.nameStateColumnsSelected];
    },
    pagination: {
      get() {
        return _.assign(
          {},
          this.$store.state[this.nameVuexModule][this.nameStatePagination],
          { totalItems: 0, page: this.page },
        );
      },
    },
    showFooter() {
      return this.$scopedSlots.actions !== undefined || this.nameLocalStorageColumnsSelected !== undefined;
    },
    arrayHeaders() {
      return _.filter(this.columns, column => this.columnsSelected.hasOwnProperty(column.value));
    },
    is_page_selected() {
      let isPageSelected = true;

      if (_.size(this.arrayItems) === 0) {
        return false;
      }

      _.forEach(this.arrayItems, (item) => {
        if (!_.has(this.$store.state[this.nameVuexModule][this.nameStateItemsSelected], item.id)) {
          isPageSelected = false;
          return false;
        }
        return true;
      });

      return isPageSelected;
    },
  },
  beforeDestroy() {
    this.functionClearItemsSelected();

    // this.pagination.page = 1;

    this.$store.dispatch(`${this.nameVuexModule}/setState`, {
      objectState: _.pick(this.pagination, ['sortBy', 'sortDesc', 'itemsPerPage']),
      nameState: this.nameStatePagination,
      nameLocalStorage: this.nameLocalStoragePagination,
    });
  },
  methods: {
    updatedOptions(options, force = false) {
      const equalOptions = _.isEqual(
        _.pick(options, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
        _.pick(this.pagination, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
      );
      console.warn('options', options);
      if (equalOptions === false || force === true) {
        this.$store.dispatch(`${this.nameVuexModule}/setState`, {
          objectState: _.pick(options, ['sortBy', 'sortDesc', 'itemsPerPage']),
          nameState: this.nameStatePagination,
          nameLocalStorage: this.nameLocalStoragePagination,
        });

        this.page = options.page;

        this.$nextTick(() => {
          this.load_page(this.filters);
        });
      }
    },
    refresh() {
      this.pagination.page = 1;
      this.load_page(this.filters);
    },
    // Reset pagination/load page if the sandbox status was changed
    sandboxUpdated() {
      this.updatedOptions({
        ...this.pagination,
        page: 1,
      }, true);

      // console.warn('this.pagination.page', this.pagination.page);
      // return;
      // if (this.pagination.page !== 1) {
      //   this.pagination.page = 1;
      // } else {
      //   this.load_page(this.filters);
      // }
    },
    updatedPagination(pagination) {
      // const equalPagination = _.isEqual(
      //   _.pick(pagination, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
      //   _.pick(this.pagination, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
      // );

      // only update if pagination changed
      // if (equalPagination === false) {
      //   this.page = 1;
        // this.page = pagination.page;

        this.$store.dispatch(`${this.nameVuexModule}/setState`, {
          objectState: _.pick(pagination, ['sortBy', 'sortDesc', 'itemsPerPage']),
          nameState: this.nameStatePagination,
          nameLocalStorage: this.nameLocalStoragePagination,
        });
      // }

      this.$nextTick(() => {
        this.load_page(this.filters);
      });
    },
    load_page(filters) {
      this.loading = true;
      this.functionLoadPage(this.pagination, filters).then(
        (itemsTotal) => {
          this.items_total = itemsTotal;
          this.loading = false;
        },
      );
    },
    toggle_all() {
      this.functionSetItemsSelected({
        add: !this.is_page_selected,
        array_items: this.arrayItems,
      });
    },
  },
  created() {
    this.load_page(this.filters);
  },
};
</script>

<style lang="scss" scoped></style>
