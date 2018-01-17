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
});