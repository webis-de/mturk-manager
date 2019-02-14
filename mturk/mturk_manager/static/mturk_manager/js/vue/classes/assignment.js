import moment from "moment";

export default class Assignment {
  constructor(data = {}) {
    this.id = data.id;
    this.id_assignment = data.id_assignment;
    this.answer = data.answer;
    this.worker = data.worker;
    this.hit = data.hit;
    this.status_external = data.status_external;
    this.status_internal = data.status_internal;
    this.datetime_creation = moment(data.datetime_creation);
    this.datetime_accept = moment(data.datetime_accept);
    this.datetime_submit = moment(data.datetime_submit);
    // this.duration = new Date(data.duration);
    this.duration = moment.duration(data.duration);
    // this.duration = Date.parse(data.duration);
  }
}
