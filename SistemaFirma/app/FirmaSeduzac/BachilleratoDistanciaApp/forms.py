from django import forms

# Formulario para registros a insertar para Bachillerato a Dsitancia
class RegistrosBachilleratoDForm(forms.Form):
    clave_ct = forms.CharField(
        label="Clave CT",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_certificacion = forms.DateField(
        label="Fecha de Certificación",
        widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'})
    )
    semestre = forms.IntegerField(
    label="Semestre",
    widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
    )