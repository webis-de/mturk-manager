$(document).ready(function()
{
	let glob_dict_assignemnts = {};

	// $(document).on('click', '.approve_assignment, .reject_assignment, .reject_internally_assignment, .approve_internally_assignment', function(e) {
	// 	const elem_button = $(this);
	// 	const id_assignment = elem_button.data('id_assignment');

	// 	if(elem_button.hasClass('active'))
	// 	{
	// 		delete glob_dict_assignemnts[id_assignment];
	// 		elem_button.removeClass('active');
	// 	} else {
	// 		if(elem_button.hasClass('approve_assignment'))
	// 		{
	// 			glob_dict_assignemnts[id_assignment] = {
	// 				state: 'approve',
	// 				message: undefined
	// 			};
	// 			$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
	// 		} else if(elem_button.hasClass('reject_assignment')) {
	// 			glob_dict_assignemnts[id_assignment] = {
	// 				state: 'reject',
	// 				message: undefined
	// 			};
	// 			$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
	// 		} else if(elem_button.hasClass('reject_internally_assignment')) {
	// 			glob_dict_assignemnts[id_assignment] = {
	// 				state: 'reject_internally',
	// 				message: undefined
	// 			};
	// 			$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
	// 		} else if(elem_button.hasClass('approve_internally_assignment')) {
	// 			glob_dict_assignemnts[id_assignment] = {
	// 				state: 'approve_internally',
	// 				message: undefined
	// 			};
	// 			$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
	// 		}
	// 		elem_button.addClass('active');
	// 	}

	// 	update_info();
	// });

	$(document).on('click', '#checkbox_assignments_main0', function() {
		if($(this).is(':checked')) 
		{
			$.each($('[name="checkbox_assignment"]'), function(i, e) {
				$(e).prop('checked', true);
			});
			$('.wrapper_buttons_selected button').prop('disabled', '');
			$('.wrapper_buttons_selected .dropdown-toggle.dropdown-toggle-split').prop('disabled', '');

		} else {
			
			$.each($('[name="checkbox_assignment"]'), function(i, e) {
				$(e).prop('checked', false);
			});
			$('.wrapper_buttons_selected button').prop('disabled', 'disabled');
			$('.wrapper_buttons_selected .dropdown-toggle.dropdown-toggle-split').prop('disabled', 'disabled');
		}
		const count_assignments_selected = $('[name="checkbox_assignment"]:checked').length;
		$('[data-inject_count_assignments_selected]').text(count_assignments_selected);
	});

	$(document).on('click', '[name="checkbox_assignment"]', function() {
		const count_assignments_selected = $('[name="checkbox_assignment"]:checked').length;
		$('[data-inject_count_assignments_selected]').text(count_assignments_selected);
		
		if(count_assignments_selected == 0)
		{
			$('.wrapper_buttons_selected button').prop('disabled', 'disabled');
			$('.wrapper_buttons_selected .dropdown-toggle.dropdown-toggle-split').prop('disabled', 'disabled');
		} else {
			$('.wrapper_buttons_selected button').prop('disabled', '');
			$('.wrapper_buttons_selected .dropdown-toggle.dropdown-toggle-split').prop('disabled', '');
		}
	});

	// $(document).on('click', '[data-task="submit_annotations"]', function(e) {
	// 	const data = {};
	// 	data.task = 'submit_annotations';
	// 	data.dict_assignments = glob_dict_assignemnts;
	// 	data.softblock_on_reject = $('#input_softblock_on_reject').is(':checked');
	// 	data.extend_hit_on_reject = $('#input_extend_hit_on_reject').is(':checked');
	// 	data.message_reject_default = $('#input_message_reject_default').val();

	// 	if(data.message_reject_default.trim() == '')
	// 	{
	// 		let need_message_reject_default = false;
	// 		$.each(data.dict_assignments, function(i, e) {
	// 			if(e.message == undefined && e.state == 'reject' || e.message == undefined && e.state == 'approve_internally')
	// 			{
	// 				need_message_reject_default = true;
	// 				return false;
	// 			}
	// 		});

	// 		if(need_message_reject_default)
	// 		{
	// 			$('#input_message_reject_default').parent().addClass('was-validated');
	// 			return
	// 		}
	// 	}

	// 	$.ajax({
	//         url: '',
	//         method: 'POST',
	//         contentType: 'application/json',
	//         headers: {'X-CSRFToken':$('input[name="csrfmiddlewaretoken"]').val()},
	//         data: JSON.stringify(data),
	//         success: function(result) {
	// 		   	glob_dict_assignemnts = {};     	
	//         	location.reload();
	//         }
	//     })
	// });

	$(document).on('click', '[data-task="button_mturk_approve_selected"], [data-task="button_mturk_reject_selected"]', function(e) {
		if($(this).data('task') == 'button_mturk_approve_selected')
		{
			handle_selected('approve');
		} else {
			handle_selected('reject');
		}
		update_info();
	});

	$(document).on('click', '[data-task="button_mturk_approve_internally_selected"], [data-task="button_mturk_reject_internally_selected"]', function(e) {
		if($(this).data('task') == 'button_mturk_approve_internally_selected')
		{
			handle_selected('approve_internally');
		} else {
			handle_selected('reject_internally');
		}
		update_info();
	});

	$(document).on('click', '.dropdown_approve_internally_selected a', function(e) {
		const elem_link = $(this);
		const message = elem_link.text();
		handle_selected('approve_internally', message);

		update_info();
	});

	$(document).on('click', '.dropdown_reject_assignment_selected a', function(e) {
		const elem_link = $(this);
		const message = elem_link.text();
		handle_selected('reject', message);

		update_info();
	});

	$(document).on('click', '.dropdown_approve_internally_assignment a', function(e) {
		const elem_link = $(this);
		const id_assignment = elem_link.data('id_assignment');
		const message = elem_link.text();

		glob_dict_assignemnts[id_assignment] = {
			state: 'approve_internally',
			message: message
		};
		
		$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
		$('.approve_internally_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');

		update_info();			
	});

	// $(document).on('click', '.dropdown_reject_assignment a', function(e) {
	// 	const elem_link = $(this);
	// 	const id_assignment = elem_link.data('id_assignment');
	// 	const message = elem_link.text();

	// 	glob_dict_assignemnts[id_assignment] = {
	// 		state: 'reject',
	// 		message: message
	// 	};
		
	// 	$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');
	// 	$('.reject_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');

	// 	update_info();
	// });

	$(document).on('click', '.dropdown-menu a', function(e) {
		e.preventDefault();
	});

	$(document).on('click', 'button', function(e) {
		$(this).blur();
	});
	
	$(document).on('click', '#dropdown_message_reject_default a', function(e) {
		$('#input_message_reject_default').val($(this).text());
	});

	window.onbeforeunload = function() {
		if(Object.keys(glob_dict_assignemnts).length > 0)
		{
	    	return 'You have unsaved changes!';
		}
	}

	function handle_selected(state, message=undefined)
	{
		$('input[name="checkbox_assignment"]:checked').each(function(index) {
			const elem_checkbox = $(this);
			const id_assignment = elem_checkbox.data('id_assignment');

			$('button[data-id_assignment="'+id_assignment+'"]').removeClass('active');

			switch(state) {
				case 'approve':
				 	$('.approve_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');
				 	break;
				case 'reject':
				 	$('.reject_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');
				 	break;
				case 'approve_internally':
				 	$('.approve_internally_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');
				 	break;
				case 'reject_internally':
				 	$('.reject_internally_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');
				 	break;
			}
			
			glob_dict_assignemnts[id_assignment] = {
				state: state,
				message: message
			};

			elem_checkbox.prop('checked', false);
		})

	}

	function update_info()
	{
		let count_approved_assignments = 0;
		let count_rejected_assignments = 0;
		let count_rejected_internally_assignments = 0;
		let count_approved_internally_assignments = 0;

		$.each(glob_dict_assignemnts, function(index, elem) {
			switch(elem.state) {
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

		$('pre').text(JSON.stringify(glob_dict_assignemnts))

		$('[data-inject_count_approved_assignments]').text(count_approved_assignments)
		$('[data-inject_count_rejected_assignments]').text(count_rejected_assignments)
		$('[data-inject_count_rejected_internally_assignments]').text(count_rejected_internally_assignments)
		$('[data-inject_count_approved_internally_assignments]').text(count_approved_internally_assignments)
	}
});