<template>
  <v-row no-gutters>
    <v-col>
      <v-container
        fluid
        class="pa-0"
      >
        <v-row dense>
          <v-col cols="6">
            <v-card class="fill-height">
              <v-card-title>Info</v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-item>
                    Version
                    <v-spacer />
                    {{ $store.state.module_app.version }}
                  </v-list-item>

                  <v-list-item>
                    Contact
                    <v-spacer />
                    <a href="mailto:mturk@kritten.org">
                      mturk@kritten.org
                    </a>
                  </v-list-item>

                  <v-list-item>
                    Created By
                    <v-spacer />
                    Kristof Komlossy,&nbsp;
                    <a href="https://webis.de/">
                      Webis
                    </a>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="6">
            <v-card class="fill-height">
              <v-card-title>Important Links</v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-item>
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
                  </v-list-item>

                  <v-list-item>
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
                  </v-list-item>

                  <v-list-item>
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
                  </v-list-item>

                  <v-list-item>
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
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row dense>
          <v-col>
            <v-card class="fill-height">
              <v-card-title>Changelog</v-card-title>
              <v-card-text>
                <changelog />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-col>
  </v-row>
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
