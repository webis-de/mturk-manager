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

	$('#modal_update_message_reject').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const message = button.data('message') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="message"]').val(message);
	})

	$('#modal_show_html').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const template = button.data('template') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('code').text(template);
		$('pre code').each(function(i, block) {
	    	hljs.highlightBlock(block);
	  	});
	})

	$('#modal_update_account').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const id = button.data('id') // Extract info from data-* attributes
		const name = button.data('name') // Extract info from data-* attributes
		const key_secret = button.data('key_secret') // Extract info from data-* attributes
		const key_access = button.data('key_access') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('input[name="id"]').val(id);
		modal.find('input[name="name"]').val(name);
		modal.find('input[name="key_secret"]').val(key_secret);
		modal.find('input[name="key_access"]').val(key_access);
	})
});