export default class Worker {
  constructor(data) {
    this.id = data.id;
    // this.m_created_at = new Date(data.CreationTime);
    // this.m_description = data.Description;
    // this.m_is_requestable = data.IsRequestable;
    this.id_worker = data.id_worker;
    this.number_of_assignments = data.number_of_assignments;
    this.count_assignments_limit = data.count_assignments_limit == null ? 0 : data.count_assignments_limit;
    this.is_blocked_soft = data.is_blocked_soft;
    this.is_blocked_global = data.is_blocked_global;
    this.is_blocked_hard = null;

    this.number_of_approved_assignments_of_project = data.number_of_approved_assignments_of_project;
    this.number_of_rejected_assignments_of_project = data.number_of_rejected_assignments_of_project;
    this.ratio_approved_assignments_of_project = data.ratio_approved_assignments_of_project;
    this.number_of_approved_assignments = data.number_of_approved_assignments;
    this.number_of_rejected_assignments = data.number_of_rejected_assignments;
    this.ratio_approved_assignments = data.ratio_approved_assignments;
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
