<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <base-page v-bind:sections="sections">
        <base-page-section
          type="table"
          identifier="batches"
        >
          <list-batches>
            <template v-slot:actions>
              <component-download-batch />
            </template>
          </list-batches>
        </base-page-section>

        <base-page-section
          type="table"
          identifier="hits"
        >
          <list-hits />
        </base-page-section>

        <base-page-section
          type="table"
          identifier="assignments"
        >
          <list-assignments>
            <template v-slot:actions>
              <component-annotate />
            </template>
          </list-assignments>
        </base-page-section>
      </base-page>
    </template>
  </div>
</template>

<script>
import ComponentDownloadBatch from '../../../components/batches/component_download_batch';
import ListBatches from '../../../components/batches/list/list-batches';
import ListHits from '../../../components/hits/list/list-hits';
import ListAssignments from '../../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../../components/assignments/annotate/component_annotate';
// import CreateBatch from '../../../components/batches/create/component_create_batch';
import BasePage from '../../../components/base/base-page';
import BasePageSection from '../../../components/base/base-page-section';

export default {
  name: 'Tasks',
  components: {
    BasePageSection,
    BasePage,
    // CreateBatch,
    ComponentAnnotate,
    ListAssignments,
    ListHits,
    ListBatches,
    ComponentDownloadBatch,
  },
  data() {
    return {
      sections: {
        batches: 'Batches',
        hits: 'HITs',
        assignments: 'Assignments',
      },
    };
  },
};
</script>
