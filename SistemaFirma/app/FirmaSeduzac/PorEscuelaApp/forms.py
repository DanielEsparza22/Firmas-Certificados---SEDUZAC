from django import forms


class RegistrosPorEscuelaForm(forms.Form):
    clave_ct = forms.CharField(
        label="Clave CT",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_certificacion = forms.DateField(
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    periodo = forms.CharField(
        label="Periodo",
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ej. 2022-2023'})
    )

class LetraFoliadorForm(forms.Form):
    letra_foliador = forms.CharField(
        label = "Letra",
        max_length=1,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    