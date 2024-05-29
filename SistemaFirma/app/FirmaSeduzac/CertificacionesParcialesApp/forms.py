from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class CURPForm(forms.Form):
    curp = forms.CharField(label='CURP',
                           max_length=18,
                           widget=forms.TextInput(attrs={'class': 'form-control','style':'width: 300px'})
                           )

class RegistrosParcialesForm(forms.Form):
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
    semestre = forms.IntegerField(
    label="Semestre",
    widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
)