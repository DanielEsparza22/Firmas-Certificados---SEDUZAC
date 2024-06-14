from django import forms

class CertificacionCForm(forms.Form):
    curp = forms.CharField(
        label='CURP',
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px'})
    )

class RegistrosCompletasForm(forms.Form):
    clave_alumno = forms.CharField(
        label="Clave del Alumno",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_certificacion = forms.DateField(
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    bachillerato = forms.CharField(
        label="Bachillerato",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width:300px', 'placeholder':'BACHILLERATO GENERAL por defecto'}),
        required=False,
    )

class LetraFoliadorForm(forms.Form):
    letra_foliador = forms.CharField(
        label = "Letra",
        max_length=1,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
