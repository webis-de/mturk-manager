from django import forms

# forms.ChoiceField(label='jo', help_text="d 4 weeks (default 3).")
class Bootstrap_Select(forms.Select):
    def __init__(self, *args, **kwargs):
        super(Bootstrap_Select, self).__init__(*args, **kwargs)

        classes_default = 'custom-select '
        try:
            self.attrs['class'] = classes_default + self.attrs['class']
        except KeyError:
            self.attrs['class'] =  classes_default

