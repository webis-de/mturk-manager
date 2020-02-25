<template>
  <v-row
    v-bind:id="identifier.identifier !== undefined ? identifier.identifier : false"
    dense
    v-bind:class="classes"
  >
    <v-col v-if="type === 'table'">
      <slot></slot>
    </v-col>
    <v-col v-else>
      <v-card class="fill-height">
        <v-card-title class="py-0">
          {{ title }}
        </v-card-title>
        <v-container
          fluid
          class="py-0 px-2"
        >
          <slot></slot>
        </v-container>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'BasePageSection',

  props: {
    type: {
      type: String,
      required: false,
      default: 'default',
    },
    identifier: {
      type: Object,
      required: false,
      default() {
        return {};
      },
    },
    title: {
      type: String,
      required: false,
      default: '',
    },
    shrink: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    classes() {
      return {
        'fill-height': this.$parent._name === '<BaseWrapNode>',
      };
    },
  },
};
</script>

<style scoped>

</style>
