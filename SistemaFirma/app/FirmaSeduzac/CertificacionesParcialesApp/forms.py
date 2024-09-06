from django import forms
from ConfiguracionApp.models import Bachillerato

class CURPForm(forms.Form):
    curp = forms.CharField(label='CURP',
                           max_length=18,
                           widget=forms.TextInput(attrs={'class': 'form-control','style':'width: 300px'})
                           )

class RegistrosParcialesForm(forms.Form):
    # clave_alumno = forms.CharField(
    #     label="Clave del Alumno",
    #     max_length=50,
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    fecha_certificacion = forms.DateField(
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    bachillerato = forms.ModelChoiceField(
        queryset=Bachillerato.objects.all(),
        label="Bachillerato",
        widget=forms.Select(attrs={'class': 'form-control', 'style':'width:300px'}),
        required=True,
        empty_label="Seleccione un bachillerato"
    )
    semestre = forms.IntegerField(
    label="Semestre",
    widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
)

class LetraFoliadorForm(forms.Form):
    letra_foliador = forms.CharField(
        label = "Letra",
        max_length=1,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

class FormFiltroCertificadosP(forms.Form):
    curp = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'class':'form-control','placeholder':'CURP del alumno'}))
    fecha_certificacion = forms.DateField(
        required= False,
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    ct = forms.CharField(required = False,
                        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Centro de Trabajo'}))