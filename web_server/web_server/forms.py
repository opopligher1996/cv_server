from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    CHOICES=[('1','level 1'),
         ('2','level 2')]
    level = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
