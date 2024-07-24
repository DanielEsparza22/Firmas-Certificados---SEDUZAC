from django.db import models

# Modelo que guarda la secuencia para el folio de Certificados Completos
class FolioSequenceCC(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{str(self.id)}'

# Modelo para guardar la letra del folio
class FolioLetraCC(models.Model):
    letra = models.CharField(max_length=1, default='A')

    def __str__(self):
        return f'{self.letra}'

