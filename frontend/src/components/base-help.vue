<template>
  <v-menu
    offset-y
    offset-x
    v-bind:close-on-content-click="false"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        icon
        small
        v-on="on"
        class="text--secondary"
      >
        <v-icon>mdi-information-outline</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-text>
        <slot></slot>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: 'BaseHelp',
};
</script>
