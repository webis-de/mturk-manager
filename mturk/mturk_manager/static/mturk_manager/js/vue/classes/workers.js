import { STATUS_BLOCK } from "./enums.js";

export default class Worker {
  constructor(data) {
    this.id = data.id;
    // this.m_created_at = new Date(data.CreationTime);
    // this.m_description = data.Description;
    // this.m_is_requestable = data.IsRequestable;
    this.id_worker = data.id_worker;
    this.count_assignments_limit =
      data.count_assignments_limit == null ? 0 : data.count_assignments_limit;
    this.is_blocked_soft = data.is_blocked_soft;
    this.is_blocked_global = data.is_blocked_global;
    this.is_blocked_hard = null;

    this.ratio_approved = null;
    // this.is_blocked = data.is_blocked;
    // this.m_status = data.QualificationTypeStatus;
  }

  // get_description() {
  // 	return this.m_description;
  // }
  // get_is_requestable() {
  // 	return this.m_is_requestable;
  // }
  // get_status() {
  // 	return this.m_status;
  // }
}
