<template>
  <v-layout>
    <v-flex>
      <v-list>
        <v-list-tile>
          <v-list-tile-content>
            Version
          </v-list-tile-content>
          <v-list-tile-content>
            {{ $store.state.module_app.version }}
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile>
          <v-list-tile-content>
            Created By
          </v-list-tile-content>
          <v-list-tile-content class="text-xs-right">
            Kristof Komlossy
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile>
          <v-list-tile-content>
            Contact
          </v-list-tile-content>
          <v-list-tile-content>
            <a href="mailto:mturk@kritten.org">
              mturk@kritten.org
            </a>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'About',
  data() {
    return {};
  },
  mounted() {
    console.warn('test', this.$store.module_app);
  },
};
</script>
