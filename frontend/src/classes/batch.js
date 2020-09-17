import { parse } from 'date-fns';
import { SettingsBatch } from './settings_batch';

export default class Batch {
  constructor(data = { settings_batch: new SettingsBatch() }) {
    this.id = data.id;
    this.name = data.name;
    this.id_project = data.id_project;
    this.use_sandbox = data.use_sandbox;
    // this.object_hits = {};
    this.settings_batch = data.settings_batch;
    this.count_hits = data.count_hits;
    this.datetime_creation = parse(data.datetime_creation);

    this.countAssignmentsTotal = data.count_assignments_total;
    this.countAssignmentsApproved = data.count_assignments_approved;
    this.countAssignmentsRejected = data.count_assignments_rejected;
    this.countAssignmentsSubmitted = data.count_assignments_submitted;
    this.countAssignmentsDead = data.count_assignments_dead;
    this.countAssignmentsPending = data.count_assignments_pending;

    this.costs_max = data.costs_max;
    this.costs_so_far = data.costs_so_far;

    this.count_workers = data.count_workers;

    // TODO: find nicer approach
    this.countAssignmentsDead = this.countAssignmentsTotal
                              - this.countAssignmentsApproved
                              - this.countAssignmentsRejected
                              - this.countAssignmentsSubmitted
                              - this.countAssignmentsPending;
  }
}
