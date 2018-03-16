from mturk_manager.models import *
from django import forms
from .widgets_bootstrap import *

class Form_Create_Project(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_mturk'].queryset = m_Account_Mturk.objects.all()
        self.auto_id='form_create_%s'

    name = forms.CharField(max_length=200, widget=Bootstrap_TextInput(attrs={'placeholder': 'Name of the project'}))
    account_mturk = forms.ModelChoiceField(queryset=None, empty_label=None, widget=Bootstrap_Select())
