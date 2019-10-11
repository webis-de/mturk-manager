<template>
  <v-row
    no-gutters
    align="center"
    class="ml-n1"
  >
    <template v-for="(crumb, index) in arrayCrumbs">
      <v-col
        v-if="typeof crumb === 'string'"
        v-bind:key="index"
      >
        {{ crumb }}
      </v-col>
      <v-col
        v-else
        v-bind:key="index"
      >
        <v-btn
          class="px-1 text-none"
          text
          active-class=""
          style="font-size: inherit; letter-spacing: normal"
          v-bind:to="{ name: crumb.route }"
        >
          {{ crumb.name }}
        </v-btn>
      </v-col>
    </template>
  </v-row>
</template>

<script>
export default {
  name: 'TheBreadcrumb',
  data() {
    return {
      objectBlacklist: Object.freeze({
        tasks: true,
      }),
    };
  },
  computed: {
    arrayCrumbs() {
      const arrayCrumbs = [{
        route: 'project',
        name: this.$store.getters['moduleProjects/getProjectCurrent'].name,
      }];

      for (let i = 2; i < this.$route.matched.length; i += 1) {
        const route = this.$route.matched[i];
        if (Object.prototype.hasOwnProperty.call(this.objectBlacklist, route.name) === false) {
          arrayCrumbs.push('/');
          arrayCrumbs.push({
            route: route.name,
            name: route.meta.name !== null ? route.meta.name : this.$store.state.module_app.nameItem,
          });
        }
      }

      return arrayCrumbs;
    },
    namePage() {
      return `${this.project_current.name} / ${this.$route.meta.name}`;
    },
  },
};
</script>

<style scoped>
  .v-btn--active::before {
    opacity: 0;
  }
</style>
