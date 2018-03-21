from django import forms

class Bootstrap_Select(forms.Select):
    def __init__(self, small=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        classes_default = 'custom-select '
        if small:
            classes_default += 'custom-select-sm '
        try:
            self.attrs['class'] = classes_default + self.attrs['class']
        except KeyError:
            self.attrs['class'] =  classes_default

class Bootstrap_TextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        classes_default = 'form-control '
        try:
            self.attrs['class'] = classes_default + self.attrs['class']
        except KeyError:
            self.attrs['class'] =  classes_default

class Bootstrap_NumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        classes_default = 'form-control '
        try:
            self.attrs['class'] = classes_default + self.attrs['class']
        except KeyError:
            self.attrs['class'] =  classes_default

class Bootstrap_FileInput(forms.FileInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        classes_default = 'custom-file-input '
        try:
            self.attrs['class'] = classes_default + self.attrs['class']
        except KeyError:
            self.attrs['class'] =  classes_default

# class Bootstrap_CheckboxInput(forms.CheckboxInput):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         classes_default = 'form-control '
#         try:
#             self.attrs['class'] = classes_default + self.attrs['class']
#         except KeyError:
#             self.attrs['class'] =  classes_default