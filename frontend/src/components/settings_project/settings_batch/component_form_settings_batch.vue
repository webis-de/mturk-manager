<template>
  <div>
    <h2>General Settings</h2>
    <v-container
      fluid
      class="pa-0 pt-3"
      grid-list-md
    >
      <v-layout wrap>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            v-bind:value="title"
            label="Title"
            v-bind:error-messages="validation_errors.settings_batch.title"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:title', $event);
              v.settings_batch.title.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            v-bind:value="description"
            label="Description"
            v-bind:error-messages="validation_errors.settings_batch.description"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:description', $event);
              v.settings_batch.description.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-layout
            row
            align-center
          >
            <v-flex>
              <v-text-field
                dense
                required
                type="number"
                v-bind:value="reward"
                step="1"
                v-bind:label="`Reward (${amount_formatted(reward)})`"
                v-bind:error-messages="validation_errors.settings_batch.reward"
                v-bind:readonly="readonly"
                v-bind:disabled="disabled"
                v-on:input="
                  $emit('update:reward', try_number($event));
                  v.settings_batch.reward.$touch();
                "
              />
            </v-flex>
            <v-flex shrink>
              <div
                slot="append"
                class="text-no-wrap"
              >
                ct, in Dollar: {{ amount_formatted(reward) }}
              </div>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            type="number"
            v-bind:value="countAssignments"
            label="Number of Assignments"
            min="1"
            v-bind:error-messages="validation_errors.settings_batch.countAssignments"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:countAssignments', try_number($event));
              v.settings_batch.countAssignments.$touch();
            "
          />

          <!-- <v-text-field
                  required
                  type="number"
                  v-bind:value="countAssignmentsMaxPerWorker"
                  v-on:input="$emit('update:countAssignmentsMaxPerWorker', try_number($event)); v.settings_batch.countAssignmentsMaxPerWorker.$touch()"
                  label="Number of Maximal Assignments Per Worker"
                  min="-1"
                  append-icon="clear"
                  v-on:click:append="$emit('update:countAssignmentsMaxPerWorker', undefined); v.settings_batch.countAssignmentsMaxPerWorker.$touch()"
                  v-bind:error-messages="validation_errors.settings_batch.countAssignmentsMaxPerWorker"
              ></v-text-field> -->
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            type="number"
            v-bind:value="lifetime"
            v-bind:label="format_duration('Lifetime', lifetime)"
            min="1"
            suffix="s"
            v-bind:error-messages="validation_errors.settings_batch.lifetime"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:lifetime', try_number($event));
              v.settings_batch.lifetime.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            type="number"
            v-bind:value="duration"
            v-bind:label="format_duration('Duration', duration)"
            min="1"
            suffix="s"
            v-bind:error-messages="validation_errors.settings_batch.duration"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:duration', try_number($event));
              v.settings_batch.duration.$touch();
            "
          />
        </v-flex>
        <v-flex
          v-if="disabled === false"
          v-bind="flexSize"
        >
          <v-select
            dense
            v-bind:value="templateWorkerExpanded"
            v-bind:items="arrayTemplatesWorker"
            label="Worker Template"
            item-text="name"
            item-value="id"
            v-bind:error-messages="validation_errors.settings_batch.templateWorker"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:templateWorker', $event);
              v.settings_batch.templateWorker.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-switch
            v-bind:label="
              `Limit Block and Project Block for Workers (${
                blockWorkers ? 'enabled' : 'disabled'
              })`
            "
            v-bind:input-value="blockWorkers"
            v-bind:error-messages="validation_errors.settings_batch.blockWorkers"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:change="
              $emit('update:blockWorkers', $event);
              v.settings_batch.blockWorkers.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-combobox
            dense
            v-bind:value="keywords"
            label="Keywords (Separated with TAB)"
            v-bind:items="list_keywords"
            hide-selected
            clearable
            multiple
            small-chips
            counter
            append-icon
            v-bind:error-messages="validation_errors.settings_batch.keywords"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:keywords', $event);
              v.settings_batch.keywords.$touch();
            "
            v-on:change="handle_change_combobox($event)"
          >
            <template
              slot="selection"
              slot-scope="data"
            >
              <v-chip
                v-bind:input-value="data.selected"
                close
                small
                v-on:input="remove(data.item)"
              >
                <strong>{{
                  data.item.text != undefined ? data.item.text : data.item
                }}</strong>&nbsp;
              </v-chip>
            </template>
          </v-combobox>
        </v-flex>
      </v-layout>
    </v-container>
    <v-divider class="my-3" />
    <h2>Qualifications</h2>
    <v-container
      fluid
      class="pa-0"
      grid-list-md
    >
      <v-layout wrap>
        <v-flex v-bind="flexSize">
          <v-switch
            v-bind:label="`Contains Adult Content`"
            v-bind:input-value="hasContentAdult"
            v-bind:error-messages="validation_errors.settings_batch.hasContentAdult"
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:change="
              $emit('update:hasContentAdult', $event);
              v.settings_batch.hasContentAdult.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            type="number"
            v-bind:value="qualificationAssignmentsApproved"
            step="1"
            max="100"
            min="0"
            label="Approved Assignments"
            append-icon="%"
            v-bind:error-messages="
              validation_errors.settings_batch.qualificationAssignmentsApproved
            "
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:qualificationAssignmentsApproved', try_number($event));
              v.settings_batch.qualificationAssignmentsApproved.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-text-field
            dense
            required
            type="number"
            v-bind:value="qualificationHitsApproved"
            step="1"
            min="0"
            label="Approved HITs"
            v-bind:error-messages="
              validation_errors.settings_batch.qualificationHitsApproved
            "
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:qualificationHitsApproved', try_number($event));
              v.settings_batch.qualificationHitsApproved.$touch();
            "
          />
        </v-flex>
        <v-flex v-bind="flexSize">
          <v-combobox
            dense
            v-bind:value="qualificationLocale"
            label="Locale (Separated with TAB)"
            hide-selected
            small-chips
            clearable
            multiple
            counter
            append-icon
            v-bind:error-messages="
              validation_errors.settings_batch.qualificationLocale
            "
            v-bind:readonly="readonly"
            v-bind:disabled="disabled"
            v-on:input="
              $emit('update:qualificationLocale', $event);
              v.settings_batch.qualificationLocale.$touch();
            "
            v-on:change="handle_change_combobox($event)"
          >
            <template
              slot="selection"
              slot-scope="data"
            >
              <v-chip
                v-bind:input-value="data.selected"
                close
                small
                v-on:input="remove_qualificationLocale(data.item)"
              >
                <strong>{{
                  data.item.text != undefined ? data.item.text : data.item
                }}</strong>&nbsp;
              </v-chip>
            </template>
          </v-combobox>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import {
  mapState, mapGetters,
} from 'vuex';
import humanizeDuration from 'humanize-duration';
import _ from 'lodash';
import helpers from '../../../mixins/helpers.mixin';

