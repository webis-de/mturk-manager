<template>
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <router-link to="#batches">
              batches
            </router-link>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <router-link to="#hits">
              hits
            </router-link>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <router-link to="#assignments">
              assignments
            </router-link>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-card id="batches">
        <list-batches>
          <template v-slot:actions>
            <component-download-batch />
          </template>
        </list-batches>
      </v-card>

      <v-card id="hits">
        <list-hits />
      </v-card>

      <v-card id="assignments">
        <list-assignments>
          <template v-slot:actions>
            <component-annotate />
          </template>
        </list-assignments>
      </v-card>
    </template>
  </div>
</template>

<script>
import ListBatches from '../../../../components/batches/list/list-batches';
import ComponentDownloadBatch from '../../../../components/batches/component_download_batch';
import ListHits from '../../../../components/hits/list/list-hits';
import ListAssignments from '../../../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../../../components/assignments/annotate/component_annotate';

export default {
  name: 'AppBatches',
  components: {
    ComponentAnnotate, ListAssignments, ListHits, ComponentDownloadBatch, ListBatches,
  },
};
</script>
