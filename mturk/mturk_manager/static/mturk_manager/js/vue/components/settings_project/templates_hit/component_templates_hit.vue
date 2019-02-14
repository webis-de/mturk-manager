<template>
  <div>
    <h2 class="headline">HIT Templates</h2>
    <component-list-templates-hit></component-list-templates-hit>
  </div>
</template>

<script>
// import settings_batch from '../../../mixins/settings_batch';
import { mapState, mapMutations, mapActions, mapGetters } from "vuex";
import _ from "lodash";
import ComponentListTemplatesHit from "./component_list_templates_hit.vue";

export default {
  // mixins: [
  //     settings_batch,
  // ],
  name: "component-templates-hit",
  data() {
    return {
      // search: undefined,
    };
  },
  methods: {},
  computed: {},
  components: {
    ComponentListTemplatesHit
  }
};
</script>

<style scoped></style>
