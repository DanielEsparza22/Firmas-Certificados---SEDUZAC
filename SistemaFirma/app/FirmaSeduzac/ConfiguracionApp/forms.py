from django import forms
from .models import AutoridadEducativa, Bachillerato

class LetraFoliadorForm(forms.Form):
    letra_foliador = forms.CharField(
        label = "Letra",
        max_length=1,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )

class AutoridadEducativaForm(forms.ModelForm):
    class Meta:
        model = AutoridadEducativa
        fields = '__all__'

        widgets = {
            'nombre_autoridad': forms.TextInput(attrs={'style': 'width: 80%;',
                                                       'placeholder':'NOMBRE EJEMPLO. SECRETARIO(A) DE EDUCACIÓN DEL ESTADO DE ZACATECAS.'}),
            'certificado_autoridad':forms.TextInput(attrs={'placeholder':'0000000000000000XXXX'})
        }

    def __init__(self, *args, **kwargs):
        super(AutoridadEducativaForm, self).__init__(*args, **kwargs)
        self.fields['nombre_autoridad'].initial = ''
        self.fields['certificado_autoridad'].initial = ''

# Formulario bachillerato
class FormBachillerato(forms.ModelForm):
    class Meta:
        model = Bachillerato
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del bachillerato...',
                'style':'width: 475px'
            })
        }
        labels = {
            'nombre': 'Ingrese el nombre del bachillerato',
        }