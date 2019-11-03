<template>
  <tr>
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ templateGlobal.name }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <component-edit-template-global
        v-bind:key="`component-edit-template-global-${templateGlobal.id}`"
        v-bind:template_global_current="templateGlobal"
        v-on:edited="$emit('edited')"
      ></component-edit-template-global>
      <component-delete-template-global
        v-bind:key="
          `component-delete-template-global-${templateGlobal.id}`
        "
        v-bind:template_global="templateGlobal"
        v-on:deleted="$emit('deleted')"
      ></component-delete-template-global>
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateGlobal from './component_edit_template_global';
import ComponentDeleteTemplateGlobal from './component_delete_template_global';

export default {
  name: 'ItemTemplatesGlobal',
  components: {
    ComponentDeleteTemplateGlobal,
    ComponentEditTemplateGlobal,
},
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
    templateGlobal() { return this.item; },
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
