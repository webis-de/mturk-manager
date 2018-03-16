from mturk_manager.models import *
from django import forms
from .widgets_bootstrap import *

class Form_Open(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_project'].queryset = m_Project.objects.all()
        self.auto_id ='form_dashboard_%s'

    name_project = forms.ModelChoiceField(queryset=None, empty_label='Select a project', widget=Bootstrap_Select())
