<template>
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <v-card>
        <list-batches>
          <template v-slot:actions>
            <component-download-batch />
          </template>
        </list-batches>
      </v-card>
    </template>
  </div>
</template>

<script>
import ListBatches from '../../../../components/batches/list/list-batches';
import ComponentDownloadBatch from '../../../../components/batches/component_download_batch';

export default {
  name: 'AppBatches',
  components: { ComponentDownloadBatch, ListBatches },
};
</script>
