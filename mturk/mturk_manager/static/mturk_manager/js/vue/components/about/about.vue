<template>
  <v-layout>
    <v-flex>
      <v-container
        fluid
        grid-list-md
      >
        <v-layout>
          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                Version: {{ $store.state.module_app.version }}
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                Contact: <a href="mailto:mturk@kritten.org">
                  mturk@kritten.org
                </a>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                Created By: Kristof Komlossy
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>

        <v-layout>
          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                <a href="https://workersandbox.mturk.com">
                  Worker Sandbox
                </a>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                <a href="https://docs.aws.amazon.com/mturk/index.html">
                  MTurk Documentation
                </a>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                <a href="https://github.com/webis-de/mturk-manager/wiki">
                  MTurk Manager Wiki
                </a>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>

        <v-layout>
          <v-flex xs4>
            <v-card>
              <v-card-text class="text-xs-center">
                <router-link
                  v-bind:to="{
                    name: 'add_credentials'
                  }"
                >
                  Update Credentials
                </router-link>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
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