export default {
  name: 'ComponentFormSettingsBatch',
  mixins: [helpers],
  props: {
    flexSize: {
      required: false,
      default() {
        return { xs12: true };
      },
    },
    readonly: {
      required: false,
      default: false,
    },
    disabled: {
      required: false,
      default: false,
    },
    v: {
      required: false,
      default() {
        return {
          settings_batch: {},
        };
      },
    },
    validation_errors: {
      required: false,
      default() {
        return {
          settings_batch: {},
        };
      },
    },
    title: {},
    description: {},
    reward: {},
    countAssignments: {},
    countAssignmentsMaxPerWorker: {},
    lifetime: {},
    duration: {},
    templateWorker: {},
    blockWorkers: {},
    keywords: {},
    hasContentAdult: {},
    qualificationAssignmentsApproved: {},
    qualificationHitsApproved: {},
    qualificationLocale: {},
  },
  data() {
    return {
    };
  },
  methods: {
    handle_change_combobox(f) {
      f.forEach((element, index) => {
        if (typeof element === 'string') {
          this.$set(f, index, { text: element });
        }
      });
    },
    format_duration(label, duration) {
      return `${label} (${humanizeDuration(duration * 1000)})`;
    },
    remove_qualificationLocale(item) {
      this.qualificationLocale.splice(
        this.qualificationLocale.indexOf(item),
        1,
      );
      // this.qualificationLocale = [...this.qualificationLocale]
    },
    remove(item) {
      this.keywords.splice(this.keywords.indexOf(item), 1);
      // this.keywords = [...this.keywords]
    },
  },
  computed: {
    templateWorkerExpanded() {
      if (this.templateWorker === null) return null;
      return this.$store.state.moduleTemplates.templatesWorker[this.templateWorker];
    },
    arrayTemplatesWorker() {
      const templatesWorker = this.$store.getters['moduleTemplates/templatesWorker'];
      if (templatesWorker === null) {
        return [];
      }

      return templatesWorker.slice().sort((a, b) => a.name.localeCompare(b.name));
    },
    list_keywords() {
      if (this.object_keywords == null) {
        return [];
      }
      return Object.values(this.object_keywords);
    },
    ...mapGetters('moduleKeywords', {
      object_keywords: 'get_object_keywords',
    }),
  },
  created() {
    // ServiceTemplates.getAll({
    //   typeTemplate: 'workerAll',
    // });
  },
};
</script>

<style lang="css" scoped></style>
