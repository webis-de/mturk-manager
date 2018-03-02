$(document).ready(function()
{
	setTimeout(function() {
		$('.wrapper_alert.custom-alert-success').animate({height: 0}, 1000, function(){
			$(this).remove()
		})
	}, 1000);

	$('.custom-file-input').on('change',function(){
	    const name_file = $(this)[0].files[0].name;
	    $(this).parent().find('span').text(name_file);
	})

	$('#modal_show_html').on('show.bs.modal', function (event) 
	{
		const button = $(event.relatedTarget) // Button that triggered the modal
		const template = button.data('template') // Extract info from data-* attributes
		const type = button.data('type') // Extract info from data-* attributes
		const modal = $(this)

		modal.find('code').removeClass()
		if(type != undefined)
		{
			modal.find('code').addClass(type)
		} else {
			modal.find('code').addClass('html')
		}

		modal.find('code').text(template);
		$('pre code').each(function(i, block) {
	    	hljs.highlightBlock(block);
	  	});
	})

	$('[data-type="info"]').popover({
		// trigger: 'click',
		trigger: 'focus',
		container: 'body',
		'html': true,
	});
});