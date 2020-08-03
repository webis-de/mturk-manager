<template>
  <td
    v-if="show"
    v-bind:class="classesCell"
    v-on:click="click"
  >
    <slot
      v-bind:item="item"
    ></slot>
  </td>
</template>

<script>
import { classesHeaders } from '../helpers';

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
    to: {
      required: false,
      type: Object,
      default: null,
    },
  },
  computed: {
    classesCell() {
      return {
        'hidden-sm-and-up': !this.show,
        'hidden-xs-only': !this.show,
        'pointer-underline': this.to !== null,
        'px-0': true,
        ...classesHeaders.reduce((obj, value) => {
          obj[value] = true;
          return obj;
        }, {}),
      };
    },
    show() {
      return this.columnsSelected.hasOwnProperty(this.name);
    },
  },
  methods: {
    click() {
      if (this.to !== null) {
        this.$router.push(this.to);
      }
    },
  },
};
</script>

<style scoped>

</style>
