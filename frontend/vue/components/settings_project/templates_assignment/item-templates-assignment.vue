<template>
  <tr>
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ templateAssignment.name }}
    </td>
    <td
      v-bind:style="{
        ...stylesCell,
      }"
      class="text-end px-1"
    >
      {{ type }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center text-no-wrap"
    >
      <component-edit-template-assignment
        v-bind:key="`component-edit-template-assignment-${templateAssignment.id}`"
        v-bind:template_assignment_current="templateAssignment"
        v-on:edited="$emit('edited')"
      />
      <component-delete-template-assignment
        v-bind:key="
          `component-delete-template-assignment-${templateAssignment.id}`
        "
        v-bind:template_assignment="templateAssignment"
        v-on:deleted="$emit('deleted')"
      />
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateAssignment from './component_edit_template_assignment';
import ComponentDeleteTemplateAssignment from './component_delete_template_assignment';
import Template_HIT from '../../../classes/template_hit';
import Template_Global from '../../../classes/template_global';

export default {
  name: 'ItemTemplatesAssignment',
  components: { ComponentDeleteTemplateAssignment, ComponentEditTemplateAssignment },
  props: {
    item: {
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
      if (this.item instanceof Template_HIT) type = 'HIT';
      else if (this.item instanceof Template_Global) type = 'Global';
      return type;
    },
    templateAssignment() { console.warn('this.item', this.item); return this.item; },
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
