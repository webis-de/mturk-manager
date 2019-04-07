import _ from 'lodash';
import { parse } from 'date-fns';

export default class HIT {
  constructor(data = {}) {
    this.id = data.id;
    this.id_hit = data.id_hit;
    this.batch = data.batch;
    this.count_assignments_additional = data.count_assignments_additional;
    this.datetime_creation = parse(data.datetime_creation);
    this.datetime_expiration = parse(data.datetime_expiration);
    this.parameters = data.parameters;

    this.countAssignmentsTotal = data.count_assignments_total;
    this.countAssignmentsApproved = data.count_assignments_approved;
    this.countAssignmentsRejected = data.count_assignments_rejected;
    this.countAssignmentsSubmitted = data.count_assignments_submitted;
    this.countAssignmentsDead = data.count_assignments_dead;
    this.countAssignmentsPending = data.count_assignments_pending;
  }
}
