from django import forms

# Formulario para la CURP a verificaar
class CertificacionCForm(forms.Form):
    curp = forms.CharField(
        label='CURP',
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px'})
    )

# Formulario para los datos a insertar
class RegistrosCompletasForm(forms.Form):
    # clave_alumno = forms.CharField(
    #     label="Clave del Alumno",
    #     max_length=50,
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
    fecha_certificacion = forms.DateField(
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    bachillerato = forms.CharField(
        label="Bachillerato",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'width:300px', 'placeholder':'BACHILLERATO GENERAL'}),
        required=False,
    )

# Formulario para actualizar la letra del foliador
class LetraFoliadorForm(forms.Form):
    letra_foliador = forms.CharField(
        label = "Letra",
        max_length=1,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

class FormFiltroCertificadosT(forms.Form):
    curp = forms.CharField(required = False,
                            widget = forms.TextInput(attrs={'class':'form-control','placeholder':'CURP del alumno'}))
    fecha_certificacion = forms.DateField(
        required= False,
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    ct = forms.CharField(required = False,
                        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Centro de Trabajo'}))
