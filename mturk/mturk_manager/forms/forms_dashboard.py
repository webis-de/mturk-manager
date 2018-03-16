from django import forms
from .widgets_bootstrap import *

class Form_Dashboard(forms.Form):
    def __init__(self, choices, *args, **kwargs):
        self.base_fields['name_project'].choices = [('', 'Select a project')] + choices
        super(Form_Dashboard, self).__init__(*args, **kwargs)
        self.auto_id='form_dashboard_%s'

    name_project = forms.ChoiceField(label='adwa', widget=Bootstrap_Select())
