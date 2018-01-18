$(document).ready(function()
{
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