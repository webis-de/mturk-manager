import _ from 'lodash';
import localforage from 'localforage';
import { normalize_answer } from './helpers';

export default class Loader {
  constructor() {
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
      url_api_messages_reject: 'api/messages_reject',
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
    console.log(this.context);
  }

  async sync_data() {
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

    this.array_messages_reject = _.orderBy(result, 'usage_count', 'desc');
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
  }

  async load_assignments() {
    let url = this.context.url_api_assignments;
    url += `?list_ids=${new URL(location.href).searchParams.get('list_ids')}`;

    const result = await $.ajax({
      url,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });

    _.forEach(result, (assignment) => {
      this.object_workers[assignment.worker.id] = assignment.worker;
      // this.set_ids_worker.add(assignment.worker);
      assignment.answer = normalize_answer(assignment.answer);
      this.object_assignments[assignment.id] = assignment;
    });
  }

  async load_hits() {
    const set_ids_hit = new Set();
    _.forEach(this.object_assignments, (assignment) => {
      set_ids_hit.add(assignment.hit);
    });

    let url = this.context.url_api_hits;
    url += `?list_ids=[${_.toArray(set_ids_hit).join(',')}]`;

    const result = await $.ajax({
      url,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });

    _.forEach(result, (hit) => {
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
  }

  async load_batches() {
    const set_ids_batch = new Set();
    _.forEach(this.object_hits, (hit) => {
      set_ids_batch.add(hit.batch);
    });

    let url = this.context.url_api_batches;
    url += `?list_ids=[${_.toArray(set_ids_batch).join(',')}]`;

    const result = await $.ajax({
      url,
      method: 'GET',
      contentType: 'application/json',
      headers: {
        Authorization: `Token ${this.token_instance}`,
        'Content-Type': 'application/json',
      },
    });

    _.forEach(result, (batch) => {
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
    this.slug_project = location.pathname.substring(6);

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
