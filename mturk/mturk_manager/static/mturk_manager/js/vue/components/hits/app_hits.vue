<template>
  <span>
    <template v-if="$route.name == 'hits'">
      <h1 class="headline">HITs</h1>
      <list-hits></list-hits>
    </template>
    <template v-else-if="$route.name == 'hit'">
      <component-hit-detail v-bind:id_hit="id_hit"></component-hit-detail>
    </template>
  </span>
</template>

<script>
import ComponentHitDetail from './detail/component_hit_detail.vue';
import slug_project from '../../mixins/slug_project';
import ComponentItemHit from './list/component_item_hit';
import ListHits from './list/list-hits';

export default {
  mixins: [slug_project],
  props: {
    id_hit: {},
  },
  name: 'app-hits',
  components: {
    ListHits,
    ComponentItemHit,
    ComponentHitDetail,
  },
};
</script>
