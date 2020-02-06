<template>
  <v-row no-gutters>
    <v-col>
      <!--      <v-row no-gutters>-->
      <!--        <v-col>-->
      <!--          <v-list-->
      <!--            dense-->
      <!--            flat-->
      <!--          >-->
      <!--            <v-card>-->
      <!--              <v-breadcrumbs-->
      <!--                class="breadcrumbs"-->
      <!--                v-bind:items="breadcrumbs"-->
      <!--              />-->
      <!--            </v-card>-->
      <!--          </v-list>-->
      <!--        </v-col>-->
      <!--      </v-row>-->
      <v-row dense>
        <v-col class="pt-0">
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
      <v-row no-gutters>
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
  props: {
    sections: {
      type: Object,
      required: true,
    },
  },
  computed: {
    anchors() {
      const sectionsOrdered = this.$slots.default.map((node) => {
        if (node.componentOptions.propsData.identifier !== undefined) {
          return node.componentOptions.propsData.identifier;
        }
        return null;
      }).filter(section => section !== null);

      return sectionsOrdered.map(identifier => ({
        label: this.sections[identifier],
        anchor: identifier,
      }));
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
      this.$vuetify.goTo(`#${hash}`, { offset: 8, duration: 0 });
    },
  },
  // mounted() {
  //   console.warn('this.$route', this.$route.hash);
  //   if (this.$route.hash !== '') {
  //     // this.isWaitingForScrolling
  //     // setTimeout(() => {
  //     //   this.$vuetify.goTo(this.$route.hash);
  //     // }, 4000);
  //     // this.$nextTick(() => {
  //     //   this.$vuetify.goTo(this.$route.hash);
  //     // });
  //   }
  // },
};
</script>

<style scoped>

</style>
