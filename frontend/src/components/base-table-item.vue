<template>
  <tr
    class="text-no-wrap roboto-mono table-row"
  >
    <td
      v-if="itemsSelected !== null"
      class="px-3"
    >
      <base-table-checkbox
        v-model="isSelected"
      />
    </td>

    <slot></slot>
  </tr>
</template>

<script>
import BaseTableCheckbox from './base-table-checkbox';

export default {
  name: 'BaseTableItem',
  components: { BaseTableCheckbox },
  props: {
    item: {
      required: true,
      type: Object,
    },
    itemsSelected: {
      type: Object,
      required: false,
      default: null,
    },
  },
  computed: {
    isSelected: {
      get() {
        return this.itemsSelected !== false && (this.itemsSelected === true || this.itemsSelected[this.item.id] !== undefined);
      },
      set(isSelected) {
        this.$emit('changed-selection', {
          isSelected,
          item: this.item,
        });
      },
    },
  },
};
</script>

<style scoped>

</style>
