<template>
  <tr>
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ templateHIT.name }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <component-edit-template-hit
        v-bind:key="`component-edit-template-hit-${templateHIT.id}`"
        v-bind:template_hit_current="templateHIT"
        v-on:edited="$emit('edited')"
      ></component-edit-template-hit>
      <component-delete-template-hit
        v-bind:key="
          `component-delete-template-hit-${templateHIT.id}`
        "
        v-bind:template_hit="templateHIT"
        v-on:deleted="$emit('deleted')"
      ></component-delete-template-hit>
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateHit from './component_edit_template_hit';
import ComponentDeleteTemplateHit from './component_delete_template_hit';

export default {
  name: 'ItemTemplatesHit',
  components: {
    ComponentDeleteTemplateHit,
    ComponentEditTemplateHit,
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
    templateHIT() { return this.item; },
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
