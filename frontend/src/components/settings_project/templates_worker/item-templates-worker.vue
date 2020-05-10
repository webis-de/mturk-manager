<template>
  <tr>
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ templateWorker.name }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      {{ templateWorker.heightFrame }} px
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      {{ Object.keys(templateWorker.dictParameters).length }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <span v-if="templateWorker.templateAssignment === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.templateAssignment.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <span v-if="templateWorker.templateHIT === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.templateHIT.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <span v-if="templateWorker.templateGlobal === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.templateGlobal.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-end px-1 text-no-wrap"
    >
      <component-edit-template-worker
        v-bind:key="`component-edit-template-worker-${templateWorker.id}`"
        v-bind:template-worker-current="templateWorker"
        v-on:edited="$emit('edited')"
      />
      <component-delete-template-worker
        v-bind:key="`component-delete-template-worker-${item.id}`"
        v-bind:template-worker="item"
        v-bind:disabled="templateWorker.has_assignments === true"
        v-on:deleted="snackbar_deleted = true"
      />
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateWorker from './component_edit_template_worker';
import ComponentDeleteTemplateWorker from './component_delete_template_worker';
import { TemplateWorker } from '../../../modules/template/templateWorker.model';

export default {
  name: 'ItemTemplatesWorker',
  components: { ComponentDeleteTemplateWorker, ComponentEditTemplateWorker },
  props: {
    item: {
      type: TemplateWorker,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
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
