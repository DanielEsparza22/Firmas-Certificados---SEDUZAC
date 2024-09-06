from django import forms

# Formulario para la CURP a cancelar
class CancelarCertForm(forms.Form):
    curp = forms.CharField(
        label='CURP',
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px'})
    )
    observaciones = forms.CharField(
        label='Observaciones',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba las observaciones de la cancelación...',
            'rows': 3,
            'cols': 55,
            'style': 'resize: none;'
        }),
        required=False
    )