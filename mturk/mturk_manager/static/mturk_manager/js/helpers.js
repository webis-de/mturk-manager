function inject_templates()
{
	console.log('OBJECT_BATCHES', OBJECT_BATCHES);
	console.log('OBJECT_HITS', OBJECT_HITS);
	console.log('OBJECT_ASSIGNMENTS', OBJECT_ASSIGNMENTS);
	_wrapper_assignments.append(create_inputs('kritten', 'submitted'));
	_.forEach(OBJECT_ASSIGNMENTS, function(assignment)
	{

		// var wrapper_assignment = $($.parseHTML('<span></span>'));
		var wrapper_assignment = $($.parseHTML('<span data-id_assignment="'+assignment.id+'"></span>'));
		// var _assignment_prepared = {
		// 	id: _assignment.id,
		// 	id_assignment: _assignment.id_assignment,
		// 	answer: normalize_answer(_assignment.answer),
		// };

		var _id_assignment = assignment.id;
		// wrapper_assignment.data('assignment', _assignment_prepared);
		wrapper_assignment.data('assignment', assignment);

		// wrapper_assignment.append('<script>var assignment_wrapper = $(\'span[data-id_assignment="'+_id_assignment+'"]\');</script>');
		wrapper_assignment.append('<script>var assignment_wrapper = $(\'span[data-id_assignment="'+_id_assignment+'"]\'); var assignment = assignment_wrapper.data("assignment")</script>');
		
		var _template_assignment = assignment.hit.batch.settings_batch.template.template_assignment.template;
		wrapper_assignment.append(_template_assignment);
		_wrapper_assignments.append(wrapper_assignment);
	});
}

function load_assignments()
{
	var url = CONTEXT.url_api_assignments.replace('PLACEHOLDER_SLUG_PROJECT', CONTEXT.slug_project);
	url += '?list_ids=['+CONTEXT.list_ids.join(',')+']';

	$.ajax({
        url: url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
            Authorization: 'Token ' + CONTEXT.token_instance,
            "Content-Type": 'application/json',
        },
    }).done(function(result) {
		_.forEach(result, function(assignment) {
			set_ids_worker.add(assignment.worker);
			assignment.answer = normalize_answer(assignment.answer);
    		OBJECT_ASSIGNMENTS[assignment.id] = assignment;
		});
    	load_hits();
    });
}

function load_hits()
{
	set_ids_hit = new Set();
	_.forEach(OBJECT_ASSIGNMENTS, function(assignment) {
		set_ids_hit.add(assignment.hit);
	});

	var url = CONTEXT.url_api_hits.replace('PLACEHOLDER_SLUG_PROJECT', CONTEXT.slug_project);
	url += '?list_ids=['+_.toArray(set_ids_hit).join(',')+']';

	$.ajax({
        url: url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
            Authorization: 'Token ' + CONTEXT.token_instance,
            'Content-Type': 'application/json',
        },
    }).done(function(result) {
		_.forEach(result, function(hit) {
			hit.parameters = JSON.parse(hit.parameters);
    		OBJECT_HITS[hit.id] = hit;
		});

		_.forEach(OBJECT_ASSIGNMENTS, function(assignment) {
			const hit = OBJECT_HITS[assignment.hit];
			assignment.hit = hit;

			if(hit.assignments == undefined)
			{
				hit.assignments = [assignment];
			} else {
				hit.assignments.push(assignment);
			}
		});
		load_batches()
    });
}

function load_batches()
{
	set_ids_batch = new Set();
	_.forEach(OBJECT_HITS, function(hit) {
		set_ids_batch.add(hit.batch);
	});

	var url = CONTEXT.url_api_batches.replace('PLACEHOLDER_SLUG_PROJECT', CONTEXT.slug_project);
	url += '?list_ids=['+_.toArray(set_ids_batch).join(',')+']';

	$.ajax({
        url: url,
        method: 'GET',
        contentType: 'application/json',
        headers: {
            Authorization: 'Token ' + CONTEXT.token_instance,
            'Content-Type': 'application/json',
        },
    }).done(function(result) {
		_.forEach(result, function(batch) {
    		OBJECT_BATCHES[batch.id] = batch;
		});

		_.forEach(OBJECT_HITS, function(hit) {
			const batch = OBJECT_BATCHES[hit.batch];
			hit.batch = batch;

			if(batch.hits == undefined)
			{
				batch.hits = [hit];
			} else {
				batch.hits.push(hit);
			}
		});
		load_workers();
    });
}

