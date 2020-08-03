<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <base-page>
        <base-page-section
          type="table"
          v-bind:identifier="{
            identifier: 'batches',
            label: 'Batches'
          }"
        >
          <list-batches>
            <template v-slot:actions>
              <component-download-batch />
            </template>
          </list-batches>
        </base-page-section>

        <base-page-section
          type="table"
          v-bind:identifier="{
            identifier: 'hits',
            label: 'HITs'
          }"
        >
          <list-hits />
        </base-page-section>

        <base-page-section
          type="table"
          v-bind:identifier="{
            identifier: 'assignments',
            label: 'Assignments'
          }"
        >
          <list-assignments>
            <template v-slot:actions>
              <component-annotate />
            </template>
          </list-assignments>
        </base-page-section>
      </base-page>
    </template>

<!--    <create-batch />-->
  </div>
</template>

<script>
import ComponentDownloadBatch from '../../../components/batches/component_download_batch';
import ListBatches from '../../../components/batches/list/list-batches';
import ListHits from '../../../components/hits/list/list-hits';
import ListAssignments from '../../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../../components/assignments/annotate/component_annotate';
import BasePage from '../../../components/base/base-page';
import BasePageSection from '../../../components/base/base-page-section';
import CreateBatch from '../../../components/batches/create/component_create_batch';

export default {
  name: 'Tasks',
  components: {
    CreateBatch,
    BasePageSection,
    BasePage,
    ComponentAnnotate,
    ListAssignments,
    ListHits,
    ListBatches,
    ComponentDownloadBatch,
  },
};
</script>
