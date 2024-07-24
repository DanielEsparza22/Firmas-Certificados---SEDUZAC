from django.db import models

# Modelo para guardar la secuencia numerica del Folio para Bachillerato a Distancia
class FolioSequenceBD(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{str(self.id)}'
