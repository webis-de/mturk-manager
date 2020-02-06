<template>
  <v-row
    v-bind:id="identifier !== null ? identifier : false"
    dense
  >
    <v-col v-if="type === 'table'">
      <slot></slot>
    </v-col>
    <v-col v-else>
      <v-card>
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
      type: String,
      required: false,
      default: null,
    },
  },
};
</script>

<style scoped>

</style>
