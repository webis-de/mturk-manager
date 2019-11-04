<template>
  <div>
    <router-view />
    <template
      v-if="$route.params.id === undefined"
    >
      <v-card>
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
import ListAssignments from '../../../../components/assignments/list/list-assignments';
import ComponentAnnotate from '../../../../components/assignments/annotate/component_annotate';

export default {
  name: 'AppAssignments',
  components: { ComponentAnnotate, ListAssignments },
};
</script>
