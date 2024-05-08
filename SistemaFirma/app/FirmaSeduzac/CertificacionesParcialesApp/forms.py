from django import forms

class CURPForm(forms.Form):
    curp = forms.CharField(label='CURP',
                           max_length=18,
                           widget=forms.TextInput(attrs={'class': 'form-control','style':'width: 300px'})
                           )
