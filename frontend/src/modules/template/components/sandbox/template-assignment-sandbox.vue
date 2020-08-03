<template>
  <base-editor
    v-bind:value="value"
    v-bind:source-preview="valueProcessed"
    v-bind:label="label"
    v-on:input="$emit('input', $event)"
  >
    <v-col>
      <v-row no-gutters>
        <v-col class="px-1">
          <v-select
            v-model="templateHIT"
            label="HIT Template"
            dense
            hide-details
            class="mt-0"
            v-bind:items="templatesHIT"
            item-value="id"
            item-text="name"
            clearable
            return-object
          />
        </v-col>
        <v-col class="px-1">
          <v-select
            v-model="templateGlobal"
            label="Global Template"
            dense
            hide-details
            class="mt-0"
            v-bind:items="templatesGlobal"
            item-value="id"
            item-text="name"
            clearable
            return-object
          />
        </v-col>
      </v-row>
    </v-col>
  </base-editor>
</template>

<script lang="typescript">
import _ from 'lodash';
import BaseEditor from '../../../app/components/base-editor.vue';

export default {
  name: 'TemplateAssignmentSandbox',
  components: { BaseEditor },
  props: {
    value: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
      default: '',
    },
  },
  data() {
    return {
      valueDebounced: this.value,
      indexAnnotate: null,
      templateHIT: undefined,
      templateGlobal: undefined,
    };
  },
  computed: {
    valueProcessed() {
      return this.sourcePreview;
    },
    templateAssignmentEscaped() {
      return this.escapeHtml(this.valueDebounced);
    },
    templateHITEscaped() {
      if (this.templateHIT === undefined) return null;

      return `'${this.escapeHtml(this.templateHIT.template)}'`;
    },
    templateGlobalEscaped() {
      if (this.templateGlobal === undefined) return null;

      return `'${this.escapeHtml(this.templateGlobal.template)}'`;
    },
    sourcePreview() {
      return this.processTemplate(this.templateAssignmentEscaped, this.templateHITEscaped, this.templateGlobalEscaped);
    },
    templatesHIT() {
      return Object.values(this.$store.state.moduleTemplates.templatesHIT);
    },
    templatesGlobal() {
      return Object.values(this.$store.state.moduleTemplates.templatesGlobal);
    },
  },
  watch: {
    value: _.debounce(function () {
      this.valueDebounced = this.value;
    }, 500),
  },
  async created() {
    const data = await fetch(`${process.env.BASE_URL}index_annotate.js`);
    this.indexAnnotate = await data.text();
  },
  methods: {
    escapeHtml(string) {
      let result = string;
      result = result
        .replace(/<\/script>/g, '<\\/script>')
        .replace(/'/g, "\\'")
        .replace(/\n/g, '\\n');
      return result;
    },
    // escapeHtml(html) {
    //   // return '<div>test</div><script>console.warn("kritten")<\\/script>';
    //   const doc = new DOMParser().parseFromString(html, 'text/html');
    //   console.warn('doc.documentElement', doc.documentElement.textContent);
    //   console.warn('doc.documentElement.textContent', doc.documentElement.outerHTML);
    //   return doc.documentElement.textContent;
    // },
    processTemplate(templateAssignment, templateHIT, templateGlobal) {
      const text = this.indexAnnotate === null ? '' : this.indexAnnotate;
      // console.warn('data', text);
      console.warn('this.$store.state.moduleProjects.slug_project_current', this.$store.state.moduleProjects.slug_project_current);

      return `<!DOCTYPE html>
        <html>
        <head>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        </head>
          <body>
            <div id="wrapper_hits"></div>
            <script>
              const globalPassedData = {
                slugProject: '${this.$store.state.moduleProjects.slug_project_current}',
                templateAssignment: 'testassignment',
                assignments: [{
                  id: 0,
                  hit: 0,
                  id_assignment: 'ASSIGNMENT0',
                  status_external: null,
                  status_internal: null,
                  datetime_accept: '2019-04-15T16:10:37Z',
                  datetime_creation: '2019-04-15T16:10:37Z',
                  datetime_submit: '2019-04-15T16:10:37Z',
                  duration: '00:00:21',
                  answer: {
                    QuestionFormAnswers: {
                      Answer: [
                        {
                          FreeText: 'Answer 0',
                          QuestionIdentifier: 'variable1',
                        }
                      ]
                    }
                  },
                  worker: {
                    id: 0,
                    id_worker: 'WORKER0',
                    is_blocked_global: false,
                  }
                },{
                  id: 1,
                  hit: 1,
                  id_assignment: 'ASSIGNMENT1',
                  status_external: null,
                  status_internal: null,
                  datetime_accept: '2019-04-15T16:10:37Z',
                  datetime_creation: '2019-04-15T16:10:37Z',
                  datetime_submit: '2019-04-15T16:10:37Z',
                  duration: '00:00:21',
                  answer: {
                    QuestionFormAnswers: {
                      Answer: [
                        {
                          FreeText: 'Answer 0',
                          QuestionIdentifier: 'variable1',
                        }
                      ]
                    }
                  },
                  worker: {
                    id: 0,
                    id_worker: 'WORKER0',
                    is_blocked_global: false,
                  }
                },],
                hits: [{
                  id: 0,
                  batch: 0,
                  id_hit: 'HIT0',
                  datetime_creation: '2019-04-15T16:10:37Z',
                  datetime_expiration: '2019-04-15T16:10:37Z',
                  count_assignments_approved: 0,
                  count_assignments_dead: 0,
                  count_assignments_pending: 0,
                  count_assignments_rejected: 0,
                  count_assignments_submitted: 1,
                  count_assignments_total: 1,
                  parameters: '{}',
                },{
                  id: 1,
                  batch: 0,
                  id_hit: 'HIT1',
                  datetime_creation: '2019-04-15T16:10:37Z',
                  datetime_expiration: '2019-04-15T16:10:37Z',
                  count_assignments_approved: 0,
                  count_assignments_dead: 0,
                  count_assignments_pending: 0,
                  count_assignments_rejected: 0,
                  count_assignments_submitted: 1,
                  count_assignments_total: 1,
                  parameters: '{}',
                },],
                batches: [{
                  id: 0,
                  name: "EXP TOPIC 18 DIALECTICAL",
                  count_hits: 175,
                  datetime_creation: "2019-04-15T08:22:53.430818Z",
                  project: 62,
                  use_sandbox: false,
                  settings_batch: {
                     id: 453,
                     name: "62__EXP TOPIC 18 DIALECTICAL__cf45af33eabc495cb48036f7f55f681c",
                     title: "Pairwise Text Quality Comparison",
                     description: "Compare two texts and decide which one fits a given quality criterium better.",
                     keywords: [
                        {
                           id: 0,
                           text: "Keyword 0"
                        },
                        {
                           id: 1,
                           text: "Keyword 1"
                        },
                     ],
                     count_assignments: 1,
                     reward: 8,
                     lifetime: 86400,
                     duration: 300,
                     has_content_adult: false,
                     qualification_assignments_approved: 95,
                     qualification_hits_approved: 20,
                     qualification_locale: [],
                     blockWorkers: true,
                     template: {
                        id: 45,
                        name: "Argument Quality Worker Template Dialectical",
                        height_frame: 1300,
                        template: "<!DOCTYPE html><html><body>assignments: <div id=\\"wrapper_hits\\"></div></body></html>",
                        json_dict_parameters: "{\\"argumentId4a\\": 1, \\"argumentId3b\\": 1, \\"discussionId2a\\": 1, \\"discussionId4b\\": 1, \\"argument4a\\": 1, \\"discussionId5b\\": 1, \\"argument2b\\": 1, \\"discussionId2b\\": 1, \\"argument5b\\": 1, \\"discussionId3a\\": 1, \\"argumentId5a\\": 1, \\"argumentId1b\\": 1, \\"discussionId4a\\": 1, \\"argumentId2a\\": 1, \\"argument1b\\": 1, \\"argument2a\\": 1, \\"argument5a\\": 1, \\"argumentId5b\\": 1, \\"argument3b\\": 1, \\"argument1a\\": 1, \\"argumentId4b\\": 1, \\"discussionId1b\\": 1, \\"argumentId3a\\": 1, \\"discussionId5a\\": 1, \\"discussionId1a\\": 1, \\"argumentId1a\\": 1, \\"argument3a\\": 1, \\"argumentId2b\\": 1, \\"discussionId3b\\": 1, \\"argument4b\\": 1}",
                        template_assignment: {
                          id: 11,
                          name: "Argument Quality Assignment Template",
                          template: '${templateAssignment}',
                        },
                        template_hit: {
                          id: 6,
                          name: "Argument Quality HIT Template",
                          template: ${templateHIT}
                        },
                        template_global: {
                          id: 7,
                          name: "Argument Quality Global Template",
                          template: ${templateGlobal}
                        },
                      },
                      count_assignments_max_per_worker: null
                    },
                    count_assignments_total: 175,
                    count_assignments_approved: 0,
                    count_assignments_rejected: 0,
                    count_assignments_submitted: 175,
                    count_assignments_dead: 0,
                    count_assignments_pending: 0,
                    count_assignments_available: 175,
                    costs_max: 1400,
                    costs_so_far: 0
                  }
                ],
              }
            <\/script>
            <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"><\/script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"><\/script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"><\/script>
            <script>${text}<\/script>
          </body>
        </html>`;
      // const templatePrefix = `
      //   <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"><\/script>
      //
      //   <script>
      //     const assignment_wrapper = $('span[data-id_assignment="${assignment.id}"]');
      //     const assignment = ${JSON.stringify(assignment)};
      //   <\/script>
      //   <span data-id_assignment="${assignment.id}">${this.value}</span>
      // `;
      // console.warn('templatePrefix', templatePrefix);
      // return templatePrefix;
    },
  },
};
</script>

<style scoped>

</style>
