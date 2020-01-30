<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col>
          <v-list
            dense
            flat
          >
            <v-card>
              <v-breadcrumbs
                class="breadcrumbs"
                v-bind:items="breadcrumbs"
              />
            </v-card>
          </v-list>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-list
            dense
            flat
          >
            <v-list-item-group>
              <v-list-item
                v-for="anchor of anchors"
                v-bind:key="anchor.anchor"
                style="min-height: 24px"
                v-on:click.native="scrollTo(anchor.anchor)"
              >
                <v-list-item-icon class="ma-0">
                  <v-icon>mdi-chevron-down</v-icon>
                </v-list-item-icon>
                <v-list-item-content class="py-0">
                  {{ anchor.label }}
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <slot></slot>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'BasePage',
  computed: {
    anchors() {
      return [];
    },
    breadcrumbs() {
      return [];
    },
  },
  created() {
    console.warn('this.$slots.default', this.$slots.default);
  },
  methods: {
    scrollTo(hash) {
      this.$vuetify.goTo(hash, { offset: 8, duration: 0 });
    },
  },
};
</script>

<style scoped>

</style>
