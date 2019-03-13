import _ from 'lodash';
import { STATUS_EXTERNAL, STATUS_INTERNAL } from '../vue/classes/enums';

export default class View {
  constructor(loader) {
    this.loader = loader;
    this.wrapper_hits = $('#wrapper_hits');
    this.button_submit = $('[data-task="submit_annotations"]');
    this.dropdown_reject_assignment = $('.dropdown_reject_assignment');
    this.group_by = 'assignments';
  }

  update() {
    this.inject_templates();
    this.update_project_info();
  }

  check_submit_button() {
    if (
      this.loader.message_reject_default.trim() == ''
      && _.find(
        this.loader.object_assignments_selected,
        e => e.state == 'reject' || e.state == 'approve_internally',
      ) != undefined
    ) return this.button_submit.prop('disabled', true);

    if (_.size(this.loader.object_assignments_selected) == 0) return this.button_submit.prop('disabled', true);

    this.button_submit.prop('disabled', false);
  }

  update_project_info() {
    if (this.loader.project.message_reject_default != undefined) {
      $('#message_reject_default').val(
        this.loader.project.message_reject_default.message,
      );
    } else {
      $('#message_reject_default').val('');
    }
  }

  update_info() {
    let count_approved_assignments = 0;
    let count_rejected_assignments = 0;
    let count_rejected_internally_assignments = 0;
    let count_approved_internally_assignments = 0;

    _.forEach(this.loader.object_assignments_selected, (assignment) => {
      switch (assignment.state) {
        case 'approve':
          count_approved_assignments += 1;
          break;
        case 'reject':
          count_rejected_assignments += 1;
          break;
        case 'approve_internally':
          count_approved_internally_assignments += 1;
          break;
        case 'reject_internally':
          count_rejected_internally_assignments += 1;
          break;
      }
    });

    const sum = _.sum([
      count_approved_assignments,
      count_rejected_assignments,
      count_rejected_internally_assignments,
      count_approved_internally_assignments,
    ]);

    // $('pre').text(JSON.stringify(this.loader.object_assignments_selected));

    $('[data-inject_count_approved_assignments]').text(
      count_approved_assignments,
    );
    $('[data-inject_count_rejected_assignments]').text(
      count_rejected_assignments,
    );
    $('[data-inject_count_rejected_internally_assignments]').text(
      count_rejected_internally_assignments,
    );
    $('[data-inject_count_approved_internally_assignments]').text(
      count_approved_internally_assignments,
    );
    $('[data-inject_count_assignments]').text(sum);
  }

  inject_templates() {
    this.wrapper_hits.html('');
    // console.log('OBJECT_BATCHES', this.loader.object_batches);
    // console.log('OBJECT_HITS', this.loader.object_hits);
    // console.log('OBJECT_ASSIGNMENTS', this.loader.object_assignments);
    const object_assignments_grouped_by_batch = _.groupBy(
      this.loader.object_assignments,
      'hit.batch.id',
    );
    _.forEach(
      object_assignments_grouped_by_batch,
      (list_assignments, id_batch) => {
        const batch = this.loader.object_batches[id_batch];

        const template_global = _.get(
          batch,
          'settings_batch.template.template_global.template',
          undefined,
        );
        if (template_global !== undefined) {
          this.wrapper_hits.append(template_global);
        }

        const template_hit = _.get(
          batch,
          'settings_batch.template.template_hit.template',
          undefined,
        );

        const template_assignment = _.get(
          batch,
          'settings_batch.template.template_assignment.template',
          undefined,
        );

        const template_assignment_parsed = $.parseHTML(template_assignment);
        let is_table = false;
        _.forEach(template_assignment_parsed, (element) => {
          if ($(element).is('tr')) {
            is_table = true;
            return false;
          }
        });

        let object_groups;
        switch (this.group_by) {
          case 'hits':
            object_groups = _.groupBy(list_assignments, 'hit.id');
            break;
          case 'workers':
            object_groups = _.groupBy(list_assignments, 'worker.id');
            break;
          default:
            object_groups = _.groupBy(list_assignments, 'id');
        }

        _.forEach(object_groups, (group, id_group) => {
          const object_grouped_by_hits = _.groupBy(group, 'hit.id');
          _.forEach(object_grouped_by_hits, (grouped_by_hits, id_hit) => {
            const id = `${id_batch}_${id_group}_${id_hit}`;
            // save hit object
            const hit = this.loader.object_hits[id_hit];
            // create wrapper for template to be able to inject the hit
            const wrapper_hit = $(
              $.parseHTML(`<span data-id_hit="${id}"></span>`),
            );
            // add hit data to wrapper to be accessible to the users
            wrapper_hit.data('hit', hit);

            wrapper_hit.append(
              `<script>var hit_wrapper = $('span[data-id_hit="${
                id
              }"]'); var hit = hit_wrapper.data("hit")</script>`,
            );

            let wrapper_assignments;

            if (template_hit) {
              const template_hit_prepared = template_hit.replace(
                /data-inject_assignments/g,
                `data-inject_assignments data-id_hit="${id}"`,
              );
              wrapper_hit.append(template_hit_prepared);

              this.wrapper_hits.append(wrapper_hit);

              wrapper_assignments = $(
                `[data-inject_assignments][data-id_hit="${id}"]`,
              );

              if (wrapper_assignments.length == 0) {
                console.warn('No \'data-inject_assignments\' defined');
                return true;
              }
            } else {
              this.wrapper_hits.append(wrapper_hit);

              wrapper_assignments = wrapper_hit;
            }

            _.forEach(grouped_by_hits, (assignment) => {
              let wrapper_assignment;

              const script_define_variables = $(`
							<script>
								var assignment_wrapper = $(\'${is_table ? 'tr' : 'span'}[data-id_assignment="${
  assignment.id
}"]\'); 
								var assignment = assignment_wrapper.data("assignment")
							</script>
						`)[0];

              if (is_table === true) {
                wrapper_assignment = $(template_assignment);
                const index_row = _.findIndex(wrapper_assignment, e => e.tagName === 'TR');

                wrapper_assignment[index_row].dataset.id_assignment = assignment.id;
                $(wrapper_assignment[index_row]).data('assignment', assignment);

                const index_script = _.findIndex(wrapper_assignment, e => e.tagName === 'SCRIPT');
                if (index_script === -1) {
                  wrapper_assignment.push(script_define_variables);
                } else {
                  wrapper_assignment.splice(
                    index_script,
                    0,
                    script_define_variables,
                  );
                }
              } else {
                // create wrapper for template to be able to inject the assignment
                wrapper_assignment = $(
                  `<span data-id_assignment="${assignment.id}"></span>`,
                );
                // add assignment data to wrapper to be accessible to the users
                wrapper_assignment.data('assignment', assignment);
                // inject inputs
                // wrapper_assignment.append(this.create_inputs(assignment));
                wrapper_assignment.append(script_define_variables);
                wrapper_assignment.append(template_assignment);
              }
              // console.log(wrapper_assignment.find('data-inject_input_forms'))
              wrapper_assignment
                .find('[data-inject_input_forms]')
                .append(this.create_inputs(assignment));
              // console.log(wrapper_assignment.find('data-inject_input_forms'));
              wrapper_assignments.append(wrapper_assignment);
            });
          });
        });
      },
    );
  }

