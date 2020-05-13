<template>
  <base-table-item
    v-bind:key="templateAssignment.id"
    v-bind:item="item"
  >
    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="templateAssignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="templateAssignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ type }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="templateAssignment"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <component-edit-template-assignment
        v-bind:key="`component-edit-template-assignment-${item.id}`"
        v-bind:template_assignment_current="templateAssignment"
        v-on:edited="$emit('edited')"
      />
      <component-delete-template-assignment
        v-bind:key="
          `component-delete-template-assignment-${templateAssignment.id}`
        "
        v-bind:template_assignment="templateAssignment"></component-delete-template-assignment>
    </base-table-cell>
  </base-table-item>
</template>

<script>
import ComponentEditTemplateAssignment from './component_edit_template_assignment';
import ComponentDeleteTemplateAssignment from './component_delete_template_assignment';
import BaseTableItem from '../../base-table-item';
import BaseTableCell from '../../base-table-cell';
import { TemplateHIT } from '../../../modules/template/templateHIT.model';
import { TemplateGlobal } from '../../../modules/template/templateGlobal.model';

export default {
  name: 'ItemTemplatesAssignment',
  components: { BaseTableCell, BaseTableItem, ComponentDeleteTemplateAssignment, ComponentEditTemplateAssignment },
  props: {
    item: {
      type: Object,
      required: true,
    },
    objectColumnsSelected: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  computed: {
    type() {
      let type = 'Assignment';
      if (this.item instanceof TemplateHIT) type = 'HIT';
      else if (this.item instanceof TemplateGlobal) type = 'Global';
      return type;
    },
    templateAssignment() { return this.item; },
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
