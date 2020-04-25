<template>
  <v-row
    no-gutters
  >
    <v-col
      cols="12"
      class="mb-2"
    >
      <v-card>
        <v-breadcrumbs
          class="breadcrumbs"
          v-bind:items="breadcrumbs"
        />
      </v-card>
    </v-col>

    <v-col cols="12">
      <component-hit-detail
        v-bind:id-hit="id"
        v-on:loaded-hit="hit = $event"
      />
    </v-col>
  </v-row>
</template>

<script>
import { mapMutations, mapState } from 'vuex';
import ComponentHitDetail from '../../../../components/hits/detail/component_hit_detail';

export default {
  name: 'AppHit',
  components: {
    ComponentHitDetail,
  },
  props: {
    id: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      hit: null,
    };
  },
  computed: {
    breadcrumbs() {
      const breadcrumbs = [
        {
          text: 'Tasks',
          disabled: false,
          to: { name: 'tasks', hash: '#batches' },
          exact: true,
        },
      ];

      if (this.hit !== null) {
        breadcrumbs.push({
          text: this.hit.batch.name,
          to: { name: 'batch', params: { id: this.hit.batch.id } },
          exact: true,
        });
        breadcrumbs.push({
          text: this.hit.id_hit,
          disabled: true,
        });
      }


      return breadcrumbs;
    },
    ...mapState('moduleHITs', {
      paginationComputed: 'paginationGeneral',
    }),
  },
  methods: {
    ...mapMutations('moduleHITs', {
      functionSetPagination: 'setPaginationGeneral',
    }),
  },
};
</script>
