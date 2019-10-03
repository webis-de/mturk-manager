<template>
  <td
    v-bind:class="classesCell"
  >
    <slot
      v-bind:item="item"
    />
  </td>
</template>

<script>
export default {
  name: 'BaseTableCell',
  props: {
    name: {
      required: true,
      type: String,
    },
    item: {
      required: true,
      type: Object,
    },
    columnsSelected: {
      required: true,
      type: Object,
    },
  },
  computed: {
    classesCell() {
      return {
        'hidden-sm-and-up': !this.show,
        'hidden-xs-only': !this.show,
      };
    },
    show() {
      return this.columnsSelected.hasOwnProperty(this.name);
    },
  },
};
</script>

<style scoped>

</style>
