from django.db import models
import re
from django.core.exceptions import ValidationError

class FolioSequence(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{str(self.id)}'
    
class FolioLetra(models.Model):
    letra = models.CharField(max_length=1, default='A')

    def __str__(self):
        return f'{self.letra}'
    

def validate_certificado_autoridad(value):
    if not re.fullmatch(r'\d{20}', value):
        raise ValidationError('El certificado de la autoridad educativa no es correcto.')
    
class AutoridadEducativa(models.Model):
    nombre_autoridad = models.CharField(max_length=100, default="MARIBEL VILLALPANDO HARO. SECRETARIA DE EDUCACIÓN DEL ESTADO DE ZACATECAS.")
    certificado_autoridad = models.CharField(
        max_length=20,
        validators=[validate_certificado_autoridad],
        default="00000000000000008682"
    )