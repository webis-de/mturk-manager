import Loader from './loader'
import View from './view'
import _ from 'lodash';
import { add_to_object_assignments_selected } from './helpers';

export default class Controller
{
	constructor() 
	{
		this.loader = new Loader();
		this.view = new View(this.loader);
	}

	async init()
	{
		this.init_events();

		await this.loader.sync_data();
		this.view.update();
	}

	init_events()
	{
		$(document).on(
			'click', 
			'.approve_assignment, .reject_assignment, .reject_internally_assignment, .approve_internally_assignment', 
			{ 
				loader: this.loader, 
				view: this.view 
			},
			function(event) 
			{
				const elem_button = $(this);
				const id_assignment = elem_button.data('id_assignment');

				if(elem_button.hasClass('active'))
				{
					delete event.data.loader.object_assignments_selected[id_assignment];
					elem_button.removeClass('active');
				} else {
					if(elem_button.hasClass('approve_assignment'))
					{
						add_to_object_assignments_selected(event.data.loader, id_assignment, 'approve', undefined)
					} else if(elem_button.hasClass('reject_assignment')) {
						add_to_object_assignments_selected(event.data.loader, id_assignment, 'reject', undefined)
					} else if(elem_button.hasClass('reject_internally_assignment')) {
						add_to_object_assignments_selected(event.data.loader, id_assignment, 'reject_internally', undefined)
					} else if(elem_button.hasClass('approve_internally_assignment')) {
						add_to_object_assignments_selected(event.data.loader, id_assignment, 'approve_internally', undefined)
					}
					elem_button.addClass('active');
				}

				event.data.view.update_info();
				event.data.view.check_submit_button();
			}
		);

		$(document).on(
			'click', 
			'[data-task="submit_annotations"]',  
			{ 
				loader: this.loader, 
				view: this.view 
			},
			async function(event) 
			{
				const data = {
					message_reject_default: event.data.loader.message_reject_default,
					assignments: event.data.loader.object_assignments_selected,
				};

				const result = await $.ajax({
			        url: event.data.loader.context.url_api_assignments,
			        method: 'PUT',
			        contentType: 'application/json',
			        data: JSON.stringify(data),
			        headers: {
			            Authorization: 'Token ' + event.data.loader.context.token_instance,
			            "Content-Type": 'application/json',
			        },
			    }).done((data) => {
			    	location.reload();
			    });
			}
		);

		$(document).on(
			'change', 
			'#input_select_groupby',  
			{ 
				loader: this.loader, 
				view: this.view 
			},
			async function(event) 
			{
				event.data.view.group_by = $(this).val();
				event.data.view.inject_templates();
			}
		);

		$(document).on(
			'click', 
			'.dropdown_reject_assignment a', 
			{ 
				loader: this.loader, 
				view: this.view 
			},
			function(event) 
			{
				const elem_link = $(this);
				const id_assignment = elem_link.data('id_assignment');
				const message = elem_link.text();
				
				add_to_object_assignments_selected(event.data.loader, id_assignment, 'reject', message)
				
				$('.reject_assignment[data-id_assignment="'+id_assignment+'"]').addClass('active');

				event.data.view.update_info();
				event.data.view.check_submit_button();
			}
		);
		// changes of default reject message
		$(document).on(
			'input', 
			'#message_reject_default',  
			{ 
				loader: this.loader, 
				view: this.view, 
			},
			async function(event) 
			{
				event.data.loader.message_reject_default = $(this).val();
				event.data.view.check_submit_button();
			}
		);
		// prevent data loss
		window.onbeforeunload = () => {
			if(_.size(this.loader.object_assignments_selected) > 0)
			{
		    	return 'You have unsaved changes!';
			}
		}
	}
}