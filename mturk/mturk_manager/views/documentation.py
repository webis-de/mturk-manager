from django.shortcuts import render

def documentation(request):
    context = {}

    context['templates'] = get_contents_spoiler()
    return render(request, 'mturk_manager/documentation.html', context)

def get_contents_spoiler():
    return {
        'template_html': '''<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
        <script type='text/javascript' src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js'></script>
    </head>
    <body>
        <form name='mturk_form' method='post' id='mturk_form' action='https://www.mturk.com/mturk/externalSubmit'>
        <input type='hidden' value='' name='assignmentId' id='assignmentId'/>
        <h1>What's up?</h1>
        <p><textarea name='comment' cols='80' rows='3'></textarea></p>
        <p><input type='submit' id='submitButton' value='Submit' /></p></form>
        <script language='Javascript'>turkSetAssignmentID();</script>
    </body>
</html>''',
        'template_html_requester_hit_template_default': '''<div class="col-12">
    <div data-inject_assignments></div>
</div>''',
        'template_html_requester_hit_template_example': '''<div class="col-12">
    <div class="input_text"></div>
    <div data-inject_assignments></div>
</div>
<script>
    var input_text = question.column1;
    hit_wrapper.find('.input_text').text(input_text);
</script>''',
        'template_html_requester_assignment_template_example': '''<div class="col-12">
    <div class="input_text"></div>
    <div data-inject_input_forms></div>
</div>
<script>
    var input_text = answer.input1;
    assignment_wrapper.find('.input_text').text(input_text);
</script>'''
    }