function load_workers() {
	// var list_ids = _.toArray(set_ids_worker);
	var url = CONTEXT.url_api_workers.replace('PLACEHOLDER_SLUG_PROJECT', CONTEXT.slug_project);
	// url += '?list_ids=['+CONTEXT.list_ids.join(',')+']';
	console.log(url)
	$.ajax({
        url: url,
        method: 'PATCH',
        data: JSON.stringify(_.toArray(set_ids_worker)),
        contentType: 'application/json',
        headers: {
            Authorization: 'Token ' + CONTEXT.token_instance,
            "Content-Type": 'application/json',
        },
    }).done(function(result) {
		_.forEach(result, function(worker) {
    		OBJECT_WORKERS[worker.id] = worker;
		});

		_.forEach(OBJECT_ASSIGNMENTS, function(assignment) {
			assignment.worker = OBJECT_WORKERS[assignment.worker];
		});

		inject_templates();
    });
}


function create_inputs(id, state='submitted')
{
	console.log(state);
	let result = `
		<div class="custom-control custom-checkbox d-inline">
			<input type="checkbox" data-kritten_checkbox="checkbox" class="custom-control-input" id="checkbox_assignment_PLACEHOLDER_ID" data-id_assignment="PLACEHOLDER_ID" name="checkbox_assignment" value="PLACEHOLDER_ID" PLACEHOLDER_DISABLED>
			<label class="custom-control-label" for="checkbox_assignment_PLACEHOLDER_ID"></label>
		</div>

		<div class="btn-group btn-group-sm">
			<button type="button" data-id_assignment="PLACEHOLDER_ID" class="btn btn-sm PLACEHOLDER_SUCCESS approve_assignment" PLACEHOLDER_DISABLED>Approve</button>
			<button type="button" data-id_assignment="PLACEHOLDER_ID" class="btn btn-sm PLACEHOLDER_REJECT_INTERNALLY reject_internally_assignment" PLACEHOLDER_DISABLED>Reject internally</button>
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
	`.replace(/PLACEHOLDER_ID/g, id)

	if(state != 'submitted') 
	{
		result = result.replace(/PLACEHOLDER_DISABLED/g, 'disabled')
		if(state == 'approved')
		{
			result = result
			.replace(/PLACEHOLDER_SUCCESS/g, 'btn-success')
			.replace(/PLACEHOLDER_DANGER/g, 'btn-light')
			.replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
			.replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light')
		} else if(state == 'rejected') {
			result = result
			.replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
			.replace(/PLACEHOLDER_DANGER/g, 'btn-danger')
			.replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
			.replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light')
		} else if(state == 'rejected_externally') {
			result = result
			.replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-warning')
			.replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-light')
			.replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
			.replace(/PLACEHOLDER_DANGER/g, 'btn-light')
		} else if(state == 'approved_externally') {
			result = result
			.replace(/PLACEHOLDER_SUCCESS/g, 'btn-light')
			.replace(/PLACEHOLDER_DANGER/g, 'btn-light')
			.replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-light')
			.replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-warning')
		}
	} else {
		result = result
		.replace(/PLACEHOLDER_SUCCESS/g, 'btn-success')
		.replace(/PLACEHOLDER_REJECT_INTERNALLY/g, 'btn-warning')
		.replace(/PLACEHOLDER_APPROVE_INTERNALLY/g, 'btn-warning')
		.replace(/PLACEHOLDER_DANGER/g, 'btn-danger')
	}

	messages_reject = '';
	// $.each(list_messages_reject, function(index, message) {
	// 	messages_reject += '<a class="dropdown-item" data-id_assignment="'+id+'" href="#">'+message+'</a>'
	// });
	result = result.replace(/PLACEHOLDER_MESSAGES_REJECT/g, messages_reject);

	return result
}