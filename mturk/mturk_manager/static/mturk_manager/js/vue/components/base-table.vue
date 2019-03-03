<template>
  <div>
    <v-data-table
      select-all
      v-bind:headers="array_headers"
      v-bind:items="array_page"
      v-bind:total-items="items_total"
      v-bind:loading="loading"
      item-key="id"
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
            v-if="objectItemsSelected !== undefined"
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
            v-bind:width="header.width"
            v-bind:class="[
              'column',
              { sortable: header.sortable !== false },
              pagination.descending ? 'desc' : 'asc',
              header.value === pagination.sortBy ? 'active' : ''
            ]"
            v-bind:style="stylesHeaderCell"
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
            <v-icon
              v-if="header.sortable !== false"
              small
            >
              arrow_upward
            </v-icon>
            {{ header.text }}
          </th>
        </tr>
      </template>

      <template
        slot="items"
        slot-scope="props"
      >
        <slot
          v-bind:props="props"
          v-bind:array_columns_selected="arrayColumnsSelected"
          v-bind:is-condensed="isCondensed"
        />
      </template>

      <template
        v-if="showFooter"
        slot="footer"
      >
        <tr>
          <slot name="footer" />
          <component-settings-table
            v-if="functionResetArrayColumns !== undefined"
            v-bind:colspan="array_headers.length + 1"
            v-bind:array_columns="arrayColumns"
            v-bind:array_columns_selected="arrayColumnsSelected"
            v-bind:function_reset="functionResetArrayColumns"
            v-on:change="functionSetArrayColumns($event)"
          />
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import * as _ from 'lodash';
import { update_sandbox as updateSandbox } from '../mixins/update_sandbox';
import { table } from '../mixins/table';
import ComponentSettingsTable from './helpers/component-settings-table';

export default {
  name: 'BaseTable',
  components: { ComponentSettingsTable },
  mixins: [updateSandbox, table],
  props: {
    arrayItems: {
      type: Function,
      required: true,
    },
    functionLoadPage: {
      type: Function,
      required: true,
    },

    arrayColumns: {
      type: Array,
      required: true,
    },
    arrayColumnsSelected: {
      type: Array,
      required: true,
    },

    functionResetArrayColumns: {
      type: Function,
      required: false,
      default: undefined,
    },
    functionSetArrayColumns: {
      type: Function,
      required: false,
      default: undefined,
    },

    objectItemsSelected: {
      type: Object,
      required: false,
      default: undefined,
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

    filters: {
      required: false,
      type: Object,
      default: () => {},
    },

    isCondensed: {
      required: false,
      type: Boolean,
      default: true,
    },

    paginationComputed: {
      type: Object,
      required: true,
    },
    functionSetPagination: {
      type: Function,
      required: true,
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
    };
  },
  computed: {
    pagination: {
      get() {
        return _.assign({}, this.paginationComputed, {totalItems: 0});
      },
      // set(value) {
      //     console.warn('computed');
      //   this.functionSetPagination(value);
      // },
    },
    showFooter() {
      return this.$scopedSlots.footer !== undefined
        || this.functionResetArrayColumns !== undefined;
    },
    array_headers() {
      const set = new Set(this.arrayColumnsSelected);
      return _.filter(this.arrayColumns, column => set.has(column.value));
    },
    is_page_selected() {
      let isPageSelected = true;

      if (_.size(this.array_page) === 0) {
        return false;
      }

      _.forEach(this.array_page, (item) => {
        if (!_.has(this.objectItemsSelected, item.id)) {
          isPageSelected = false;
          return false;
        }
        return true;
      });

      return isPageSelected;
    },
    array_page() {
      const arrayItems = this.arrayItems();
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
    this.functionSetPagination({
      undefined,
      setPageTo1: true,
    });
  },
  methods: {
    updatedPagination(pagination) {
      // only update if pagination changed
      if (!_.isEqual(
        _.pick(pagination, ['page', 'rowsPerPage', 'sortBy', 'descending']),
        _.pick(this.pagination, ['page', 'rowsPerPage', 'sortBy', 'descending']),
      )) {
        this.functionSetPagination({
          pagination,
        });
      }

      this.$nextTick(() => {
        this.load_page();
      });
    },
    load_page() {
      this.loading = true;
      this.functionLoadPage(this.pagination, this.filters).then(
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
