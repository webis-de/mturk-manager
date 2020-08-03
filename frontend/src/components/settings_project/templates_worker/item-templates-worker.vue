<template>
  <base-table-item
    v-bind:key="templateWorker.id"
    v-bind:item="item"
  >
    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="heightFrame"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.heightFrame }} px
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="countParameters"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ Object.keys(item.dictParameters).length }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateAssignment"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="item.templateAssignment === null">
        None
      </span>
      <span v-else>
        {{ item.templateAssignment.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateHIT"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="item.templateHIT === null">
        None
      </span>
      <span v-else>
        {{ item.templateHIT.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateGlobal"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="item.templateGlobal === null">
        None
      </span>
      <span v-else>
        {{ item.templateGlobal.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateGlobal"
      v-bind:item="templateWorker"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-edit-template-worker
        v-bind:key="`component-edit-template-worker-${item.id}`"
        v-bind:template-worker-current="item"
        v-on:edited="$emit('edited')"
      />
      <component-delete-template-worker
        v-bind:key="`component-delete-template-worker-${item.id}`"
        v-bind:template-worker="item"
        v-bind:disabled="item.has_assignments === true"
        v-on:deleted="snackbar_deleted = true"
      />
    </base-table-cell>
  </base-table-item>
</template>

<script>
import ComponentEditTemplateWorker from './component_edit_template_worker';
import ComponentDeleteTemplateWorker from './component_delete_template_worker';
import { TemplateWorker } from '../../../modules/template/templateWorker.model';
import BaseTableCell from '../../base-table-cell';
import BaseTableItem from '../../base-table-item';

export default {
  name: 'ItemTemplatesWorker',
  components: { BaseTableItem, BaseTableCell, ComponentDeleteTemplateWorker, ComponentEditTemplateWorker },
  props: {
    item: {
      type: TemplateWorker,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
  },
  computed: {
    templateWorker() { return this.item; },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: 'unset !important',
          paddingLeft: '5px !important',
          paddingRight: '5px !important',
        };
      }
      return {};
    },
  },
};
</script>

<style scoped>
</style>
