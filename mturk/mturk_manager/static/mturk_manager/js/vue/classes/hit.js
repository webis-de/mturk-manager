import _ from 'lodash';
import moment from 'moment';

export default class HIT {
  constructor(data = {}) {
    this.id = data.id;
    this.id_hit = data.id_hit;
    this.batch = data.batch;
    this.count_assignments_additional = data.count_assignments_additional;
    this.datetime_creation = moment(data.datetime_creation);
    this.datetime_expiration = moment(data.datetime_expiration);
    this.parameters = data.parameters;
    this.count_assignments_available = data.count_assignments_available;
    this.count_assignments_total = data.count_assignments_total;
    // this.object_assignments = {};

    // this._count_assignments_total = null;
    // this._count_assignments_available = null;
    // this._progress = null;
  }

  get progress() {
    // if(this._progress != null) return this._progress;

    const progress = (this.count_assignments_available / this.count_assignments_total) * 100.0;
    // this._progress = progress;
    return progress;
  }
}
