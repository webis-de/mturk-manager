from mturk_manager.models import *
from django import forms
from .widgets_bootstrap import *

class Form_Update_Project(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print(args)
        print(kwargs)
        super().__init__(*args, **kwargs)
        self.fields['fk_template_main'].queryset = kwargs['instance'].templates
        self.fields['fk_template_assignment_main'].queryset = kwargs['instance'].templates_assignment
        self.auto_id ='form_update_project_%s'
        
    fk_template_main = forms.ModelChoiceField(queryset=None, label='Default worker template', empty_label='Please select a template', widget=Bootstrap_Select(small=True))
    fk_template_assignment_main = forms.ModelChoiceField(queryset=None, label='Default requester assignment template', empty_label='Please select a template', widget=Bootstrap_Select(small=True))


    class Meta:
        model = m_Project
        fields = [
            'title',
            'description',
            'reward',
            'count_assignments',
            'lifetime',
            'duration',
            'keywords',
            'use_sandbox',
            'fk_template_main',
            'fk_template_assignment_main',
            'fk_template_hit_main',
            'fk_template_global_main',
            'fk_message_reject_default',
            'fk_message_block_default',
            'block_workers',
        ]
        widgets = {
            'title': Bootstrap_TextInput(),
            'description': Bootstrap_TextInput(),
            'reward': Bootstrap_NumberInput(attrs={'step': '0.01'}),
            'count_assignments': Bootstrap_NumberInput(),
            'lifetime': Bootstrap_NumberInput(),
            'duration': Bootstrap_NumberInput(),
            'keywords': Bootstrap_TextInput(),
            'use_sandbox': forms.CheckboxInput(),
        }
        labels = {
            'count_assignments': '#Assignements',
            'keywords': 'Keywords (comma-separated)',
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['account_mturk'].queryset = m_Account_Mturk.objects.all()
    #     self.auto_id='form_create_%s'

    # name = forms.CharField(max_length=200, widget=Bootstrap_TextInput(attrs={'placeholder': 'Name of the project'}))
    # account_mturk = forms.ModelChoiceField(queryset=None, empty_label=None, widget=Bootstrap_Select())
