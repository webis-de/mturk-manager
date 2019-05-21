<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-data-table
    select-all
    v-bind:headers="array_headers"
    v-bind:items="array_page"
    v-bind:total-items="items_total"
    v-bind:loading="loading"
    item-key="id"
    header-key="value"
    v-bind:rows-per-page-items="[5, 10, 25, { text: 'All', value: null }]"
    v-bind:pagination="pagination"
    v-on:update:pagination="updatedPagination($event)"
  >
    <template
      slot="headers"
      slot-scope="props"
    >
      <tr v-bind:style="stylesHeaderRow">
        <th
          v-if="nameStateItemsSelected !== undefined"
          v-bind:style="stylesHeaderCell"
        >
          <v-checkbox
            v-bind:input-value="is_page_selected"
            v-bind:indeterminate="props.indeterminate"
            primary
            hide-details
            v-on:click.native="toggle_all()"
          />
        </th>
        <th
          v-for="header in props.headers"
          v-bind:key="header.value"
          v-bind:class="[
            'column',
            { sortable: header.sortable !== false },
            pagination.descending ? 'desc' : 'asc',
            header.value === pagination.sortBy ? 'active' : '',
            ...header.classes,
          ]"
          v-bind:style="{
            ...stylesHeaderCell,
            width: header.width,
          }"
          v-on="
            header.sortable !== false
              ? {
                click: () => {
                  updatedPagination({
                    sortBy: header.value,
                    descending: !pagination.descending,
                    page: 1,
                    rowsPerPage: pagination.rowsPerPage,
                  });
                }
              }
              : {}
          "
        >
          {{ header.text }}
          <v-icon
            v-if="header.sortable !== false"
            small
            style="position: absolute"
          >
            arrow_upward
          </v-icon>
        </th>
      </tr>
    </template>

    <template
      slot="items"
      slot-scope="props"
    >
      <slot
        v-bind:props="props"
        v-bind:array_columns_selected="columnsSelected"
        v-bind:is-condensed="isCondensed"
        v-bind:refresh="refresh"
      />
    </template>

    <template
      v-if="showFooter"
      slot="actions-prepend"
    >
      <v-layout>
        <v-flex>
          <slot name="actions"
            v-bind:refresh="refresh"
          />
        </v-flex>
        <v-flex>
          <base-table-filters
            v-if="filters !== undefined"

            v-bind:filters="filters"
            v-bind:filters-default="filtersDefault"
            v-bind:name-state-filters="nameStateFilters"
            v-bind:name-local-storage-filters="nameLocalStorageFilters"
            v-bind:set-state="setState"

            v-on:filtersChanged="updatedPagination({
              sortBy: pagination.sortBy,
              descending: !pagination.descending,
              page: 1,
              rowsPerPage: pagination.rowsPerPage,
            }, true);"
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
        </v-flex>
        <v-flex>
          <component-settings-table
            v-if="nameLocalStorageColumnsSelected !== undefined"
            v-bind:colspan="array_headers.length + 1"
            v-bind:columns="columns"
            v-bind:columns-selected="columnsSelected"

            v-bind:name-vuex-module="nameVuexModule"
            v-bind:name-state-columns-selected="nameStateColumnsSelected"
            v-bind:name-state-columns-selected-initial="nameStateColumnsSelectedInitial"
            v-bind:name-local-storage-columns-selected="nameLocalStorageColumnsSelected"
          />
          </v-flex>
        </v-layout>
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
      type: Array | Function | null,
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
      //   rowsPerPage: 25,
      //   descending: true,
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
        return _.assign({}, this.$store.state[this.nameVuexModule][this.nameStatePagination], {totalItems: 0, page: this.page});
      },
    },
    showFooter() {
      return this.$scopedSlots.actions !== undefined || this.nameLocalStorageColumnsSelected !== undefined;
    },
    array_headers() {
      const set = new Set(this.columnsSelected);
      return _.filter(this.columns, column => set.has(column.value));
    },
    is_page_selected() {
      let isPageSelected = true;

      if (_.size(this.array_page) === 0) {
        return false;
      }

      _.forEach(this.array_page, (item) => {
        if (!_.has(this.$store.state[this.nameVuexModule][this.nameStateItemsSelected], item.id)) {
          isPageSelected = false;
          return false;
        }
        return true;
      });

      return isPageSelected;
    },
    array_page() {
      let arrayItems = this.arrayItems;

      if (_.isFunction(this.arrayItems)) {
        arrayItems = this.arrayItems();
      }

      return arrayItems === null ? [] : arrayItems;
    },
    stylesHeaderRow() {
      return {
        height: this.isCondensed ? 'unset' : null,
      };
    },
    stylesHeaderCell() {
      return {
        padding: this.isCondensed ? '5px' : null,
      };
    },
  },
  beforeDestroy() {
    this.functionClearItemsSelected();

    // this.pagination.page = 1;

    this.$store.dispatch(`${this.nameVuexModule}/setState`, {
      objectState: _.pick(this.pagination, ['sortBy', 'descending', 'rowsPerPage']),
      nameState: this.nameStatePagination,
      nameLocalStorage: this.nameLocalStoragePagination,
    });
  },
  methods: {
    refresh() {
      this.pagination.page = 1;
      this.load_page(this.filters);
    },
    // Reset pagination/load page if the sandbox status was changed
    sandboxUpdated() {
      if (this.pagination.page !== 1) {
        this.pagination.page = 1;
      } else {
        this.load_page(this.filters);
      }
    },
    updatedPagination(pagination) {
      const equalPagination = _.isEqual(
        _.pick(pagination, ['page', 'rowsPerPage', 'sortBy', 'descending']),
        _.pick(this.pagination, ['page', 'rowsPerPage', 'sortBy', 'descending']),
      );

      // only update if pagination changed
      if (equalPagination === false) {
        this.page = pagination.page;

        this.$store.dispatch(`${this.nameVuexModule}/setState`, {
          objectState: _.pick(pagination, ['sortBy', 'descending', 'rowsPerPage']),
          nameState: this.nameStatePagination,
          nameLocalStorage: this.nameLocalStoragePagination,
        });
      }

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
        array_items: this.array_page,
      });
    },
  },
};
</script>

<style lang="scss" scoped></style>