  create_inputs(assignment) {
    // console.log(assignment);
    // <div class="custom-control custom-checkbox d-inline">
    // 	<input type="checkbox" data-kritten_checkbox="checkbox" class="custom-control-input" id="checkbox_assignment_PLACEHOLDER_ID" data-id_assignment="PLACEHOLDER_ID" name="checkbox_assignment" value="PLACEHOLDER_ID" PLACEHOLDER_DISABLED>
    // 	<label class="custom-control-label" for="checkbox_assignment_PLACEHOLDER_ID"></label>
    // </div>
    let result = `

			<div class="btn-group btn-group-sm">
				<button type="button" data-id_assignment="PLACEHOLDER_ID" class="btn PLACEHOLDER_SUCCESS approve_assignment" PLACEHOLDER_DISABLED>Approve</button>
				<button type="button" data-id_assignment="PLACEHOLDER_ID" class="btn PLACEHOLDER_REJECT_INTERNALLY reject_internally_assignment" PLACEHOLDER_DISABLED>Reject internally</button>
			</div>
			
			<div class="btn-group btn-group-sm">
				<div class="btn-group btn-group-sm">
	            	<button type="button" name="task" value="button_mturk_reject__PLACEHOLDER_ID" data-id_assignment="PLACEHOLDER_ID" class="btn PLACEHOLDER_DANGER reject_assignment" PLACEHOLDER_DISABLED>Reject</button>
	            	<button type="button" class="btn PLACEHOLDER_DANGER dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" PLACEHOLDER_DISABLED></button>
					<div class="dropdown-menu dropdown_reject_assignment">
						PLACEHOLDER_MESSAGES_REJECT
					</div>
	            </div>
			
				<div class="btn-group btn-group-sm">
	            	<button type="button" name="task" value="button_mturk_reject__PLACEHOLDER_ID" data-id_assignment="PLACEHOLDER_ID" class="btn PLACEHOLDER_APPROVE_INTERNALLY approve_internally_assignment" PLACEHOLDER_DISABLED>Approve internally</button>
	            	<button type="button" class="btn PLACEHOLDER_APPROVE_INTERNALLY dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" PLACEHOLDER_DISABLED></button>
					<div class="dropdown-menu dropdown_approve_internally_assignment">
						PLACEHOLDER_MESSAGES_REJECT
					</div>
	        	</div>
	        </div>
		`.replace(/PLACEHOLDER_ID/g, assignment.id);

    if (assignment.status_external != null) {
      result = result.replace(/PLACEHOLDER_DISABLED/g, 'disabled');
      if (assignment.status_external == STATUS_EXTERNAL.APPROVED) {
        if (assignment.status_internal == STATUS_INTERNAL.REJECTED) {
          result = result
            .replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
            .replace(/PLACEHOLDER_DANGER/g, 'btn-light')
            .replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
            .replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-warning');
        } else {
          result = result
            .replace(/PLACEHOLDER_SUCCESS/g, 'btn-success')
            .replace(/PLACEHOLDER_DANGER/g, 'btn-light')
            .replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
            .replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light');
        }
      } else if (assignment.status_external == STATUS_EXTERNAL.REJECTED) {
        if (assignment.status_internal == STATUS_INTERNAL.APPROVED) {
          result = result
            .replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-warning')
            .replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light')
            .replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
            .replace(/PLACEHOLDER_DANGER/g, 'btn-light');
        } else {
          result = result
            .replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
            .replace(/PLACEHOLDER_DANGER/g, 'btn-danger')
            .replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
            .replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light');
        }
      }
    } else {
      result = result
        .replace(/PLACEHOLDER_SUCCESS/g, 'btn-success')
        .replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-warning')
        .replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-warning')
        .replace(/PLACEHOLDER_DANGER/g, 'btn-danger');
    }

    let messages_reject = '';
    _.forEach(this.loader.array_messages_reject, (message_reject) => {
      messages_reject += `<a class="dropdown-item" data-id_assignment="${
        assignment.id
      }" href="#">${message_reject.message}</a>`;
    });
    result = result.replace(/PLACEHOLDER_MESSAGES_REJECT/g, messages_reject);

    return result;
  }
}
