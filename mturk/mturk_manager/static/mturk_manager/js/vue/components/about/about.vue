<template>
  <v-layout>
    <v-flex>
      <v-container
        fluid
        grid-list-md
      >
        <v-layout>
          <v-flex xs6>
            <v-card height="100%">
              <v-card-title>Info</v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-tile>
                    Version
                    <v-spacer />
                    {{ $store.state.module_app.version }}
                  </v-list-tile>

                  <v-list-tile>
                    Contact
                    <v-spacer />
                    <a href="mailto:mturk@kritten.org">
                      mturk@kritten.org
                    </a>
                  </v-list-tile>

                  <v-list-tile>
                    Created By
                    <v-spacer />
                    Kristof Komlossy
                  </v-list-tile>

                  <v-list-tile>
                    Credits
                    <v-spacer />
                    Martin Potthast,&nbsp;<a href="https://webis.de/">
                      Webis
                    </a>
                  </v-list-tile>
                </v-list>
              </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs6>
            <v-card>
              <v-card-title>Important Links</v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-tile>
                    Worker Sandbox
                    <v-spacer />
                    <v-btn
                      href="https://workersandbox.mturk.com"
                      target="_blank"
                      color="primary"
                      small
                    >
                      Open
                    </v-btn>
                  </v-list-tile>

                  <v-list-tile>
                    MTurk Documentation
                    <v-spacer />
                    <v-btn
                      href="https://docs.aws.amazon.com/mturk/index.html"
                      target="_blank"
                      color="primary"
                      small
                    >
                      Open
                    </v-btn>
                  </v-list-tile>

                  <v-list-tile>
                    MTurk Manager Wiki
                    <v-spacer />
                    <v-btn
                      href="https://github.com/webis-de/mturk-manager/wiki"
                      target="_blank"
                      color="primary"
                      small
                    >
                      Open
                    </v-btn>
                  </v-list-tile>

                  <v-list-tile>
                    MTurk Manager Code
                    <v-spacer />
                    <v-btn
                      href="https://github.com/webis-de/mturk-manager"
                      target="_blank"
                      color="primary"
                      small
                    >
                      Open
                    </v-btn>
                  </v-list-tile>
                </v-list>
              </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>

        <v-layout>
          <v-flex>
            <v-card>
              <v-card-title>Changelog</v-card-title>
              <v-card-text>
                <changelog />
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
import Changelog from './changelog';

export default {
  name: 'About',
  components: { Changelog },
  data() {
    return {};
  },
};
</script>
