<template>
  <base-table-item
    v-bind:key="template.id"
    v-bind:item="template"
  >
    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize first-column"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.name }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="name"
      class="text-left text-capitalize"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      {{ item.type }}
    </base-table-cell>

    <base-table-cell
      v-slot="{ item }"
      name="actions"
      class="text-left text-capitalize"
      v-bind:item="template"
      v-bind:columns-selected="objectColumnsSelected"
    >
      <update-template-requester v-bind:template="template" />
      <delete-template-requester v-bind:template="template" />
    </base-table-cell>
  </base-table-item>
</template>

<script lang="ts">
import BaseTableCell from '@/components/base-table-cell';
import UpdateTemplateRequester from '@/modules/template/components/update/update-template-requester.vue';
import DeleteTemplateRequester from '@/modules/template/components/delete/delete-template-requester.vue';
import BaseTableItem from '../../../../components/base-table-item';

export default {
  name: 'TableTemplatesRequesterItem',
  components: {
    DeleteTemplateRequester,
    UpdateTemplateRequester,
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
