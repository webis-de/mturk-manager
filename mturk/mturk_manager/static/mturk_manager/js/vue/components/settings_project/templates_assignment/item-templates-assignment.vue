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
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <component-edit-template-assignment
        v-bind:key="`component-edit-template-assignment-${templateAssignment.id}`"
        v-bind:template_assignment_current="templateAssignment"
        v-on:edited="$emit('edited')"
      ></component-edit-template-assignment>
      <component-delete-template-assignment
        v-bind:key="
          `component-delete-template-assignment-${templateAssignment.id}`
        "
        v-bind:template_assignment="templateAssignment"
        v-on:deleted="$emit('deleted')"
      ></component-delete-template-assignment>
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateAssignment from './component_edit_template_assignment';
import ComponentDeleteTemplateAssignment from './component_delete_template_assignment';

export default {
  name: 'ItemTemplatesAssignment',
  components: {ComponentDeleteTemplateAssignment, ComponentEditTemplateAssignment},
  props: {
    props: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  computed: {
    templateAssignment() { return this.props.item; },
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