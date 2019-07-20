<template>
  <td
    v-bind:style="stylesCell"
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
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  computed: {
    classesCell() {
      return {
        'hidden-sm-and-up': !this.show,
        'hidden-xs-only': !this.show,
      };
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
    show() {
      return this.columnsSelected.hasOwnProperty(this.name);
    },
  },
};
</script>

<style scoped>

</style>
