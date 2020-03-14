<template>
  <tr
    class="text-no-wrap"
    v-bind:class="classes"
  >
    <td>
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
      required: true,
    },
  },
  data() {
    return {
      classes: ['roboto-mono'],
    };
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
