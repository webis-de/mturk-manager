import _ from 'lodash';
import localforage from 'localforage';
import { normalize_answer } from './helpers';

export default class Loader {
  constructor(controller) {
    this.controller = controller;
    this.url_api = null;
    this.token_instance = null;
    this.PLACEHOLDER_SLUG_PROJECT = 'PLACEHOLDER_SLUG_PROJECT';
    this.context = {
      url_api_project: `projects/${this.PLACEHOLDER_SLUG_PROJECT}`,
      url_api_assignments: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/assignments_for_annotation`,
      url_api_assignments_update_stati: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/assignments`,
      url_api_hits: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/hits_for_annotation`,
      url_api_batches: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/batches_for_annotation`,
      url_api_workers: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/workers`,
      url_api_messages_reject: `projects/${this.PLACEHOLDER_SLUG_PROJECT}/messagesReject`,
    };
    this.project = {};
    this.message_reject_default = '';
    this.object_assignments = {};
    this.object_hits = {};
    this.object_batches = {};
    this.object_workers = {};
    this.set_ids_worker = new Set();
    this.array_messages_reject = [];

    this.object_assignments_selected = {};

    this.globalPassedData = null;
    try {
      this.globalPassedData = globalPassedData;
    } catch(e) {}

    console.log(this.context);
  }

  async sync_data() {
    this.controller.stepActive = null;

    await this.load_project();
    await this.load_assignments();
    await this.load_hits();
    await this.load_batches();
    // await this.load_workers();
    await this.load_messages_reject();
  }

  async load_messages_reject() {
    const url = this.context.url_api_messages_reject;

    const result = await $.ajax({
      url,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });

    this.array_messages_reject = _.orderBy(result.data, 'usage_count', 'desc');

    this.controller.stepActive = 4;
  }

  async load_project() {
    const url = this.context.url_api_project;

    const result = await $.ajax({
      url,
      method: 'GET',
      data: JSON.stringify(_.toArray(this.set_ids_worker)),
      contentType: 'application/json',
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });

    this.project = result;

    if (this.project.message_reject_default !== undefined && this.project.message_reject_default !== null) {
      this.message_reject_default = this.project.message_reject_default.message;
    }

    this.controller.stepActive = 0;
  }

  async load_assignments() {
    let assignments: [];
    if (this.globalPassedData === null) {
      let url = this.context.url_api_assignments;

      url += `?list_ids=${new URL(location.href).searchParams.get('list_ids')}`;

      assignments = await $.ajax({
        url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
          Authorization: `Token ${this.token_instance}`,
          'Content-Type': 'application/json',
        },
      });
    } else {
      assignments = this.globalPassedData.assignments;
    }

    _.forEach(assignments, (assignment) => {
      this.object_workers[assignment.worker.id] = assignment.worker;
      // this.set_ids_worker.add(assignment.worker);
      assignment.answer = normalize_answer(assignment.answer);
      this.object_assignments[assignment.id] = assignment;
    });

    this.controller.stepActive = 1;
  }

  async load_hits() {
    let hits: [];
    if (this.globalPassedData === null) {
      const set_ids_hit = new Set();
      _.forEach(this.object_assignments, (assignment) => {
        set_ids_hit.add(assignment.hit);
      });

      let url = this.context.url_api_hits;
      url += `?list_ids=[${_.toArray(set_ids_hit).join(',')}]`;

      hits = await $.ajax({
        url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
          Authorization: `Token ${this.token_instance}`,
          'Content-Type': 'application/json',
        },
      });
    } else {
      hits = this.globalPassedData.hits;
    }

    _.forEach(hits, (hit) => {
      hit.parameters = JSON.parse(hit.parameters);
      this.object_hits[hit.id] = hit;
    });

    _.forEach(this.object_assignments, (assignment) => {
      const hit = this.object_hits[assignment.hit];
      assignment.hit = hit;

      if (hit.assignments == undefined) {
        hit.assignments = [assignment];
      } else {
        hit.assignments.push(assignment);
      }
    });

    this.controller.stepActive = 2;
  }

  async load_batches() {
    let batches: [];
    if (this.globalPassedData === null) {
      const set_ids_batch = new Set();
      _.forEach(this.object_hits, (hit) => {
        set_ids_batch.add(hit.batch);
      });

      let url = this.context.url_api_batches;
      url += `?list_ids=[${_.toArray(set_ids_batch).join(',')}]`;

      batches = await $.ajax({
        url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
          Authorization: `Token ${this.token_instance}`,
          'Content-Type': 'application/json',
        },
      });
    } else {
      batches = this.globalPassedData.batches;
    }

    _.forEach(batches, (batch) => {
      this.object_batches[batch.id] = batch;
    });

    _.forEach(this.object_hits, (hit) => {
      const batch = this.object_batches[hit.batch];
      hit.batch = batch;

      if (batch.hits == undefined) {
        batch.hits = [hit];
      } else {
        batch.hits.push(hit);
      }
    });

    this.controller.stepActive = 3;
  }

  // async load_workers() {
  // 	const url = this.context.url_api_workers;
  //
  // 	const result = await $.ajax({
  //         url: url,
  //         method: 'PATCH',
  //         data: JSON.stringify(_.toArray(this.set_ids_worker)),
  //         contentType: 'application/json',
  //         headers: {
  //             Authorization: 'Token ' + this.token_instance,
  //             "Content-Type": 'application/json',
  //         },
  //     });
  //
  // 	_.forEach(result, (worker) => {
  // 		this.object_workers[worker.id] = worker;
  // 	});
  //
  // 	_.forEach(this.object_assignments, (assignment) => {
  // 		assignment.worker = this.object_workers[assignment.worker];
  // 	});
  // }

  async init() {
    if (this.globalPassedData === null) {
      this.slug_project = location.pathname.substring(6);
    } else {
      this.slug_project = this.globalPassedData.slugProject;
    }

    this.url_api = await localforage.getItem('url_api');
    this.token_instance = await localforage.getItem('token_instance');

    _.forEach(this.context, (value, key) => {
      if (key.startsWith('url_')) {
        this.context[key] = `${this.url_api
        }/${
          value.replace('PLACEHOLDER_SLUG_PROJECT', this.slug_project)}`;
      }
    });
  }
}
