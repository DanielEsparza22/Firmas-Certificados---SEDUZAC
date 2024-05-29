from django import forms

class CertificacionPForm(forms.Form):
    curp = forms.CharField(
        label='CURP',
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px'})
    )
