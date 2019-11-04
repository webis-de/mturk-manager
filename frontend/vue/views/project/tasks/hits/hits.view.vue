<template>
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <v-card>
        <list-hits />
      </v-card>
    </template>
  </div>
</template>

<script>
import ListHits from '../../../../components/hits/list/list-hits';

export default {
  name: 'AppHits',
  components: { ListHits },
};
</script>
