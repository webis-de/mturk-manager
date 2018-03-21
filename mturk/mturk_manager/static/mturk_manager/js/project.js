$(document).ready(function()
{
	$('#modal_update_template').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const name = button.data('name') // Extract info from data-* attributes
		const height_frame = button.data('height_frame') // Extract info from data-* attributes
		const id_template_assignment = button.data('id_template_assignment') // Extract info from data-* attributes
		const id_template_hit = button.data('id_template_hit') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="name"]').val(name);
		modal.find('input[name="height_frame"]').val(height_frame);
		modal.find('select[name="template_assignment"]').val(id_template_assignment);
		modal.find('select[name="template_hit"]').val(id_template_hit);
	})

	$('#modal_update_template_assignment').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const name = button.data('name') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="name"]').val(name);
	})

	$('#modal_update_template_hit').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const name = button.data('name') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="name"]').val(name);
	})

	$('#modal_update_template_global').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const name = button.data('name') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="name"]').val(name);
	})

	$('#modal_update_message_reject').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const message = button.data('message') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="message"]').val(message);
	})

	$.ajax({
        url: window.location.href + '/api/balance',
        success: function(result) {
        	$('#balance_mturk_current').text(result.balance + '$');
        }
    })
});
