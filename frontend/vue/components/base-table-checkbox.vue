<template>
  <v-checkbox
    v-bind:input-value="value"
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
  },
  methods: {
    click() {
      this.$emit('input', !this.value);
    },
  },
};
</script>
