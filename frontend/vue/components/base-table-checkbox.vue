<template>
  <v-checkbox
    v-bind:input-value="value"
    v-bind:indeterminate="indeterminate"
    class="pa-0 ma-0"
    primary
    hide-details
    v-on:change="click"
  />
</template>

<script>
export default {
  name: 'BaseTableCheckbox',
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    indeterminate: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    click() {
      this.$emit('input', !this.value);
    },
  },
};
</script>
