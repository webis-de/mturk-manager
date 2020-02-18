<template>
  <div>
    <div
      v-ripple
      style="position:absolute; z-index:999; width: 26px; height: 24px; cursor: pointer"
      v-on:click="click"
    >
    </div>
    <v-simple-checkbox
      v-bind:value="value"
      class="pa-0 ma-0"
      primary
      hide-details
    />
  </div>
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
