$(document).ready(function()
{
	let glob_dict_assignemnts = {};

	$(document).on('click', '.approve_assignment, .reject_assignment', function(e) {
		const elem_button = $(this);
		const id_assignment = elem_button.data('id_assignment');

		if(elem_button.hasClass('active'))
		{
			delete glob_dict_assignemnts[id_assignment];
			elem_button.removeClass('active');
		} else {
			if(elem_button.hasClass('approve_assignment'))
			{
				glob_dict_assignemnts[id_assignment] = {
					state: 'approve',
					message: undefined
				};
				const elem_button_reject = $('.reject_assignment[data-id_assignment="'+id_assignment+'"]');
				elem_button_reject.removeClass('active');
			} else {
				glob_dict_assignemnts[id_assignment] = {
					state: 'reject',
					message: undefined
				};
				const elem_button_approve = $('.approve_assignment[data-id_assignment="'+id_assignment+'"]');
				elem_button_approve.removeClass('active');
			}

			elem_button.addClass('active');
		}

		print_dict_assignment();
	});

	$(document).on('click', '[data-task="submit_annotations"]', function(e) {
		const data = {};
		data.task = 'submit_annotations';
		data.dict_assignments = glob_dict_assignemnts;
		data.message_reject_default = $('#input_message_reject_default').val();

		if(data.message_reject_default.trim() == '')
		{
			let need_message_reject_default = false;
			$.each(data.dict_assignments, function(i, e) {
				if(e.message == undefined && e.state == 'reject')
				{
					need_message_reject_default = true;
					return false;
				}
			});

			if(need_message_reject_default)
			{
				$('#input_message_reject_default').parent().addClass('was-validated');
				return
			}
		}

		$.ajax({
	        url: '',
	        method: 'POST',
	        contentType: 'application/json',
	        headers: {'X-CSRFToken':$('input[name="csrfmiddlewaretoken"]').val()},
	        data: JSON.stringify(data),
	        success: function(result) {
			   	glob_dict_assignemnts = {};     	
	        	location.reload();
	        }
	    })
	});

	$(document).on('click', '[data-task="button_mturk_reject_selected"]', function(e) {
		const elem_button = $(this);

		$('input[name="checkbox_assignment"]:checked').each(function(index) {
			const elem_checkbox = $(this);
			const id_assignment = elem_checkbox.data('id_assignment');

			const elem_button_approve = $('.approve_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_approve.removeClass('active');
			
			const elem_button_reject = $('.reject_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_reject.addClass('active');

			glob_dict_assignemnts[id_assignment] = {
				state: 'reject',
				message: undefined
			};

			elem_checkbox.prop('checked', false);
		})

		print_dict_assignment();
	});

	$(document).on('click', '[data-task="button_mturk_approve_selected"]', function(e) {
		const elem_button = $(this);

		$('input[name="checkbox_assignment"]:checked').each(function(index) {
			const elem_checkbox = $(this);
			const id_assignment = elem_checkbox.data('id_assignment');

			const elem_button_approve = $('.approve_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_approve.addClass('active');
			
			const elem_button_reject = $('.reject_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_reject.removeClass('active');

			glob_dict_assignemnts[id_assignment] = {
				state: 'approve',
				message: undefined
			};

			elem_checkbox.prop('checked', false);
		})

		print_dict_assignment();
	});

	$(document).on('click', '.dropdown_reject_assignment_selected a', function(e) {
		const elem_link = $(this);

		$('input[name="checkbox_assignment"]:checked').each(function(index) {
			const elem_checkbox = $(this);
			const id_assignment = elem_checkbox.data('id_assignment');

			const elem_button_approve = $('.approve_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_approve.removeClass('active');
			
			const elem_button_reject = $('.reject_assignment[data-id_assignment="'+id_assignment+'"]');
			elem_button_reject.addClass('active');

			glob_dict_assignemnts[id_assignment] = {
				state: 'reject',
				message: elem_link.text()
			};

			elem_checkbox.prop('checked', false);
		});

		print_dict_assignment();
	});

	$(document).on('click', '.dropdown_reject_assignment a', function(e) {
		const elem_link = $(this);
		const id_assignment = elem_link.data('id_assignment');

		glob_dict_assignemnts[id_assignment] = {
			state: 'reject',
			message: elem_link.text()
		};
		
		const elem_button = $('.reject_assignment[data-id_assignment="'+id_assignment+'"]');
		elem_button.addClass('active');

		const elem_button_approve = $('.approve_assignment[data-id_assignment="'+id_assignment+'"]');
		elem_button_approve.removeClass('active');
		
		print_dict_assignment();
	});

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

	function print_dict_assignment()
	{
		$('pre').text(JSON.stringify(glob_dict_assignemnts, null, 2));
	}
});