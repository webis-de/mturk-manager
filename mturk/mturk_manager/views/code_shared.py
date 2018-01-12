import boto3
from mturk_manager.models import *
from viewer.models import *
from secrets import token_urlsafe

glob_url_sandbox = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

def glob_create_batch(db_obj_project, request):
    name = request.POST['name']
    if name.strip() == '':
        name = token_urlsafe()

    return m_Batch.objects.create(
        name=name,
        fk_project=db_obj_project,
        title=request.POST['title'],
        description=request.POST['description'],
        keywords=request.POST['keywords'],
        count_assignments=request.POST['count_assignments'],
        use_sandbox=True if request.POST['use_sandbox'] == '1' else False,
        reward=request.POST['reward'],
        lifetime=request.POST['lifetime'],
        duration=request.POST['duration'],
        fk_template=m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template']),
    )

def create_question(template, height_frame, dict_parameters):
    for key, value in dict_parameters.items():
        template = template.replace('${'+key+'}', value)

    return '''
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
            <HTMLContent><![CDATA['''+template+''']]></HTMLContent>
            <FrameHeight>'''+str(height_frame)+'''</FrameHeight>
        </HTMLQuestion>'''

def get_client(db_obj_project, use_sandbox=True):
    if use_sandbox:
        return boto3.client('mturk',
            aws_access_key_id=db_obj_project.fk_account_mturk.key_access,
            aws_secret_access_key=db_obj_project.fk_account_mturk.key_secret,
            region_name='us-east-1',
            endpoint_url=glob_url_sandbox
        )
    else:
        return boto3.client('mturk',
            aws_access_key_id=db_obj_project.fk_account_mturk.key_access,
            aws_secret_access_key=db_obj_project.fk_account_mturk.key_secret,
            region_name='us-east-1'
        )
