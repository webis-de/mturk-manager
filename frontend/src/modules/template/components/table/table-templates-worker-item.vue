<template>
  <base-table-item
    v-bind:key="template.id"
    v-bind:item="template"
  >
    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="heightFrame"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.heightFrame }} px
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="countParameters"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ Object.keys(item.dictParameters).length }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateAssignment"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="templateAssignment === null">
        None
      </span>
      <span v-else>
        {{ templateAssignment.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateHIT"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="templateHIT === null">
        None
      </span>
      <span v-else>
        {{ templateHIT.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="templateGlobal"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <span v-if="templateGlobal === null">
        None
      </span>
      <span v-else>
        {{ templateGlobal.name }}
      </span>
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-left text-capitalize"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <update-template-worker v-bind:template="template" />
      <delete-template-worker v-bind:template="template" />
    </base-table-cell>
  </base-table-item>
</template>

<script lang="ts">
import BaseTableCell from '@/components/base-table-cell';
import DeleteTemplateWorker from '@/modules/template/components/delete/delete-template-worker.vue';
import UpdateTemplateWorker from '@/modules/template/components/update/update-template-worker.vue';
import BaseTableItem from '../../../../components/base-table-item';

export default {
  name: 'TableTemplatesWorkerItem',
  components: {
    UpdateTemplateWorker,
    DeleteTemplateWorker,
    BaseTableCell,
    BaseTableItem,
  },
  props: {
    template: {
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
    templateAssignment() {
      if (this.template.templateAssignment === null) return null;

      return this.$store.state.moduleTemplates.templatesAssignment[this.template.templateAssignment];
    },
    templateHIT() {
      if (this.template.templateHIT === null) return null;

      return this.$store.state.moduleTemplates.templatesHIT[this.template.templateHIT];
    },
    templateGlobal() {
      if (this.template.templateGlobal === null) return null;

      return this.$store.state.moduleTemplates.templatesGlobal[this.template.templateGlobal];
    },
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
