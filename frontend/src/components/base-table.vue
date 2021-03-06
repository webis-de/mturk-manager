<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-data-table
    v-intersect.once="onIntersect"
    v-bind:show-select="showSelect"
    v-bind:headers="arrayHeaders"
    v-bind:items="arrayItemsReal"
    v-bind:server-items-length="itemsTotal"
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
    v-bind:style="objectStyles"

    v-on:update:options="updatedOptions($event)"
  >
    <template
      v-slot:header.data-table-select
    >
      <base-table-checkbox
        v-model="isSelectedAll"
        v-bind:indeterminate="isIndeterminate"
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
        v-bind:changed-selection="changedSelection"
        v-bind:items-selected="itemsSelected"
      ></slot>
    </template>

    <template
      v-if="showFooter"
      v-slot:top
    >
      <v-row
        dense
        align="center"
        class="pr-4"
      >
        <v-col
          class="py-0 pl-4 title"
        >
          {{ title }}
        </v-col>
        <v-col class="shrink">
          <slot
            name="actions"
            v-bind:refresh="refresh"
          ></slot>
        </v-col>
        <v-col
          v-if="filters !== undefined"
          class="shrink"
        >
          <base-table-filters
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
              ></slot>
            </template>
          </base-table-filters>
        </v-col>
        <v-col
          v-if="nameLocalStorageColumnsSelected !== undefined"
          class="shrink"
        >
          <component-settings-table

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
import intersect from 'vuetify/lib/directives/intersect';
import { updateSandbox } from '../mixins/update-sandbox.mixin';
import ComponentSettingsTable from './common/component-settings-table';
import BaseTableFilters from './base-table-filters';
import BaseTableCheckbox from './base-table-checkbox';

/**
 * TODO: lazy loading if visible
 */

export default {
  name: 'BaseTable',
  directives: {
    intersect,
  },
  components: { BaseTableCheckbox, BaseTableFilters, ComponentSettingsTable },
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
      type: Array | null,
      required: true,
    },
    functionLoadPage: {
      type: Function,
      required: false,
      default: null,
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

    showSelect: {
      required: false,
      type: Boolean,
      default: true,
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
      itemsTotal: -1,
      page: 1,

      columns: this.$store.state[this.nameVuexModule][this.nameStateColumns],

      itemsSelected: {},
      isWholePageSelected: false,
      isAtLeastOneItemOfPageSelected: false,
    };
  },
  computed: {
    arrayItemsReal() {
      return this.arrayItems === null ? [] : this.arrayItems;
    },
    itemsTotalReal() {
      return this.functionLoadPage === null ? this.arrayItemsReal.length : this.itemsTotal;
    },
    isIndeterminate() {
      return this.isWholePageSelected === false && this.isAtLeastOneItemOfPageSelected === true;
    },
    objectStyles() {
      return {
        'min-height': `${this.heightTable}px`,
      };
    },
    heightTable() {
      let { itemsPerPage } = this.pagination;

      if (this.itemsTotalReal !== null && this.itemsTotal < itemsPerPage) {
        itemsPerPage = this.itemsTotal;
      }

      return itemsPerPage * 25.0
        - 1 // border of last row
        + 32 // thead
        + 36 // headitemsPerPage
        + 37; // footer
    },
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
      return _.filter(this.columns, (column) => Object.prototype.hasOwnProperty.call(this.columnsSelected, column.value));
    },
    // is_page_selected() {
    //   let isPageSelected = true;
    //
    //   if (_.size(this.arrayItems) === 0) {
    //     return false;
    //   }
    //
    //   _.forEach(this.arrayItems, (item) => {
    //     if (!_.has(this.$store.state[this.nameVuexModule][this.nameStateItemsSelected], item.id)) {
    //       isPageSelected = false;
    //       return false;
    //     }
    //     return true;
    //   });
    //
    //   return isPageSelected;
    // },
    isSelectedAll: {
      get() {
        return this.isWholePageSelected;
      },
      set(isSelected) {
        this.changedSelection({
          isSelected,
        });
      },
    },
  },
  watch: {
    itemsSelected: {
      handler() {
        this.recalculateIsWholePageSelected();
        this.recalculateIsAtLeastOneItemOfPageSelected();
      },
    },
    arrayItems: {
      handler() {
        this.recalculateIsWholePageSelected();
        this.recalculateIsAtLeastOneItemOfPageSelected();
      },
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
    recalculateIsWholePageSelected() {
      if (this.arrayItems.length === 0) return false;

      let isWholePageSelected = true;

      for (let i = 0; i < this.arrayItems.length; i += 1) {
        if (this.itemsSelected[this.arrayItems[i].id] === undefined) {
          isWholePageSelected = false;
          break;
        }
      }

      this.isWholePageSelected = isWholePageSelected;
    },
    recalculateIsAtLeastOneItemOfPageSelected() {
      let isAtLeastOneItemOfPageSelected = false;

      for (let i = 0; i < this.arrayItems.length; i += 1) {
        if (this.itemsSelected[this.arrayItems[i].id] !== undefined) {
          isAtLeastOneItemOfPageSelected = true;
          break;
        }
      }

      this.isAtLeastOneItemOfPageSelected = isAtLeastOneItemOfPageSelected;
    },
    onIntersect(entries, observer, isIntersecting) {
      if (isIntersecting === true && this.functionLoadPage !== null) {
        this.load_page(this.filters);
      }
    },
    updatedOptions(options, force = false) {
      const equalOptions = _.isEqual(
        _.pick(options, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
        _.pick(this.pagination, ['page', 'itemsPerPage', 'sortBy', 'sortDesc']),
      );

      if (equalOptions === false || force === true) {
        this.$store.dispatch(`${this.nameVuexModule}/setState`, {
          objectState: _.pick(options, ['sortBy', 'sortDesc', 'itemsPerPage']),
          nameState: this.nameStatePagination,
          nameLocalStorage: this.nameLocalStoragePagination,
        });

        this.page = options.page;

        if (this.functionLoadPage !== null) {
          this.$nextTick(() => {
            this.load_page(this.filters);
          });
        }
      }
    },
    refresh() {
      this.pagination.page = 1;
      if (this.functionLoadPage !== null) {
        this.load_page(this.filters);
      }
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

      if (this.functionLoadPage !== null) {
        this.$nextTick(() => {
          this.load_page(this.filters);
        });
      }
    },
    load_page(filters) {
      this.loading = true;
      this.functionLoadPage(this.pagination, filters).then(
        (itemsTotal) => {
          this.itemsTotal = itemsTotal;
          this.loading = false;
        },
      );
    },
    changedSelection({ isSelected, item }) {
      let arrayItems = [item];
      if (item === undefined) {
        arrayItems = this.arrayItems;
      }

      for (let i = 0; i < arrayItems.length; i += 1) {
        if (isSelected === true) {
          this.$set(this.itemsSelected, arrayItems[i].id, true);
        } else {
          this.$delete(this.itemsSelected, arrayItems[i].id);
        }
      }
      this.$emit('changed-selection', this.itemsSelected);
    },
  },
};
</script>

<style lang="scss" scoped></style>
